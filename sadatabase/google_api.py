from django.conf import settings

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import os.path
import pickle
from datetime import datetime, timezone, timedelta


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


def create_event(data):

    service = build_service()

    event = {
        'summary': data["title"],
        'location': "",
        'description': data["title"],
        'start': {
            'dateTime': datetime.combine(data["date"], datetime.min.time()).astimezone(timezone.utc).isoformat(),
            'timeZone': 'America/Chicago',
        },
        'end': {
            'dateTime': (datetime.combine(data["date"], datetime.min.time()).astimezone(timezone.utc)+timedelta(days=1)).isoformat(),
            'timeZone': 'America/Chicago',
        },
    }
    created_event = service.events().insert(calendarId="primary", body=event).execute()
    print(f"Created event: {created_event['id']}")
