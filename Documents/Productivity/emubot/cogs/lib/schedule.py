from cogs.lib.lecture import Lecture
import json
import os

"""
WORK IN PROGRESS
author: William Chen

1) function: add remind table that returns the time to remind lecture
"""

PATH = os.path.dirname(__file__)

class Schedule():

	def __init__(self, name, periods, ifamelective, userID):
		self.periods = []
		self.name = name
		self.userID = userID
		if ifamelective:
			for i in range(0, len(periods)):
				self.periods.append(Lecture(periods[i], i, userID))
		else:
			for i in range(0, len(periods)):
				self.periods.append(Lecture(periods[i],i+1, userID))

	def writeSchedule(d):
		with open(PATH + '/schedules.txt', 'w') as f:
			f.write(json.dumps(d))

	def readSchedule():
		with open(PATH + '/schedules.txt', 'r') as f:
			return json.load(f)

	def readScheduleInstance(self):
		with open(PATH + '/schedules.txt', 'r') as f:
			return json.load(f)

	def appendSchedule(self):
		exists = False
		dct = self.readScheduleInstance() 
		l = []
		for period in self.periods:
			l.append(period.toList())
		for i in range(0, len(dct['schedule'])):
			if dct['schedule'][i]['name'] == self.name or dct['schedule'][i]['periods'][0][2] == self.userID:
				dct['schedule'][i]['periods'] = l
				dct['schedule'][i]['name'] = self.name
				exists = True
		if not exists:
			dct['schedule'].append({'name':self.name, 'periods':l})
		with open(f'{PATH}/schedules.txt', 'w') as f:
			f.write(json.dumps(dct))