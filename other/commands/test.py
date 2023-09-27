import discord
from discord.ext import commands, tasks
from discord import app_commands

import json
import asyncio
from dbVars import *

class TestCommands(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
	
	@commands.command()
	async def f(self, ctx):
		try:
			await ctx.send(bot_presence())
		except Exception as e:
			print(e)

async def setup(bot: commands.Bot):
	await bot.add_cog(TestCommands(bot))