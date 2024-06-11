import discord
from discord.ext import commands
from discord import app_commands

import asyncio
import re
from dbVars import *
from botFunctions import *


class Settings(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	profile_commands = app_commands.Group(name = "profile", description = "Команды для настройки профиля пользователя.")

	def set_profile_param(self, interaction, param: str, content):
		custom_users = json.load(open("./.db/crossplatform/custom/users.json", "r", encoding="utf-8"))
		if str(interaction.user.id) not in custom_users:
			custom_users[str(interaction.user.id)] = {}
		if str(interaction.guild.id) not in custom_users[str(interaction.user.id)]:
			custom_users[str(interaction.user.id)][str(interaction.guild.id)] = {}
		if "profile" not in custom_users[str(interaction.user.id)][str(interaction.guild.id)]:
			custom_users[str(interaction.user.id)][str(interaction.guild.id)]["profile"] = {}
		custom_users[str(interaction.user.id)][str(interaction.guild.id)]["profile"][param] = str(content)
		with open("./.db/crossplatform/custom/users.json", "w", encoding="utf-8") as write_file: json.dump(custom_users, write_file, ensure_ascii = False, indent = 4)
	
	async def del_profile_param(self, interaction, param: str):
		custom_users = json.load(open("./.db/crossplatform/custom/users.json", "r", encoding="utf-8"))
		if str(interaction.user.id) not in custom_users:
			custom_users[str(interaction.user.id)] = {}
		if str(interaction.guild.id) not in custom_users[str(interaction.user.id)]:
			custom_users[str(interaction.user.id)][str(interaction.guild.id)] = {}
		if "profile" not in custom_users[str(interaction.user.id)][str(interaction.guild.id)]:
			custom_users[str(interaction.user.id)][str(interaction.guild.id)]["profile"] = {}
		if str(param) not in custom_users[str(interaction.user.id)][str(interaction.guild.id)]["profile"]:
			return await interaction.response.send_message(f"В Вашем профиле не указан {param}.")
		
		# Удалить параметр из профиля
		custom_users[str(interaction.user.id)][str(interaction.guild.id)]["profile"].pop(str(param))
		
		# Проверка и удаление profile, если он стал пустым
		if not custom_users[str(interaction.user.id)][str(interaction.guild.id)]["profile"]:
			del custom_users[str(interaction.user.id)][str(interaction.guild.id)]["profile"]
		
		# Проверка и удаление str(interaction.guild.id), если profile стал пустым
		if not custom_users[str(interaction.user.id)][str(interaction.guild.id)]:
			del custom_users[str(interaction.user.id)][str(interaction.guild.id)]
		
		# Проверка и удаление str(interaction.user.id), если str(interaction.guild.id) стал пустым
		if not custom_users[str(interaction.user.id)]:
			del custom_users[str(interaction.user.id)]
		
		with open("./.db/crossplatform/custom/users.json", "w", encoding="utf-8") as write_file: json.dump(custom_users, write_file, ensure_ascii=False, indent=4)
	

	@profile_commands.command(
		name = "set_profile_about",
		description = 'Добавить биографию для своего профиля на сервере.'
	)
	async def set_profile_about(self, interaction: discord.Interaction, *, content: str):
		try:
			self.set_profile_param(interaction, "about", content)
			await interaction.response.send_message(f"```json\n{cspl_custom_users(interaction)[str(interaction.user.id)][str(interaction.guild.id)]['profile']}\n```", ephemeral = True)
		except Exception as e:
			print(repr(e))
	
	@profile_commands.command(
		name = "set_profile_age",
		description = 'Добавить возраст для своего профиля на сервере.'
	)
	async def set_profile_age(self, interaction: discord.Interaction, content: str):
		try:
			self.set_profile_param(interaction, "age", content)
			await interaction.response.send_message(f"```json\n{cspl_custom_users(interaction)[str(interaction.user.id)][str(interaction.guild.id)]['profile']}\n```", ephemeral = True)
		except Exception as e:
			print(repr(e))
	
	@profile_commands.command(
		name = "set_profile_city",
		description = 'Добавить город для своего профиля на сервере.'
	)
	async def set_profile_city(self, interaction: discord.Interaction, *, content: str):
		try:
			self.set_profile_param(interaction, "city", content)
			await interaction.response.send_message(f"```json\n{cspl_custom_users(interaction)[str(interaction.user.id)][str(interaction.guild.id)]['profile']}\n```", ephemeral = True)
		except Exception as e:
			print(repr(e))
	
	@profile_commands.command(
		name = "del_profile_about",
		description = 'Удалить биографию из своего профиля на сервере.'
	)
	async def del_profile_about(self, interaction: discord.Interaction):
		try:
			await self.del_profile_param(interaction, "about")
			await interaction.response.send_message("Успешно удалена биография.")
		except Exception as e:
			print(repr(e))
	
	@profile_commands.command(
		name = "del_profile_age",
		description = 'Удалить свой возраст из своего профиля на сервере.'
	)
	async def del_profile_age(self, interaction: discord.Interaction):
		try:
			await self.del_profile_param(interaction, "age")
			await interaction.response.send_message("Успешно удален возраст.")
		except Exception as e:
			print(repr(e))
	
	@profile_commands.command(
		name = "del_profile_city",
		description = 'Удалить город из своего профиля на сервере.'
	)
	async def del_profile_city(self, interaction: discord.Interaction):
		try:
			await self.del_profile_param(interaction, "city")
			await interaction.response.send_message("Успешно удален город.")
		except Exception as e:
			print(repr(e))

			
async def setup(bot):
	await bot.add_cog(Settings(bot))