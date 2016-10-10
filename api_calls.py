from __future__ import print_function
import httplib2
import os
import json

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

# Only needed for tests currently
import datetime
import pprint as pp

import argparse

parser = argparse.ArgumentParser(parents=[tools.argparser])
flags = parser.parse_args()

SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Ember Google Calendar API Access'


def get_credentials(user):
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'account-credentials-' + user + '.json')

    store = oauth2client.file.Storage(credential_path)  # stores the users credentials --> TODO: put in database
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME

        credentials = tools.run_flow(flow, store, flags)

        print('Storing credentials to ' + credential_path)
    return credentials


def get_freebusy_query(user, time_min, time_max):
    """Gets the freebusy data from a calendar between time_min and time_max.

    Returns:
        A json that contains all of the times in which the user is busy.
    """
    credentials = get_credentials(user)
    http = credentials.authorize(httplib2.Http())

    service = discovery.build('calendar', 'v3', http=http)

    request_query = {
        "timeMin": time_min,
        "timeMax": time_max,
        "items": [
            {
                "id": "primary"
            }
        ]
    }

    # POST request to get freebusy data between timeMin and timeMax
    request = service.freebusy().query(body=request_query).execute()
    return json.dumps(request)


def insert_event(user, request_body):
    """Creates event in users calendar
    """
    credentials = get_credentials(user)
    http = credentials.authorize(httplib2.Http())

    service = discovery.build('calendar', 'v3', http=http)

    service.events().insert(calendarId='primary', body=request_body).execute()


# Currently used to test both functionalities with dummy values
if __name__ == '__main__':
    # Test for freebusy method
    free_busy = get_freebusy_query("test", datetime.datetime.utcnow().isoformat() + 'Z',
                       (datetime.datetime.utcnow() + datetime.timedelta(days=1)).isoformat() + 'Z')
    pp.pprint(free_busy)

    # Test for inserting an event (currently inserts an hour long event 1 hour from now)
    dummy_event_body = {
        'summary': 'Test Event!',
        'location': '201 N Goodwin Ave, Urbana, IL 61801',
        'description': 'Check out this cool test event!',
        'start': {
          'dateTime': (datetime.datetime.utcnow() + datetime.timedelta(hours=1)).isoformat() + 'Z',
        },
        'end': {
            'dateTime': (datetime.datetime.utcnow() + datetime.timedelta(hours=2)).isoformat() + 'Z',
        }
    }
    insert_event("test", dummy_event_body)