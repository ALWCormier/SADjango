from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Application, Event

from .google_api import create_event


@receiver(post_save, sender=Application)
def update_events(sender, instance, created, **kwargs):

    # dates that could get added to the calendar
    date_fields = {"Commitment_Due_Original", "Commitment_Due_New", "Carryover_Due_Original", "Carryover_Due_New",
                   "Ten_Percent_Due_Original", "Ten_Percent_Due_New", "Cost_Cert_Due_Original", "Cost_Cert_Due_New",
                   "CSR_Due_Original", "CSR_Due_New", "PiS_Due_Original", "PiS_Due_New"}

    if not created:

        # if updating and update fields are specified, they are using the admin panel, which doesnt support calendar updates
        if not kwargs["update_fields"]:
            return

        # get the intersection of relevant date fields and fields that have been changed
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
            event.date = getattr(instance, event.field_name)
            event.save()

            print("updated an event")

        else:
            name = " ".join(event.field_name.split("_")[:-1])
            create_event({"title": f"{name} for {event.development_name}",
                          "date": event.date})
            print("created an event")


@receiver(post_delete, sender=Event)
def remove_events(sender, instance, **kwargs):

    # google api remove event
    print("event deleted")
