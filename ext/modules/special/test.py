import discord
from discord.ext import commands
from discord import app_commands

import asyncio
import re
import os
import json
import yaml

from dbVars import *
import botDecorators

class Test(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		
	@app_commands.command(
		name = "test",
		description="тестовая команда (только для овнера)"
	)
	async def test(self, interaction: discord.Interaction):
		try:
			if interaction.user.id not in sf_sp(): return await interaction.response.send_message("Нету прав.")
			await interaction.response.send_message('тест', ephemeral=True, delete_after=3)
		except Exception as e:
			print(repr(e))

	@commands.command()
	@commands.is_owner()
	async def t(self, ctx: discord.Message):
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

			print(cspl_get_param(ctx, 'g', 'prefix'))
		except ValueError as e:
			await ctx.send(str(e))
		except Exception as e:
			print(repr(e))

async def setup(bot):
	await bot.add_cog(Test(bot))