import discord
from discord.ext import commands
from cogs.lib.schedule import Schedule
from cogs.lib.lecture import Lecture

class IntakeProcess():
	
	def __init__(self, ctx, client):
		self.client = client
		self.channel = ctx.message.channel
		self.processauthor = ctx.message.author
		self.inEnter = True

		self.inName = True
		self.name = ''

		self.inAM = False
		self.ifAM = False
		
		self.periods = []

		self.embed = discord.Embed(
			colour = discord.Colour.dark_blue(),
			title = "You have begun a process to enter your schedule, please enter your name: ",
			description = "Available Commands: back to reenter last entry, clear to clear all entries, quit to end the menu",
			author = "Emu Bot"
			)

	def enterName(self, message):
		self.embed = discord.Embed(
				colour = discord.Colour.dark_blue(),
				title = "Next: Do you have AM elective or not? Yes or no?",
				description = "Available Commands: back to reenter last entry, clear to clear all entries, quit to end the menu",
				author = "emu bot"
				)
		self.embed.add_field(name = "Your name has been saved", value = message.content)
		self.name = message.content
		self.inName = False
		self.inAM = True
		return self.embed


	def enterSchedule(self, message):
		if message.content.lower() == "done":
			self.embed = discord.Embed(title = "OK, your response have been recorded", description = "To rewrite the schedule, simply repeat the process. To add zoom link to your lectures, type ;zoom", colour = discord.Colour.dark_blue()) 
			self.storeSchedule(self.name, self.periods, self.ifAM, str(self.processauthor.id))
			self.inEnter = False

		elif len(self.periods) >= 10:
			self.embed = discord.Embed(title = "OK, your response have been recorded", description = "To rewrite the schedule, simply repeat the process. To add zoom link to your lectures, type ;zoom", colour = discord.Colour.dark_blue()) 
			self.storeSchedule(self.name, self.periods, self.ifAM, str(self.processauthor.id))
			self.inEnter = False

		else:
			self.periods.append(message.content)
			self.embed.add_field(name = f'Period {len(self.periods) - (self.ifAM)}', value = message.content)
			return self.embed

	def enterIfAM(self, message):
		self.embed = discord.Embed(
			title = 'Next up, enter your class names in order. When you are done, just type done! (Also, type in Lunch as a normal period. I will not ping you when the period is named lunch!',
			description = 'Available Commands: back to reenter last entry, clear to clear all entries, quit to end the menu'
			)
		if message.content.lower() == "yes" or message.content.lower() == "true":
			self.ifAM = True
		elif message.content.lower() == "no" or message.content.lower() == "false":
			self.ifAM = False
		self.inAM = False


	def goBack(self, message):
		if self.inEnter and len(self.embed.fields) == 1:
			self.inAM = True
			self.inAM = False
			self.embed.remove_field(len(self.embed.fields)-1)
			return self.embed
		elif self.inAM == True:
			self.inName = True 
			self.inAM = False
			self.embed.remove_field(len(self.embed.fields)-1)
			return self.embed
		else:
			self.embed.remove_field(len(self.embed.fields)-1)
			self.periods.pop(-1)
			return self.embed

	def clear(self):
		self.inEnter = True

		self.inName = True
		self.name = ''

		self.inAM = False
		self.ifAM = False
		
		self.periods = []

		self.embed = discord.Embed(
			colour = discord.Colour.dark_blue(),
			description = "Available Commands: back to reenter last entry, clear to clear all entries, quit to end the menu",
			title = "You have begun a process to enter your schedule, please enter your name: ",
			author = "emu bot")

	def scheduleProcess(self, message):
		if message.channel != self.channel:
			return None

		if message.author != self.processauthor:
			return None

		if message.author == self.client.user:
			return None
			#no self recursion

		if message.content[0] == ";":
			return None

		if self.inEnter == False:
			return None

		if message.content.lower() == 'go back' or message.content.lower() == 'back':
			return self.goBack(message)

		if message.content.lower() == 'clear':
			self.clear()
			return self.embed

			#no interfering with actual command
		if ((message.content.lower() == 'quit') or (message.content.lower() == 'q')):
			if self.processauthor == message.author:
				self.inEnter = False
			return None

		elif self.inName:
			self.enterName(message)
			return self.embed
			#first order in the process. Store your name

		elif self.inAM:
			self.enterIfAM(message)
			return self.embed
			#Last event in the process. Store if you have AM elective or not

		else:
			self.enterSchedule(message)
			return self.embed
			#The Middle Event in the process, Store your period information


	def storeSchedule(self, name, periods, ifAM, userID):
		sched = Schedule(name, periods, ifAM, userID)
		sched.appendSchedule()