import discord
from discord.ext import commands
from cogs.lib.schedule import Schedule
from cogs.lib.intakeProcess import IntakeProcess
"""
author: William Chen

"""

class scheduleIntake(commands.Cog):

	def __init__(self, client):
		self.client = client
		self.processes = []
		for i in range(0, 20):
			self.processes.append(None)

	@commands.Cog.listener()
	async def on_ready(self):
		print('Schedule Intake is ready')

	@commands.command()
	async def enter(self, ctx):
		for i in range(0, len(self.processes)):
			if (self.processes[i]==None):
				self.processes[i] = IntakeProcess(ctx, self.client)
				await ctx.send(embed = self.processes[i].embed)
				return
				for j in range(0, len(self.processes)):
					if processes[j].processauthor == ctx.message.author and i!=j:
						processes[j] = None
				return
			elif i == len(self.processes):
				await ctx.send("There are too many processes going on right now, please wait!")
				return
		#start the schedule enter process


	@commands.Cog.listener()
	async def on_message(self, msg):
		for i in range(0, len(self.processes)):
			if self.processes[i] != None:
				if self.processes[i].inEnter == False:
					self.processes[i] = None
				else:
					result = self.processes[i].scheduleProcess(msg)
					if result:
						counter = 0
						async for message in msg.channel.history(limit = 10):
							if message.author == self.client.user or message.author == msg.author and counter < 2:
								await message.delete()
								counter+=1
						await msg.channel.send(embed = result)

def setup(client):
	client.add_cog(scheduleIntake(client))