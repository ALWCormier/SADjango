from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from .models import Application, Event

from datetime import datetime, timedelta
from dateutil import tz

from .google_api import build_service, create_google_event, update_google_event
from .google_api import remove_google_event, getall_google_events
from .models import PreviousParticipantEntities


@receiver(post_save, sender=Application)
def update_events(sender, instance, created, **kwargs):
    # dates that could get added to the calendar
    date_fields = {"Commitment_Due_Original", "Commitment_Due_New", "Carryover_Due_Original", "Carryover_Due_New",
                   "Ten_Percent_Due_Original", "Ten_Percent_Due_New", "Cost_Cert_Due_Original", "Cost_Cert_Due_New",
                   "CSR_Due_Original", "CSR_Due_New", "PiS_Due_Original", "PiS_Due_New"}

    if not created:

        # if updating and update fields are specified, they are using the admin panel, which is more work
        if not kwargs["update_fields"]:

            try:
                events_for_app = Event.objects.get(application=instance)
                all_google_events = getall_google_events()
                for db_apps_event in events_for_app:
                    fdate = datetime.combine(db_apps_event, datetime.min.time()).astimezone(
                        tz.gettz("America/Chicago")).isoformat()
                    for google_event in all_google_events:
                        if google_event.id == db_apps_event.google_id and google_event.start == fdate:
                            name = " ".join(db_apps_event.field_name.split("_")[:-1])
                            update_google_event(
                                {"title": f"{name} for {db_apps_event.development_name}", "date": db_apps_event.date,
                                 "id": db_apps_event.google_id})
                            print(f"updated: {name}")
            except:
                event_dates = set()
                for field in date_fields:
                    if getattr(instance, field):
                        event_dates.add(field)

        # get the intersection of relevant date fields and fields that have been changed
        else:
            event_dates = date_fields & kwargs["update_fields"]

    else:
        event_dates = set()
        for field in date_fields:
            if getattr(instance, field):
                event_dates.add(field)

    # get or create event object, storing (obj, created) in output
    events = []
    for date_field_name in event_dates:
        new_event_tuple = Event.objects.get_or_create(
            development_name=instance.Development_Name,
            field_name=date_field_name,
            defaults={"application": instance, "date": getattr(instance, date_field_name)},
        )
        new_event_tuple[0].save()
        events.append(new_event_tuple)

    for event, new_event in events:
        if not new_event:
            name = " ".join(event.field_name.split("_")[:-1])
            event.date = getattr(instance, event.field_name)
            event.save()
            if event.date:
                update_google_event({"title": f"{name} for {event.development_name}", "date": event.date,
                                     "id": event.google_id})
                print("updated an event")
            else:
                event.delete()

        else:
            name = " ".join(event.field_name.split("_")[:-1])
            event_id = create_google_event({"title": f"{name} for {event.development_name}", "date": event.date})
            event.google_id = event_id
            event.save()
            print("created an event")


@receiver(post_delete, sender=Event)
def remove_events(sender, instance, **kwargs):
    # google api remove event
    remove_google_event(instance.google_id)
