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

from firebase import firebase

import argparse

parser = argparse.ArgumentParser(parents=[tools.argparser])
flags = parser.parse_args()

SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Ember Google Calendar API Access'

FIREBASE_SECRET = 'lrr9Q2GQI7jqZEx00m3SZBSwzyP8Ym2bi4TufPJT'


def get_credentials(user):
    # TODO: CHANGE AUTHORIZATION TO NOT BE PUBLIC
    authentication = firebase.FirebaseAuthentication(FIREBASE_SECRET, 'emberuiucbot@gmail.com')

    database = firebase.FirebaseApplication('https://ember-ai-146020.firebaseio.com', authentication=authentication)

    token = database.get('/users', user.replace('.', '(dot)').replace('@', '(at)'))
    credentials = client.AccessTokenCredentials(token['token'], 'my-user-agent/1.0')
    # credentials = client.GoogleCredentials(token['token'], "295894273459-m5r8e3572ru6vs7tlvjpor2o99bv7g1l.apps.googleusercontent.com", "BQhM6U69IS0XHK8itNb0vjpV", token['refreshToken'], 1, "https://accounts.google.com/o/oauth2/token", 'my-user-agent/1.0')
    # print(credentials.to_json()) TODO: remove (and above)

    return credentials


def credientials_exist(user):
    authentication = firebase.FirebaseAuthentication(FIREBASE_SECRET, 'emberuiucbot@gmail.com')
    database = firebase.FirebaseApplication('https://ember-ai-146020.firebaseio.com', authentication=authentication)
    return not database.get('/users', user.replace('.', '(dot)').replace('@', '(at)')) is None


def get_freebusy_query(user, time_min, time_max):
    """Gets the freebusy data from a calendar between time_min and time_max.

    Returns:
        A json that contains all of the times in which the user is busy.
    """
    credentials = get_credentials(user) # string
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
    # credentials.refresh(http) TODO: remove
    # print(credentials.to_json()) TODO: remove

    service = discovery.build('calendar', 'v3', http=http)

    service.events().insert(calendarId='primary', body=request_body).execute()


# Currently used to test both functionalities with dummy values
if __name__ == '__main__':
    # # Test for freebusy method
    # free_busy = get_freebusy_query("emberuiucbot@gmail.com", datetime.datetime.utcnow().isoformat() + 'Z',
    #                    (datetime.datetime.utcnow() + datetime.timedelta(days=1)).isoformat() + 'Z')
    # pp.pprint(free_busy)
    #
    # # Test for inserting an event (currently inserts an hour long event 1 hour from now)
    # dummy_event_body = {
    #     'summary': 'Test Event!',
    #     'location': '201 N Goodwin Ave, Urbana, IL 61801',
    #     'description': 'Check out this cool test event!',
    #     'start': {
    #       'dateTime': (datetime.datetime.utcnow() + datetime.timedelta(hours=1)).isoformat() + 'Z',
    #     },
    #     'end': {
    #         'dateTime': (datetime.datetime.utcnow() + datetime.timedelta(hours=2)).isoformat() + 'Z',
    #     }
    # }
    # insert_event("emberuiucbot@gmail.com", dummy_event_body)
    #
    print(credientials_exist("emberuiucbot@gmail.com"))
    print(credientials_exist("pranayiscool"))