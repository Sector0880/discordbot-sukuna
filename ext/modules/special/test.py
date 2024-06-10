import discord
from discord.ext import commands
from discord import app_commands

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
	
	group = app_commands.Group(name = 'test', description = 'lol')
		
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
			#await ctx.send(embed = em)
			await ctx.send(dbVars.cspl_get_param(ctx, 'u', 'profile'))
		except ValueError as e:
			await ctx.send(str(e))
		except Exception as e:
			print(repr(e))
	
	
	@group.command(name="ggg", description="...")
	async def _ping(self, interaction: discord.Interaction, server_id: discord.Member):
		await interaction.response.send_message("pong!")

async def setup(bot):
	await bot.add_cog(Test(bot))