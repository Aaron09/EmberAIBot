import datetime

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
                    for time_set in data_set['calendars'][calendar_id]['busy']:
                            self.my_events.append(event(datetime.datetime.strptime(time_set['end'], "%Y-%m-%dT%H:%M:%Sz"), datetime.datetime.strptime(time_set['start'],"%Y-%m-%dT%H:%M:%Sz")))
