import discord
from discord.ext import commands
from discord import app_commands

import asyncio
import enum
import re
from dbVars import *
from botFunctions import *

class Biography(commands.GroupCog, name = "biography"):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		super().__init__()
		self.stop = False
	
	def set_biography_param(self, interaction, param: str, content):
		custom_users = json.load(open("./.db/crossplatform/custom/users.json", "r", encoding="utf-8"))
		if str(interaction.user.id) not in custom_users:
			custom_users[str(interaction.user.id)] = {}
		if str(interaction.guild.id) not in custom_users[str(interaction.user.id)]:
			custom_users[str(interaction.user.id)][str(interaction.guild.id)] = {}

		if "biography" not in custom_users[str(interaction.user.id)][str(interaction.guild.id)]:
			custom_users[str(interaction.user.id)][str(interaction.guild.id)]["biography"] = {}
		custom_users[str(interaction.user.id)][str(interaction.guild.id)]["biography"][param] = str(content)
		with open("./.db/crossplatform/custom/users.json", "w", encoding="utf-8") as write_file: json.dump(custom_users, write_file, ensure_ascii = False, indent = 4)
	
	async def del_biography_param(self, interaction, param: str, all = False):
		try:
			custom_users = json.load(open("./.db/crossplatform/custom/users.json", "r", encoding="utf-8"))
			if str(interaction.user.id) not in custom_users:
				custom_users[str(interaction.user.id)] = {}
			if str(interaction.guild.id) not in custom_users[str(interaction.user.id)]:
				custom_users[str(interaction.user.id)][str(interaction.guild.id)] = {}
			if "biography" not in custom_users[str(interaction.user.id)][str(interaction.guild.id)]:
				custom_users[str(interaction.user.id)][str(interaction.guild.id)]["biography"] = {}
			if all == False:
				if str(param) not in custom_users[str(interaction.user.id)][str(interaction.guild.id)]["biography"]:
					await interaction.response.send_message(f"В Вашей биографии не указан {param}.")
					self.stop = True
					return
			
			# Удалить параметр из профиля
			custom_users[str(interaction.user.id)][str(interaction.guild.id)]["biography"].pop(str(param))
			
			# Проверка и удаление biography, если он стал пустым
			if not custom_users[str(interaction.user.id)][str(interaction.guild.id)]["biography"]:
				del custom_users[str(interaction.user.id)][str(interaction.guild.id)]["biography"]
			
			# Проверка и удаление str(interaction.guild.id), если biography стал пустым
			if not custom_users[str(interaction.user.id)][str(interaction.guild.id)]:
				del custom_users[str(interaction.user.id)][str(interaction.guild.id)]
			
			# Проверка и удаление str(interaction.user.id), если str(interaction.guild.id) стал пустым
			if not custom_users[str(interaction.user.id)]:
				del custom_users[str(interaction.user.id)]
			
			with open("./.db/crossplatform/custom/users.json", "w", encoding="utf-8") as write_file: json.dump(custom_users, write_file, ensure_ascii=False, indent=4)
		except KeyError:
			pass
	
	@app_commands.command(
		name = "set",
		description = 'Добавить информацию для своей биографии'
	)
	async def set(self, interaction: discord.Interaction, *, about: str = None, age: int = None, city: str = None, vk: str = None, tg: str = None):
		try:
			if about:
				self.set_biography_param(interaction, "about", about)
			if age:
				self.set_biography_param(interaction, "age", age)
			if city:
				self.set_biography_param(interaction, "city", city)
			if vk:
				self.set_biography_param(interaction, "vk", vk)
			if tg:
				self.set_biography_param(interaction, "tg", tg)
			emb = discord.Embed(
				title = "Успешно",
				description = f"Вы изменили свои данные в биографии:\n" + '\n'.join([
					f"**О себе:** {cspl_get_param(interaction, 'u', 'about', 'biography', interaction.user)}" if cspl_get_param(interaction, 'u', 'about', 'biography', interaction.user) else "**О себе:** `нету`",
					f"**Возраст:** {cspl_get_param(interaction, 'u', 'age', 'biography', interaction.user)}" if cspl_get_param(interaction, 'u', 'age', 'biography', interaction.user) else "**Возраст:** `нету`",
					f"**Город:** {cspl_get_param(interaction, 'u', 'city', 'biography', interaction.user)}" if cspl_get_param(interaction, 'u', 'city', 'biography', interaction.user) else "**Город:** `нету`",
					f"**VK:** {cspl_get_param(interaction, 'u', 'vk', 'biography', interaction.user)}" if cspl_get_param(interaction, 'u', 'vk', 'biography', interaction.user) else "**VK:** `нету`",
					f"**TG:** {cspl_get_param(interaction, 'u', 'tg', 'biography', interaction.user)}" if cspl_get_param(interaction, 'u', 'tg', 'biography', interaction.user) else "**TG:** `нету`",
				]),
				color=discord.Color.green()
			)
			await interaction.response.send_message(embed = emb, ephemeral = True)
			#await interaction.response.send_message(f"```json\n{cspl_custom_users(interaction)[str(interaction.user.id)][str(interaction.guild.id)]['biography']}\n```", embed = emb, ephemeral = True)
		except Exception as e:
			print(repr(e))
	
	@app_commands.command(
		name = "del",
		description = 'Удалить информацию из своей биографии'
	)
	@app_commands.choices(parameter = [
		app_commands.Choice(name = 'about', value = 1),
		app_commands.Choice(name = 'age', value = 2),
		app_commands.Choice(name = 'city', value = 3),
		app_commands.Choice(name = 'vk', value = 4),
		app_commands.Choice(name = 'tg', value = 5),
		app_commands.Choice(name = 'all', value = 6)
	])
	async def delete(self, interaction: discord.Interaction, parameter: app_commands.Choice[int]):
		try:
			if parameter.name == 'about':
				await self.del_biography_param(interaction, "about")
			if parameter.name == 'age':
				await self.del_biography_param(interaction, "age")
			if parameter.name == 'city':
				await self.del_biography_param(interaction, "city")
			if parameter.name == 'vk':
				await self.del_biography_param(interaction, "vk")
			if parameter.name == 'tg':
				await self.del_biography_param(interaction, "tg")
			if parameter.name == 'all':
				await self.del_biography_param(interaction, "about", True)
				await self.del_biography_param(interaction, "age", True)
				await self.del_biography_param(interaction, "city", True)
				await self.del_biography_param(interaction, "vk", True)
				await self.del_biography_param(interaction, "tg", True)
			
			if self.stop:
				return
			emb = discord.Embed(
				title = "Успешно",
				description = f"Вы удалили свои данные из биографии:\n" + '\n'.join([
					f"**О себе:** {cspl_get_param(interaction, 'u', 'about', 'biography', interaction.user)}" if cspl_get_param(interaction, 'u', 'about', 'biography', interaction.user) else "**О себе:** `нету`",
					f"**Возраст:** {cspl_get_param(interaction, 'u', 'age', 'biography', interaction.user)}" if cspl_get_param(interaction, 'u', 'age', 'biography', interaction.user) else "**Возраст:** `нету`",
					f"**Город:** {cspl_get_param(interaction, 'u', 'city', 'biography', interaction.user)}" if cspl_get_param(interaction, 'u', 'city', 'biography', interaction.user) else "**Город:** `нету`",
					f"**VK:** {cspl_get_param(interaction, 'u', 'vk', 'biography', interaction.user)}" if cspl_get_param(interaction, 'u', 'vk', 'biography', interaction.user) else "**VK:** `нету`",
					f"**TG:** {cspl_get_param(interaction, 'u', 'tg', 'biography', interaction.user)}" if cspl_get_param(interaction, 'u', 'tg', 'biography', interaction.user) else "**TG:** `нету`",
				]),
				color=discord.Color.green()
			)
			await interaction.response.send_message(embed = emb, ephemeral = True)
		except Exception as e:
			print(repr(e))

class Settings(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.biography_commands = Biography(bot)
	
	class ChoiceModules(enum.Enum):
		module_info = 1
		module_fun = 2
		module_settings = 3
		module_moderation = 4
		module_economy = 5
		module_audit = 6
		module_music = 7

	@app_commands.command(
		name = "switch",
		description = "Изменить состояние переключателей настроек бота"
	)
	@app_commands.checks.has_permissions(administrator = True)
	@app_commands.default_permissions(administrator = True)
	async def switch(self, interaction: discord.Interaction, on: ChoiceModules = None, off: ChoiceModules = None):
		await interaction.response.send_message("Скоро...", ephemeral=True)
	
	
	async def setup_biography_commands(self):
		await self.bot.add_cog(self.biography_commands)


async def setup(bot):
	settings = Settings(bot)
	await settings.setup_biography_commands()
	await bot.add_cog(settings)