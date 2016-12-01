import json, os, datetime, pytz, calendar_object, api_calls, dateutil, email_creation
from dateutil import rrule
#Params: 2 calendar objects
#Returns: A list of size 2 lists containing start of that free block and the end of that free block.
def check_time(calendar_list):
        calendar_collection = calendar_list
        free_zones_JSON = []
        in_free_time = False

        best_free_count = float("inf")
        best_free_start = datetime.datetime.utcnow()
        best_free_end = datetime.datetime.utcnow()
        waitng_for_best_end = False

        start = datetime.datetime.utcnow()
        #start.replace(tzinfo= pytz.timezone('US/Central'))
        end = start + datetime.timedelta(days=1)

        for dt in dateutil.rrule.rrule(dateutil.rrule.MINUTELY, dtstart=start, until=end):
            for calendar in calendar_collection:
                for event in calendar.my_events:
                    if(event.event_starts(dt.hour,dt.minute)):
                            calendar.event_counter +=1
                    elif (event.event_ends(dt.hour,dt.minute)):
                            calendar.event_counter -= 1
                #check if all cals are free
                allCalendarsFree = check_count_calendars(calendar_collection)

                if(find_num_avaiable(calendar_collection) < best_free_count and not waitng_for_best_end):
                    print("started",dt,find_num_avaiable(calendar_collection))
                    best_free_count = find_num_avaiable(calendar_collection)
                    best_free_start = dt
                    waitng_for_best_end = True
                if(find_num_avaiable(calendar_collection) != best_free_count and waitng_for_best_end):
                    print("ended",dt,find_num_avaiable(calendar_collection))
                    best_free_end = dt
                    waitng_for_best_end = False
                

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
                                            "hour": end.hour,
                                            "minute": end.minute,
                                            "day":end.day,
                                            "month":end.month,
                                            "year":end.year
                                    })

        #The Json Object we return.
        free_zones_JSON = clean_up_times(free_zones_JSON) 
               
        if( len(free_zones_JSON) < 2):
            free_zones_JSON.append({
                                            "type": "start",
                                            "hour": best_free_start.hour,
                                            "minute": best_free_start.minute,
                                            "day": best_free_start.day,
                                            "month": best_free_start.month,
                                            "year": best_free_start.year
                                    })
            free_zones_JSON.append({
                                            "type": "end",
                                            "hour": best_free_end.hour,
                                            "minute": best_free_end.minute,
                                            "day": best_free_end.day,
                                            "month": best_free_end.month,
                                            "year": best_free_end.year
                                    })
        
        return {
                'day': 1,
                'free_zones': free_zones_JSON
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
def check_count_calendars(calendar_collection):
    count = 0
    for calendarCHECK in calendar_collection:
        if(calendarCHECK.event_counter == 0):
            count+=1
    return count == len(calendar_collection)

def find_num_avaiable(calendar_collection):
    count = 0
    for calendarCHECK in calendar_collection:
        count+=calendarCHECK.event_counter
    return count