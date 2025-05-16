import django.conf
from django.conf import settings

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import os.path
import pickle
from datetime import datetime, timezone, timedelta
from dateutil import tz


def build_service():
    scopes = ['https://www.googleapis.com/auth/calendar']
    creds = None

    if os.path.exists(os.path.join(settings.GOOGLE_API, 'token.pickle')):
        with open(os.path.join(settings.GOOGLE_API, 'token.pickle'), 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                os.path.join(settings.GOOGLE_API, 'credentials.json'), scopes)
            creds = flow.run_local_server(port=0)

        with open(os.path.join(settings.GOOGLE_API, 'token.pickle'), 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    return service


def format_event(data):

    # if django.conf.settings.DEBUG:
    #     kwargs1 = {"days": 0, "hours": 0}
    #     kwargs2 = {"days": 1, "hours": 0}
    # else:
    #     kwargs1 = {"days": 0, "hours": 5}
    #     kwargs2 = {"days": 1, "hours": 5}

    event = {
        'summary': data["title"],
        'location': "",
        'description': data["title"],
        'start': {
            'dateTime': datetime.combine(data["date"], datetime.min.time()).isoformat(),
            'timeZone': 'America/Chicago',
        },
        'end': {
            'dateTime': (datetime.combine(data["date"], datetime.min.time())+ timedelta(days=1)).isoformat(),
            'timeZone': 'America/Chicago',
        },
    }

    return event


def create_google_event(data):

    service = build_service()
    event = format_event(data)

    created_event = service.events().insert(calendarId="primary", body=event).execute()
    print(f"Created event: {created_event['id']}")
    return created_event["id"]


def update_google_event(data):

    service = build_service()
    event = format_event(data)

    updated_event = service.events().update(calendarId="primary", eventId=data["id"], body=event).execute()
    print(f"Updated event: {updated_event['id']}")


def remove_google_event(event_id):

    service = build_service()
    try:
        service.events().delete(calendarId="primary", eventId=event_id).execute()
    except:
        print("resource already deleted")


def getall_google_events():
    service = build_service()
    return service.events().list(calendarId="primary").execute()
