import discord
from discord.ext import commands

import asyncio
import re
import os
import json
import yaml

import dbVars
import botDecorators

class Owner(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		
	@commands.command(aliases = ['logs_cuc'])
	@commands.is_owner()
	async def delete_commands_usage_counter(self, ctx):
		try:
			with open("./.db/logs/commandsUsageCounter.yml", "r") as read_file: commandsUsageCounter = yaml.safe_load(read_file)
			commandsUsageCounter["all"]["use"] = 0
			commandsUsageCounter["all"]["success"] = 0
			commandsUsageCounter["all"]["lose"] = 0
			commandsUsageCounter["all"]["error"] = 0

			commandsUsageCounter["repeat"]["use"] = 0
			commandsUsageCounter["repeat"]["success"] = 0
			commandsUsageCounter["repeat"]["lose"] = 0
			commandsUsageCounter["repeat"]["error"] = 0

			commandsUsageCounter["time"]["use"] = 0
			commandsUsageCounter["time"]["success"] = 0
			commandsUsageCounter["time"]["lose"] = 0
			commandsUsageCounter["time"]["error"] = 0
			with open("./.db/logs/commandsUsageCounter.yml", "w") as write_file: yaml.safe_dump(commandsUsageCounter, write_file, sort_keys = False, allow_unicode = True)
			await ctx.send("успешно!")
		except ValueError as e:
			await ctx.send(str(e))
		except Exception as e:
			print(e)
	
	@commands.command(aliases = ['sgp'])
	@commands.is_owner()
	async def set_guild_params(self, ctx):
		try:
			await ctx.send("скоро")
		except ValueError as e:
			await ctx.send(str(e))
		except Exception as e:
			print(e)

async def setup(bot):
	await bot.add_cog(Owner(bot))