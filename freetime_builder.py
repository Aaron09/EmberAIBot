
import json, os, datetime, pytz, calendar_object, api_calls, dateutil, email_creation, calendar_algorithim

#takes json input for specific calendar and creates new calendar object with data from json
def create_calendar(json_data):
    calendar_new = calendar()
    calendar_new.add_events(json.loads(json_data))
    return calendar_new

#creates json file with all the free times between calendars
def create_free_times_json(calendar_list):
    with open('free_times.json', 'w') as outfile:
        json.dump(calendar_algorithim.check_time(calendar_list), outfile)

def make_event(data_set, best_time):
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
    return email_creation.generate_email_content(free_times_data) #return to Aaron for email

#main method to execute whole process
#AARON THIS IS FOR YOU!
#@Params email_list list of strings -- corresponds to users emails
#@Returns formatted string for email
def build_free_times(email_list):
    calendars = []
    for email in email_list:
        json_file = json.loads(api_calls.get_all_freebusy_queries(email, datetime.datetime.utcnow().isoformat() + 'Z', (datetime.datetime.utcnow() + datetime.timedelta(days=1)).isoformat() + 'Z'))

        calendar_new = calendar_object.calendar()
        for cal in json_file:
            calendar_new.add_events(json_file[cal])
        calendars.append(calendar_new)
    #print calendars
    # for cal in calendars:
    #     for event in cal.my_events:
    #         print(event.start_time , event.end_time)
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
            event = make_event(data_set, idealTime)

            #print(event)

            #add to users calendars
            for user in emails:
               api_calls.insert_event(user,event)

            return email_creation.generate_best_time_email(data_set, idealTime)


if __name__ == '__main__':
    build_free_times(["jonah.casebeer@gmail.com","jonahmc2@illinois.edu"])
    print(return_free_times())
    #print(find_best_time_and_email(times,["iuqwog"]))
    # json_file1 = get_freebusy_query("email1", datetime.datetime.utcnow().isoformat() + 'Z', (datetime.datetime.utcnow() + datetime.timedelta(days=1)).isoformat() + 'Z')
    # json_file2 = get_freebusy_query("email2", datetime.datetime.utcnow().isoformat() + 'Z', (datetime.datetime.utcnow() + datetime.timedelta(days=1)).isoformat() + 'Z')
    # print(json_file1)
    # print(json_file2)
    # calendars.append(create_calendar(json_file1))
    # calendars.append(create_calendar(json_file2))
    # create_free_times_json(calendars)
