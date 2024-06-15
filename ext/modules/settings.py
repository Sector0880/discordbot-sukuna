import discord
from discord.ext import commands
from discord import app_commands

import asyncio
import re
from dbVars import *
from botFunctions import *

class Profile(commands.GroupCog, name = "profile"):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		super().__init__()
	
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
	

	@app_commands.command(
		name = "set_about",
		description = 'Добавить биографию для своего профиля на сервере.'
	)
	async def set_about(self, interaction: discord.Interaction, *, content: str):
		try:
			self.set_profile_param(interaction, "about", content)
			await interaction.response.send_message(f"```json\n{cspl_custom_users(interaction)[str(interaction.user.id)][str(interaction.guild.id)]['profile']}\n```", ephemeral = True)
		except Exception as e:
			print(repr(e))
	
	@app_commands.command(
		name = "set_age",
		description = 'Добавить возраст для своего профиля на сервере.'
	)
	async def set_age(self, interaction: discord.Interaction, content: int):
		try:
			self.set_profile_param(interaction, "age", content)
			await interaction.response.send_message(f"```json\n{cspl_custom_users(interaction)[str(interaction.user.id)][str(interaction.guild.id)]['profile']}\n```", ephemeral = True)
		except Exception as e:
			print(repr(e))
	
	@app_commands.command(
		name = "set_city",
		description = 'Добавить город для своего профиля на сервере.'
	)
	async def set_city(self, interaction: discord.Interaction, *, content: str):
		try:
			self.set_profile_param(interaction, "city", content)
			await interaction.response.send_message(f"```json\n{cspl_custom_users(interaction)[str(interaction.user.id)][str(interaction.guild.id)]['profile']}\n```", ephemeral = True)
		except Exception as e:
			print(repr(e))
	
	@app_commands.command(
		name = "del_about",
		description = 'Удалить биографию из своего профиля на сервере.'
	)
	async def del_about(self, interaction: discord.Interaction):
		try:
			await self.del_profile_param(interaction, "about")
			await interaction.response.send_message("Успешно удалена биография.")
		except Exception as e:
			print(repr(e))
	
	@app_commands.command(
		name = "del_age",
		description = 'Удалить свой возраст из своего профиля на сервере.'
	)
	async def del_age(self, interaction: discord.Interaction):
		try:
			await self.del_profile_param(interaction, "age")
			await interaction.response.send_message("Успешно удален возраст.")
		except Exception as e:
			print(repr(e))
	
	@app_commands.command(
		name = "del_city",
		description = 'Удалить город из своего профиля на сервере.'
	)
	async def del_city(self, interaction: discord.Interaction):
		try:
			await self.del_profile_param(interaction, "city")
			await interaction.response.send_message("Успешно удален город.")
		except Exception as e:
			print(repr(e))
	
	@app_commands.command(
		name = "show",
		description = 'Показать профиль юзера.'
	)
	async def show(self, interaction: discord.Interaction, user: discord.Member = None):
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
				status = '<a:mark_none:815121643479236618> Не беспокоить'
			else:
				status = '<:offline:748149539915038731> Не в сети'
			
			emb = discord.Embed(colour = 0x2b2d31)
			emb.set_author(name = f'{profile}', icon_url = profile.avatar)
			emb.set_thumbnail(url = profile.avatar)
			if user != self.bot.user:
				emb.add_field(name = 'Профиль', value = '\n'.join([
					f"**О себе:** {cspl_get_param(interaction, 'u', 'about', 'profile', user if user else None)}" if cspl_get_param(interaction, 'u', 'about', 'profile', user if user else None) else "**О себе:** `нету`",
					f"**Возраст:** {cspl_get_param(interaction, 'u', 'age', 'profile', user if user else None)}" if cspl_get_param(interaction, 'u', 'age', 'profile', user if user else None) else "**Возраст:** `нету`",
					f"**Город:** {cspl_get_param(interaction, 'u', 'city', 'profile', user if user else None)}" if cspl_get_param(interaction, 'u', 'city', 'profile', user if user else None) else "**Город:** `нету`",
				]), inline = False)
			else:
				emb.add_field(name = 'Профиль', value = '\n'.join([
					f"**О себе:** 3990см хуй блять нахуй",
					f"**Возраст:** 2000+",
					f"**Город:** Залупа",
				]), inline = False)
			#emb.add_field(name = 'Статус', value = status, inline = False)
			emb.add_field(name = f'Роли [{role_list_number}]', value = 'Отсутствуют' if role_list == '' else role_list, inline = False)
			emb.add_field(name = 'В Discord', value = profile.created_at.strftime('**Дата:** %d/%m/%Y\n**Время:** %H:%M:%S'))
			emb.add_field(name = 'На сервере', value = profile.joined_at.strftime('**Дата:** %d/%m/%Y\n**Время:** %H:%M:%S'))
			emb.set_footer(text = f'ID: {profile.id}')
			emb.timestamp = datetime.now()

			await interaction.response.send_message(embed = emb, ephemeral=True)
		except Exception as e:
			await interaction.response.send_message(repr(e), ephemeral=True)

class Settings(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.profile_commands = Profile(bot)
	
	@app_commands.command(
		name = "switch",
		description = "Изменить переключатели настроек бота."
	)
	@app_commands.checks.has_permissions(administrator = True)
	@app_commands.default_permissions(administrator = True)
	async def switch(self, interaction: discord.Interaction, switch: str):
		await interaction.response.send_message("Скоро...", ephemeral=True)
	
	
	async def setup_profile_commands(self):
		await self.bot.add_cog(self.profile_commands)


async def setup(bot):
	settings = Settings(bot)
	await settings.setup_profile_commands()
	await bot.add_cog(settings)