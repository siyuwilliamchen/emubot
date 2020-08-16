import discord
import os
from discord.ext import commands, tasks
"""
WORK IN PROGRESS
author: William Chen

PROJECT TO-DO list:
1) Schedule-remind section
2) Homework-collect section
3) Other functions

"""
client = commands.Bot(command_prefix = ';')
PATH = os.path.dirname(__file__)
client.remove_command('help')

version = '0.1.4'
@client.event
async def on_ready():
	print(f"Emu Bot is ready... v {version}")

@client.command()
async def about(ctx):
	display = discord.Embed(
		author = 'William Chen',
		colour = discord.Colour.blue(),
		title = 'Developed by William Chen',
		description = f'Current Version: v{version}'
		)
	await ctx.channel.send(embed = display)

@client.command()
async def load(ctx, extension):
	if ctx.message.author.id == 479427064336875530:
		client.load_extension(f'cogs.{extension}')
		await ctx.send('Requested module loaded')
		return
	await ctx.send('You do not have permission to use this command')

@client.command()
async def unload(ctx, extension):
	if ctx.message.author.id == 479427064336875530:
		client.unload_extension(f'cogs.{extension}')
		await ctx.send('Requested module unloaded')
		return
	await ctx.send('You do not have permission to use this command')

for filename in os.listdir(PATH + '/cogs'):
	if filename.endswith('.py'):
		client.load_extension(f'cogs.{filename[:-3]}')

client.run(os.environ['DISCORD_TOKEN'])