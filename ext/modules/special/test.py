import discord
from discord.ext import commands

import asyncio
import re
import os
import json
import yaml

import dbVars
import botDecorators

class Test(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		
	@commands.command()
	@commands.is_owner()
	async def t(self, ctx):
		try:
			em = discord.Embed(
				title="Слеш команды",
				description="Список всех слеш команд бота",
				color=discord.Color.blurple())

			for slash_command in self.bot.tree.walk_commands():
				em.add_field(name=slash_command.name, 
							value=slash_command.description if slash_command.description else slash_command.name, 
							inline=False) 
			await ctx.send(embed = em)
		except ValueError as e:
			await ctx.send(str(e))
		except Exception as e:
			print(e)

async def setup(bot):
	await bot.add_cog(Test(bot))