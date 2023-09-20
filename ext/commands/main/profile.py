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

class ProfileCommands(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
	
	@app_commands.command(
		name = "profile"
	)
	async def profile(self, interaction: discord.Interaction, user: discord.Member = None):
		try:
			profile = interaction.user if not user else user
			roles = profile.roles
			role_list = ''
			role_list_number = 0

			for role in reversed(roles):
				if role != interaction.guild.default_role:
					role_list += f'<@&{role.id}> '
					role_list_number += 1
				
			if profile.status == discord.Status.online:
				status = '<:online:748149457396433016> В сети'
			elif profile.status == discord.Status.idle:
				status = '<:idle:748149485707984907> Не активен'
			elif profile.status == discord.Status.dnd:
				status = '<:dnd:748149518167441411> Не беспокоить'
			else:
				status = '<:offline:748149539915038731> Не в сети'
			
			emb = discord.Embed(colour = color_success)
			emb.set_author(name = f'{profile}', icon_url = profile.avatar)
			emb.set_thumbnail(url = profile.avatar)
			emb.add_field(name = 'Присоеденился к Discord', value = profile.created_at.strftime('**Дата:** %d/%m/%Y\n**Время:** %H:%M:%S'))
			emb.add_field(name = 'Присоеденился к серверу', value = profile.joined_at.strftime('**Дата:** %d/%m/%Y\n**Время:** %H:%M:%S'))
			emb.add_field(name = 'Статус', value = status, inline = False)
			emb.add_field(name = f'Роли [{role_list_number}]', value = 'Отсутствуют' if role_list == '' else role_list, inline = False)
			#emb.set_footer(text = f'ID: {profile.id}')
			emb.timestamp = datetime.utcnow()

			await interaction.response.send_message(embed = emb, ephemeral=True)
		except Exception as e:
			await interaction.response.send_message(e, ephemeral=True)

async def setup(bot: commands.Bot):
	await bot.add_cog(ProfileCommands(bot))