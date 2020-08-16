import discord
from discord.ext import commands

class help(commands.Cog):

	def __init__(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_ready(self):
		print('Bot help menu is ready')

	@commands.command()
	async def help(self, ctx):
		display = discord.Embed(
			title = 'Emu Bot Help Menu',
			author = 'Emu Bot',
			colour = discord.Colour.red(),
			description = 'This is a table for allowed commands and their functions! <> means you have to enter specified information after the command itself separated by a space. For example, correct way to call ;zoom would be ;zoom 3 link'
			)
		display.add_field(
			name = ';help', value = 'To bring up this command'
			)
		display.add_field(
			name = ';enter', value = 'To enter your schedule. After you do it, you can have the bot remind you when you have class! If you are not OK with sharing your schedule, do not use this!'
			)
		display.add_field(
			name = ';zoom <period> <link>', value = 'type ;zoom, your period number, and your zoom url, separated by space.'
			)
		display.add_field(
			name = ';remind', value = 'After you have entered your schedule, turn this on for daily remind before lecture'
			)
		display.add_field(
			name = ';remindOff', value = 'To stop daily remind before lecture'
			)
		display.add_field(
			name = ';find', value = 'Display a detailed description of your schedule'
			)
		display.add_field(
			name = ';delete', value = 'Delete your schedule from the database'
			)
		display.add_field(
			name = ';about', value= 'Checks the development status of the project.'
			)
		await ctx.channel.send(embed = display)

def setup(client):
	client.add_cog(help(client))