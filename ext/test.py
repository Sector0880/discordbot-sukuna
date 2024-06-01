import discord
from discord.ext import commands

import asyncio
import re
import os
import json

from dbVars import *

class Test(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		
	@commands.command()
	async def t(self, ctx, param, item):
		try:
			await ctx.send('hi')
		except ValueError as e:
			await ctx.send(str(e))
		except Exception as e:
			print(e)

async def setup(bot):
	await bot.add_cog(Test(bot))