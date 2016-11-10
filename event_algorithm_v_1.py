import datetime
import json
import os
from dateutil import rrule
from datetime import datetime, timedelta
from pytz import timezone
import pytz
from api_calls import *
import api_calls as CalendarHandler

class time_slot(object):
        def __init__(self,in_start_time,in_end_time):
            self.start_time = in_start_time
            self.end_time = in_end_time

class event(object):
        def __init__(self, input_end_time, input_start_time):
                self.end_time = input_end_time
                self.start_time = input_start_time
        #Params: hour and minute ints.
        #Returns: whether events objects start time is at that time
        def event_starts(self,hour, minute):
                if hour == self.start_time.hour and minute == self.start_time.minute:
                        return True
                return False
        #Params: hour and minute ints.
        #Returns: whether events objects end time is at that time.
        def event_ends(self,hour, minute):
                if hour == self.end_time.hour and minute == self.end_time.minute:
                        return True
                return False


class calendar(object):
        def __init__(self):
                self.my_events = []
                self.event_counter = 0

        #Params: parsed JSON file for individual user (contains all events)
        #adds all events as objects from provided calendar data set to the calender object
        def add_events(self, data_set):
                for calendar_id in data_set['calendars']:
                    for time_set in calendar_id['busy']:
                            self.my_events.append(event(datetime.datetime.strptime(time_set['end'], "%Y-%m-%dT%H:%M:%Sz"), datetime.datetime.strptime(time_set['start'],"%Y-%m-%dT%H:%M:%Sz")))

#Params: 2 calendar objects
#Returns: A list of size 2 lists containing start of that free block and the end of that free block.
def checkTime(calendar_list):
        calendar_collection = calendar_list
        free_zones_JSON = []
        in_free_time = False

        #These are simply dummy times and will be changed once we check sections larger than 24h
        start = datetime.datetime.utcnow()
        #start.replace(tzinfo= pytz.timezone('US/Central'))
        end = start + timedelta(days=1)

        for dt in rrule.rrule(rrule.MINUTELY, dtstart=start, until=end):
            for calendar in calendar_collection:
                for event in calendar.my_events:
                    if(event.event_starts(dt.hour,dt.minute)):
                            calendar.event_counter +=1
                    elif (event.event_ends(dt.hour,dt.minute)):
                            calendar.event_counter -= 1
                #check if all cals are free
                allCalendarsFree = checkCountCalendars(calendar_collection)

                if(allCalendarsFree and not in_free_time):
                    free_zones_JSON.append({
                                                    "type": "start",
                                                    "hour": dt.hour,
                                                    "minute": dt.minute,
                                                    "day": dt.day,
                                                    "month": dt.month,
                                                    "year": dt.year
                                            })
                    in_free_time = True
                elif(not allCalendarsFree and in_free_time):
                    free_zones_JSON.append({
                                                    "type": "end",
                                                    "hour": dt.hour,
                                                    "minute": dt.minute,
                                                    "day": dt.day,
                                                    "month": dt.month,
                                                    "year": dt.year
                                            })
                    in_free_time = False

        #if the 2 cals are free until the end of that day
        if(in_free_time):
            free_zones_JSON.append({
                                            "type": "end",
                                            "hour": 23,
                                            "minute": 59,
                                            "day":dt.day,
                                            "month":dt.month,
                                            "year":dt.year
                                    })

        #The Json Object we return.
        return {
                'day': 1,
                'free_zones': clean_up_times(free_zones_JSON)
        }

def clean_up_times(free_zones_JSON):
    free_zone_starts = []
    free_zone_ends = []
    for free_zone in free_zones_JSON:
        start_end = datetime.datetime(free_zone['year'], free_zone['month'], free_zone['day'] ,free_zone["hour"], free_zone['minute'])

        if free_zone['type'] == "start":
            free_zone_starts.append(start_end)
        else:
            free_zone_ends.append(start_end)

    free_start_end = zip(free_zone_starts,free_zone_ends)
    final_start_end = []
    for free_era in free_start_end:
        time_diff = free_era[1]-free_era[0]
        if divmod(time_diff.days * 86400 + time_diff.seconds , 60)[0] > 10:
            final_start_end.append({
                                                    "type": "start",
                                                    "hour": free_era[0].hour,
                                                    "minute": free_era[0].minute,
                                                    "day": free_era[0].day,
                                                    "month": free_era[0].month,
                                                    "year": free_era[0].year
                                            })
            final_start_end.append({
                                                    "type": "end",
                                                    "hour": free_era[1].hour,
                                                    "minute": free_era[1].minute,
                                                    "day": free_era[1].day,
                                                    "month": free_era[1].month,
                                                    "year": free_era[1].year
                                            })
    return (final_start_end)

#Params: A list of calendars
#Returns: If all the calendars are free at the time checked
def checkCountCalendars(calendar_collection):
    count = 0
    for calendarCHECK in calendar_collection:
        if(calendarCHECK.event_counter == 0):
            count+=1
    return count == len(calendar_collection)


#takes json input for specific calendar and creates new calendar object with data from json
def create_calendar(json_data):
    calendar_new = calendar()
    calendar_new.add_events(json.loads(json_data))
    return calendar_new

#creates json file with all the free times between calendars
def create_free_times_json(calendar_list):
    with open('free_times.json', 'w') as outfile:
            json.dump(checkTime(calendar_list), outfile)

def utc_to_local(utc_dt):
    local_tz = pytz.timezone('US/Central')
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt) # .normalize might be unnecessary

def break_up_freezones(data_set):
    free_zone_starts = []
    free_zone_ends = []
    for free_zone in data_set['free_zones']:
        start_end = datetime.datetime(free_zone['year'], free_zone['month'], free_zone['day'] ,free_zone["hour"], free_zone['minute'])
        localized = utc_to_local(start_end)
        string_localized = localized.strftime("%m-%d-%Y %I:%M %p")
        if free_zone['type'] == "start":
            free_zone_starts.append(string_localized)
            #free_zone_starts.append(str(free_zone["hour"]) + ":" + str(free_zone['minute']).zfill(2))
        else:
            free_zone_ends.append(string_localized)
            #free_zone_ends.append(str(free_zone["hour"]) + ":" + str(free_zone['minute']).zfill(2))
    return (free_zone_starts, free_zone_ends)

# creates email message with all the free times
def generate_email_content(data_set):
    free_zones = break_up_freezones(data_set)
    message = "Hello, \nBoth parties have the following time slots avaiable to meet: \n"
    for i in range(len(free_zones[0])):
        message += free_zones[0][i] + " to " + free_zones[1][i] + "\n"
    return message

def generate_best_time_email(data_set, best_time):
    (free_zone_starts, free_zone_ends) = break_up_freezones(data_set)
    message = "Hello, \nthe final meeting time will be from \n"
    message += free_zonez[0][best_time] + " to " + free_zones[1][best_time] + "\n"
    return message

#return the first free time and puts it in json to be added to calendar
#OPHIR THIS IS FOR YOU!
def return_time(data_set, best_time):
    free_zone_starts = []
    free_zone_ends = []
    for free_zone in data_set['free_zones']:
        if free_zone['type'] == "start":
            free_zone_starts.append(datetime.datetime(free_zone['year'], free_zone['month'], free_zone['day'] ,free_zone["hour"], free_zone['minute']).isoformat())
        else:
            free_zone_ends.append(datetime.datetime(free_zone['year'], free_zone['month'], free_zone['day'] ,free_zone["hour"], free_zone['minute']).isoformat())

    event_body = {
        'summary': 'Test Event!',
        'location': '201 N Goodwin Ave, Urbana, IL 61801',
        'description': 'Check out this cool test event!',
        'start': {
          'dateTime': free_zone_starts[best_time] + 'Z',
        },
        'end': {
            'dateTime': free_zone_ends[best_time] + 'Z',
        }
    }
    #TODO: Here we will call Ophir's function and pass the eventbody json for
    # ophir's magic to add to the calendar
    return event_body

#opens json file and creates email content
def return_free_times():
    if(os.path.isfile('free_times.json')):
        with open('free_times.json') as data_file:
                free_times_data = json.load(data_file)
    return generate_email_content(free_times_data) #return to Aaron for email

#main method to execute whole process
#AARON THIS IS FOR YOU!
#@Params email_list list of strings -- corresponds to users emails
#@Returns formatted string for email
def main(email_list):
    calendars = []
    for email in email_list:
        json_file = json.loads(get_all_freebusy_queries(email, datetime.datetime.utcnow().isoformat() + 'Z', (datetime.datetime.utcnow() + datetime.timedelta(days=1)).isoformat() + 'Z'))

        calendar_new = calendar()
        for cal in json_file:
            calendar_new.add_events(json_file[cal])
        calendars.append(calendar_new)

    create_free_times_json(calendars)
    return (return_free_times())

#@Params dict of time indexs and popularity
#@Returns formatted email and uploads object
def find_best_time_and_email(freq_times,emails):
    if(os.path.isfile('free_times.json')):
        with open('free_times.json') as data_file:
            #clean data set
            data_set = json.load(data_file)

            #make event to be added to calendar

            idealTime = max(freq_times, key=freq_times.get)-1
            event = return_time(data_set, idealTime)

            #print(event)

            #add to users calendars
            for user in emails:
               CalendarHandler.insert_event(user,event)

            return generate_best_time_email(data_set, idealTime)


if __name__ == '__main__':
    main(["jonah.casebeer@gmail.com","jonahmc2@illinois.edu"])
    print(return_free_times())
    #print(find_best_time_and_email(times,["iuqwog"]))
    # json_file1 = get_freebusy_query("email1", datetime.datetime.utcnow().isoformat() + 'Z', (datetime.datetime.utcnow() + datetime.timedelta(days=1)).isoformat() + 'Z')
    # json_file2 = get_freebusy_query("email2", datetime.datetime.utcnow().isoformat() + 'Z', (datetime.datetime.utcnow() + datetime.timedelta(days=1)).isoformat() + 'Z')
    # print(json_file1)
    # print(json_file2)
    # calendars.append(create_calendar(json_file1))
    # calendars.append(create_calendar(json_file2))
    # create_free_times_json(calendars)
