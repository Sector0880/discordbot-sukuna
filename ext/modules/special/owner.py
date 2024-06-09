import discord
from discord.ext import commands

import asyncio
import re
import os
import json

import dbVars

class Owner(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		
	@commands.command()
	@commands.is_owner()
	async def t(self, ctx, set):
		try:
			await ctx.send(dbVars.cspl_get_param(ctx, "g", set))
		except ValueError as e:
			await ctx.send(str(e))
		except Exception as e:
			print(e)

async def setup(bot):
	await bot.add_cog(Owner(bot))