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
		
	@app_commands.command(
		name = "test",
		description="тестовая команда (только для овнера)"
	)
	async def test(self, interaction: discord.Interaction):
		if interaction.user.id not in dbVars.sf_sp(): return await interaction.response.send_message("Нету прав.")
		await interaction.response.send_message(dbVars.cspl_get_param(interaction, 'u', 'xp', 'economy'))

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
			await ctx.send(dbVars.cspl_get_param(ctx, 'u', 'xp', 'economy'))
		except ValueError as e:
			await ctx.send(str(e))
		except Exception as e:
			print(repr(e))

async def setup(bot):
	await bot.add_cog(Test(bot))