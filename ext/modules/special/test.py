import discord
from discord.ext import commands
from discord import app_commands

import asyncio
import re
import os
import json
import yaml
import postgrest

from dbVars import *
import botDecorators

from supabase import create_client, Client

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
			print(cspl_get_param(interaction, 'g', 'status', ['modules', 'economy', 'events', 'economy_system']))
		except Exception as e:
			print(repr(e))

	@commands.command()
	@commands.is_owner()
	async def t(self, ctx):
		try:
			await ctx.send(cspl_get_param(ctx, 'u', 'xp', ['economy']))
		except ValueError as e:
			await ctx.send(str(e))
		except Exception as e:
			print(repr(e))

async def setup(bot):
	await bot.add_cog(Test(bot))