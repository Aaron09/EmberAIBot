import datetime, pytz

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
    free_zones = break_up_freezones(data_set)
    message = "Hello, \nthe final meeting time will be from \n"
    message += free_zones[0][best_time] + " to " + free_zones[1][best_time] + "\n"
    return message

def utc_to_local(utc_dt):
    local_tz = pytz.timezone('US/Central')
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt) # .normalize might be unnecessary