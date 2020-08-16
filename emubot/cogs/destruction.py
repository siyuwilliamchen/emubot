import discord
from discord.ext import commands

VICTIMS = ['koolkid420', 'koolkid666']

class Destruction(commands.Cog):
	"""docstring for Descruction"""
	def __init__(self, client):
		self.client = client


	@commands.Cog.listener()
	async def on_message(self, msg):
		for victim in VICTIMS:
			if msg.author.display_name == victim:
				msg.delete()