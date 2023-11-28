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
	async def h(self, ctx, item):
		try:
			if ctx.author.id not in [980175834373562439, 522136072151367691, 224632121879166976]: return await ctx.send("Нету прав.") # на автора сообщения
			await ctx.send(guild_item(ctx, item))
		except ValueError as e:
			await ctx.send(str(e))
		except Exception as e:
			print(e)

async def setup(bot):
	await bot.add_cog(Test(bot))