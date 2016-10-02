import datetime
import json
import os
from dateutil import rrule
from datetime import datetime, timedelta

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
				for time_set in data_set['calendars']['primary']['busy']:
						self.my_events.append(event(datetime.strptime(time_set['end'], "%Y-%m-%dT%H:%M:%Sz"), datetime.strptime(time_set['start'],"%Y-%m-%dT%H:%M:%Sz")))

#Params: 2 calendar objects
#Returns: A list of size 2 lists containing start of that free block and the end of that free block.
def checkTime(cal1, cal2):
		calendar_collection = [cal1,cal2]
		free_zones_JSON = []
		in_free_time = False

		#These are simply dummy times and will be changed once we check sections larger than 24h
		start = datetime(2016,9,20)
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
													"minute": dt.minute
											})
					in_free_time = True
				elif(not allCalendarsFree and in_free_time):
					free_zones_JSON.append({
													"type": "end",
													"hour": dt.hour,
													"minute": dt.minute
											})
					in_free_time = False
					
		#if the 2 cals are free until the end of that day
		if(in_free_time):
			free_zones_JSON.append({
											"type": "end",
											"hour": 23,
											"minute": 59
									})

		#The Json Object we return.
		return {
				'day': 1,
				'free_zones': free_zones_JSON
		}


#Params: A list of calendars
#Returns: If all the calendars are free at the time checked
def checkCountCalendars(calendar_collection):
	count = 0
	for calendarCHECK in calendar_collection:
		if(calendarCHECK.event_counter == 0):
			count+=1
	return count == len(calendar_collection)


def getJSONSandcheck():
	#Curently reads 2 dummy JSON files
	if(os.path.isfile('calendar1.json')):
				with open('calendar1.json') as data_file:
						calendar1_data = json.load(data_file)
	calendar1 = calendar()
	calendar1.add_events(calendar1_data)

	if(os.path.isfile('calendar2.json')):
				with open('calendar2.json') as data_file:
						calendar2_data = json.load(data_file)
	calendar2 = calendar()
	calendar2.add_events(calendar2_data)

	with open('free_times.json', 'w') as outfile:
			json.dump(checkTime(calendar1,calendar2), outfile)

def create_timeslots(data_set):
		global time_slots
		time_slots = []
		free_zone_starts = []
		free_zone_ends = []
		for free_zone in data_set['free_zones']:
				if free_zone['type'] == "start":
						free_zone_starts.append(str(free_zone["hour"]) + ":" + str(free_zone['minute']).zfill(2))
				else:
						free_zone_ends.append(str(free_zone["hour"]) + ":" + str(free_zone['minute']).zfill(2))
		for i in range(len(free_zone_starts)):
				time_slots.append(time_slot(free_zone_starts[i], free_zone_ends[i]))


def generate_email():
		message = "Hello, \nBoth parties have the following time slots avaiable to meet: \n"
		for time_slot in time_slots:
				message += time_slot.start_time + " to " + time_slot.end_time + "\n"
		print message

if __name__ == "__main__":
		getJSONSandcheck()
		if(os.path.isfile('free_times.json')):
					with open('free_times.json') as data_file:
							free_times_data = json.load(data_file)
		create_timeslots(free_times_data)
		generate_email()
