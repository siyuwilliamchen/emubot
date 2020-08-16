import discord
import datetime
from discord.ext import tasks,commands
from cogs.lib.schedule import Schedule
from cogs.lib.lecture import Lecture
import json
import os
"""
WORK IN PROGRESS
author: William Chen

TO-DO LIST:
2) command: turn remind on / off
8) command: update zoom link for lectures
10) sectional help function


DONE:
3) command: getAllSchedules(person) (if none inputted, get all)
"""

PATH = os.path.dirname(__file__)

class scheduleProcessor(commands.Cog):

	def __init__(self, client):
		self.client = client
		self.timetable = [845, 930, 1015, 1100, 1145, 1230, 1315, 1400, 1445]
		self.signups = self.loadSignups()
		self.inZoom = False
		self.inTeacher = False
		#a list of people who signed up for remind, the people's format is a list of length 2, ppl[0] = name, ppl[1] = user.id

	@commands.Cog.listener()
	async def on_ready(self):
		self.checkSched.start()
		print('Schedule Processor is ready')



	def writeSignups(self, l):
		with open(f'{PATH}/lib/signups.txt', 'w') as f:
			f.write(json.dumps(l))

	def appendSignups(self, userid):
		curr = self.loadSignups()
		curr.append(userid)
		self.writeSignups(curr)

	def loadSignups(self):
		with open(f'{PATH}/lib/signups.txt', 'r') as f:
			return json.load(f)

	@tasks.loop(seconds = 30)
	async def checkSched(self):
		for signup in self.signups:
			if self.findScheduleInstance(signup):
				await self.remind(self.findScheduleInstance(signup), signup)

	async def remind(self, schedule, userid):
		currDate = datetime.date.today()
		currTime = datetime.datetime.now()
		if currDate.weekday() <= 6:
		 	for period in schedule.periods:
		 		if period.period < 9:
		 			if currTime.hour == (self.timetable[period.period] / 100) and currTime.minute == (self.timetable[period.period] % 100):
		 				await self.client.get_user(userid).send(f'Hey, you have {period.period} period: {period.name} right now, the zoom link is {period.zoomlink}, if you would like disable this remind, type ;remindOff, if you want to update your zoom meetings, type ;zoom <period> <link>')

	@commands.command(aliases = ['remind', 'remindme'])
	async def remindOn(self, ctx):
		schedules = self.unserialize(Schedule.readSchedule())
		self.appendSignups(ctx.message.author.id)
		await ctx.send('OK, you have signed up for the schedule remind function!')

	@commands.command()
	async def remindOff(self, ctx):
		signups = self.loadSignups()
		for i in range(0, len(signups)):
			if signups[i] == ctx.message.author.id:
				signups.pop(i)
			await ctx.send('OK, you have removed yourself from the schedule remind function!')
		await ctx.send('We have not found you in or sign up lists.')



	@commands.command(aliases = ['show','showall', 'showallschedule', 'allschedules'])
	async def showAllSchedule(self, ctx):
		if ctx.message.author.id != 479427064336875530:
			await ctx.send('Sorry, you are not authorized to use this command')
			return
		schedules = self.unserialize(Schedule.readSchedule())
		display = discord.Embed(
			title = 'All Schedules Entry in the Data Base',
			colour = discord.Colour.green(),
			description = 'Available Methods: none',
			author = 'Emu Bot'
			)
		for schedule in schedules:
			periodnames = []
			for period in schedule.periods:
				periodnames.append(period.name)
			display.add_field(
				name = f'The schedule of {schedule.name}',
				value = str(periodnames)
				)
		await ctx.send(embed = display)

	@commands.command(aliases = ['deleteSched','scheduledelete','deleteschedule', 'delete'])
	async def deleteSchedule(self, ctx):
		found = False
		schedules = self.unserialize(Schedule.readSchedule())
		for i in range(0, len(schedules)):
			if not found:
				if schedules[i].periods[0].userid == str(ctx.message.author.id):
					schedules.pop(i)
					found = True
		Schedule.writeSchedule(self.serialize(schedules))
		if found:
			await ctx.send('Schedule found and deleted')
		else:
			await ctx.send('Schedule not found, try again')

	@commands.command(aliases = ['find', 'findsched', 'schedulefind'])
	async def findSchedule(self, ctx):
		found = False
		schedules = self.unserialize(Schedule.readSchedule())
		for schedule in schedules:
			if schedule.periods[0].userid == str(ctx.message.author.id):
				display = discord.Embed(
					title = f'Schedule of {schedule.name}',
					author = 'Emu Bot',
					colour = discord.Colour.green(),
					description = 'This is your schedule'
					)
				for period in schedule.periods:
					display.add_field(
						name = f'Period {period.period}',
						value = f'{period.name} \n Zoom Link: {period.zoomlink}'
						)
				await ctx.send(embed = display)


	@commands.command(aliases = ['zoom'])
	async def updateZoom(self, ctx, *, s):
		info = s.split()
		num = None
		link = None
		schedules = self.unserialize(Schedule.readSchedule())
		for i in range(0, len(schedules)):
			if schedules[i].periods[0].userid == str(ctx.message.author.id):
				try:
					num = int(info[0])
					link = info[1]
				except:
					await ctx.channel.send('Please separate them by space!')
					return
				for j in range(0, len(schedules[i].periods)):
					if schedules[i].periods[j].period == num:
						schedules[i].periods[j].zoomlink = link
						Schedule.writeSchedule(self.serialize(schedules))
						await ctx.message.delete()
						await ctx.channel.send('Your zoom link has been updated!')
						return
		await ctx.channel.send('Oops, something went wrong, make sure your period number is correct and try again!')
		return

	def findScheduleInstance(self, userid):
		schedules = self.unserialize(Schedule.readSchedule())
		for schedule in schedules:
			if schedule.periods[0].userid == str(userid):
				return schedule

	def serialize(self, schedules):
		#takes a list of schedules, returns to the serialized json dictionary
		#schedules is a list of schedules objects
		result = {'schedule':[]}
		for schedule in schedules:
			p = []
			for period in schedule.periods:
				p.append(period.toList())
			d = {'name':schedule.name, 'periods':p}
			result['schedule'].append(d)
		return result


	def unserialize(self, d):
		#takes a serialized json dictionary, unserialize it to a list of schedules
		result = []
		for dct in d['schedule']:
			name = dct['name']
			lectures = []
			for period in dct['periods']:
				lectures.append(Lecture(period[0], period[1], period[2], period[3]))
			schedule = Schedule(name, [], False, period[3])
			schedule.periods = lectures
			result.append(schedule)
		return result


def setup(client):
	client.add_cog(scheduleProcessor(client))