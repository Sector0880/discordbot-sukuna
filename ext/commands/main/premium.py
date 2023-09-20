import discord
from discord.ext import commands, tasks
from discord import app_commands
# не юзай блять
#from discord import Option

import yaml
import json
import re
import asyncio
import uuid
from time import sleep
from datetime import datetime, timedelta

from botConfig import *
from dbVars import *
import botFunctions
	
class PremiumCommands(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@app_commands.command(
		name = "check_premium",
		description = "Проверить премиум-статус у сервера (показывает данные с базы данных)"
	)
	@botFunctions.check_command_permissions()
	async def check_premium(self, interaction: discord.Interaction):
		# open db
		with open("./.db/multiplayer/guilds.json", "r", encoding="utf-8") as read_file: guilds_config_data = json.load(read_file)
		privileges_0 = guilds_config_data[str(interaction.guild.id)]["additional-features"]["privileges"][0]  # path to privileges in server

		emb = discord.Embed(
			title = f'Премиум на сервере: {guilds_config_data[str(interaction.guild.id)]["overview"]["guild-name"]}',
			color = 0xFFD700 if guild_premium(interaction) else 0x2b2d31
		)
		emb.add_field(
			name = "Статус",
			value= f'Осталось: `{str(datetime.fromisoformat(guild_premium_time_end(interaction)) - datetime.now())[:-7]}`' if guild_premium(interaction) else "Премиум отсутствует"
		)
		"""
		emb.add_field(
			name = "База данных",
			value = f'```ansi\n\u001b[0;33m{json.dumps(privileges_0, ensure_ascii = False, indent = 4)}\u001b[0m```',
			inline=False
		)
		"""
		await interaction.response.send_message(embed = emb, ephemeral = True)

async def setup(bot: commands.Bot):
	await bot.add_cog(PremiumCommands(bot))