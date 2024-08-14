import discord
from discord.ext import commands
from discord import app_commands

import asyncio
import enum
import re
from dbVars import *
from botFunctions import *
import botDecorators
import botConfig

class Biography(commands.GroupCog, name = "biography"):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		super().__init__()
		self.stop = False
	
	def set_biography_param(self, interaction: discord.Interaction, param: str, content):
		custom_users = json.load(open(botConfig.path_db_cspl_custom_users, "r", encoding="utf-8"))
		if str(interaction.user.id) not in custom_users:
			custom_users[str(interaction.user.id)] = {}
		if str(interaction.guild.id) not in custom_users[str(interaction.user.id)]:
			custom_users[str(interaction.user.id)][str(interaction.guild.id)] = {}

		if "biography" not in custom_users[str(interaction.user.id)][str(interaction.guild.id)]:
			custom_users[str(interaction.user.id)][str(interaction.guild.id)]["biography"] = {}
		custom_users[str(interaction.user.id)][str(interaction.guild.id)]["biography"][param] = str(content)
		with open(botConfig.path_db_cspl_custom_users, "w", encoding="utf-8") as write_file: json.dump(custom_users, write_file, ensure_ascii = False, indent = 4)
		
	async def del_biography_param(self, interaction: discord.Interaction, param: str, all = False):
		try:
			custom_users = json.load(open(botConfig.path_db_cspl_custom_users, "r", encoding="utf-8"))
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
			
			with open(botConfig.path_db_cspl_custom_users, "w", encoding="utf-8") as write_file: json.dump(custom_users, write_file, ensure_ascii=False, indent=4)
		except KeyError:
			pass
	
	@app_commands.command(
		name = "set",
		description = 'Добавить информацию для своей биографии'
	)
	@botDecorators.check_cmd_work()
	async def set(self, interaction: discord.Interaction, *, phrase: str = None, age: int = None, city: str = None, vk: str = None, tg: str = None):
		try:
			await interaction.response.defer(ephemeral = True, thinking = True)

			if phrase:
				self.set_biography_param(interaction, "phrase", phrase)
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
					f"**О себе:** {cspl_get_param(interaction, 'u', 'phrase', ['biography'])}" if cspl_get_param(interaction, 'u', 'phrase', ['biography']) else "**О себе:** `нету`",
					f"**Возраст:** {cspl_get_param(interaction, 'u', 'age', ['biography'])}" if cspl_get_param(interaction, 'u', 'age', ['biography']) else "**Возраст:** `нету`",
					f"**Город:** {cspl_get_param(interaction, 'u', 'city', ['biography'])}" if cspl_get_param(interaction, 'u', 'city', ['biography']) else "**Город:** `нету`",
					f"**VK:** {cspl_get_param(interaction, 'u', 'vk', ['biography'])}" if cspl_get_param(interaction, 'u', 'vk', ['biography']) else "**VK:** `нету`",
					f"**TG:** {cspl_get_param(interaction, 'u', 'tg', ['biography'])}" if cspl_get_param(interaction, 'u', 'tg', ['biography']) else "**TG:** `нету`",
				]),
				color=discord.Color.green()
			)
			await interaction.edit_original_response(embed = emb)
		except Exception as e:
			print(repr(e))
	
	@app_commands.command(
		name = "del",
		description = 'Удалить информацию из своей биографии'
	)
	@app_commands.choices(parameter = [
		app_commands.Choice(name = 'phrase', value = 1),
		app_commands.Choice(name = 'age', value = 2),
		app_commands.Choice(name = 'city', value = 3),
		app_commands.Choice(name = 'vk', value = 4),
		app_commands.Choice(name = 'tg', value = 5),
		app_commands.Choice(name = 'all', value = 6)
	])
	@botDecorators.check_cmd_work()
	async def delete(self, interaction: discord.Interaction, parameter: app_commands.Choice[int]):
		try:
			if parameter.name == 'phrase':
				await self.del_biography_param(interaction, "phrase")
			if parameter.name == 'age':
				await self.del_biography_param(interaction, "age")
			if parameter.name == 'city':
				await self.del_biography_param(interaction, "city")
			if parameter.name == 'vk':
				await self.del_biography_param(interaction, "vk")
			if parameter.name == 'tg':
				await self.del_biography_param(interaction, "tg")
			if parameter.name == 'all':
				await self.del_biography_param(interaction, "phrase", True)
				await self.del_biography_param(interaction, "age", True)
				await self.del_biography_param(interaction, "city", True)
				await self.del_biography_param(interaction, "vk", True)
				await self.del_biography_param(interaction, "tg", True)
			
			if self.stop:
				return
			emb = discord.Embed(
				title = "Успешно",
				description = f"Вы удалили свои данные из биографии:\n" + '\n'.join([
					f"**О себе:** {cspl_get_param(interaction, 'u', 'phrase', ['biography'], interaction.user)}" if cspl_get_param(interaction, 'u', 'phrase', ['biography'], interaction.user) else "**О себе:** `нету`",
					f"**Возраст:** {cspl_get_param(interaction, 'u', 'age', ['biography'], interaction.user)}" if cspl_get_param(interaction, 'u', 'age', ['biography'], interaction.user) else "**Возраст:** `нету`",
					f"**Город:** {cspl_get_param(interaction, 'u', 'city', ['biography'], interaction.user)}" if cspl_get_param(interaction, 'u', 'city', ['biography'], interaction.user) else "**Город:** `нету`",
					f"**VK:** {cspl_get_param(interaction, 'u', 'vk', ['biography'], interaction.user)}" if cspl_get_param(interaction, 'u', 'vk', ['biography'], interaction.user) else "**VK:** `нету`",
					f"**TG:** {cspl_get_param(interaction, 'u', 'tg', ['biography'], interaction.user)}" if cspl_get_param(interaction, 'u', 'tg', ['biography'], interaction.user) else "**TG:** `нету`",
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
	
	class SwitchChoice(enum.Enum):
		module_info = {'name': 'module_info', 'param': 'status', 'path': ['modules', 'info']}
		module_fun = {'name': 'module_fun', 'param': 'status', 'path': ['modules', 'fun']}
		module_settings = {'name': 'module_settings', 'param': 'status', 'path': ['modules', 'settings']}
		module_moderation = {'name': 'module_moderation', 'param': 'status', 'path': ['modules', 'moderation']}
		module_economy = {'name': 'module_economy', 'param': 'status', 'path': ['modules', 'economy']}
		module_audit = {'name': 'module_audit', 'param': 'status', 'path': ['modules', 'audit']}

		command_help = {'name': 'command_help', 'param': 'status', 'path': ['modules', 'info', 'commands', 'help']}
		command_ping = {'name': 'command_ping', 'param': 'status', 'path': ['modules', 'info', 'commands', 'ping']}
		command_dashboard = {'name': 'command_dashboard', 'param': 'status', 'path': ['modules', 'info', 'commands', 'dashboard']}
		command_about = {'name': 'command_about', 'param': 'status', 'path': ['modules', 'info', 'commands', 'about']}
		command_serverinfo = {'name': 'command_serverinfo', 'param': 'status', 'path': ['modules', 'info', 'commands', 'serverinfo']}
		command_member = {'name': 'command_member', 'param': 'status', 'path': ['modules', 'info', 'commands', 'member']}
		command_avatar = {'name': 'command_avatar', 'param': 'status', 'path': ['modules', 'info', 'commands', 'avatar']}
		command_dev = {'name': 'command_avatar', 'param': 'status', 'path': ['modules', 'info', 'commands', 'dev']}

		command_time = {'name': 'command_time', 'param': 'status', 'path': ['modules', 'fun', 'commands', 'time']}
		command_battle = {'name': 'command_battle', 'param': 'status', 'path': ['modules', 'fun', 'commands', 'battle']}
		command_opinion = {'name': 'command_opinion', 'param': 'status', 'path': ['modules', 'fun', 'commands', 'opinion']}

		command_switch = {'name': 'command_switch', 'param': 'status', 'path': ['modules', 'settings', 'commands', 'switch']}
		command_set = {'name': 'command_biography set', 'param': 'status', 'path': ['modules', 'settings', 'commands', 'set']}
		command_del = {'name': 'command_biography del', 'param': 'status', 'path': ['modules', 'settings', 'commands', 'del']}

		command_mute = {'name': 'command_mute', 'param': 'status', 'path': ['modules', 'moderation', 'commands', 'mute']}
		command_unmute = {'name': 'command_unmute', 'param': 'status', 'path': ['modules', 'moderation', 'commands', 'unmute']}
		command_timeout = {'name': 'command_timeout', 'param': 'status', 'path': ['modules', 'moderation', 'commands', 'timeout']}
		command_untimeout = {'name': 'command_untimeout', 'param': 'status', 'path': ['modules', 'moderation', 'commands', 'untimeout']}
		command_ban = {'name': 'command_ban', 'param': 'status', 'path': ['modules', 'moderation', 'commands', 'ban']}

		event_lvl_system = {'name': 'event_lvl_system', 'param': 'status', 'path': ['modules', 'economy', 'events', 'lvl_system']}

		event_block_badwords = {'name': 'event_block_badwords', 'param': 'status', 'path': ['modules', 'audit', 'events', 'block_badwords']}

	@app_commands.command(
		name = "switch",
		description = "Изменить состояние переключателей настроек бота"
	)
	@app_commands.checks.has_permissions(administrator = True)
	@app_commands.default_permissions(administrator = True)
	@botDecorators.check_cmd_work()
	async def switch(self, interaction: discord.Interaction, on: SwitchChoice = None, off: SwitchChoice = None):
		await interaction.response.defer(ephemeral=True, thinking=True)
		try:
			interaction_txt = ''
			if on:
				if cspl_get_param(interaction, 'g', on.value['param'], on.value['path']):
					return await interaction.edit_original_response(content=f'{on.value['name']} уже включен')
				
				custom_guilds = json.load(open(botConfig.path_db_cspl_custom_guilds, "r", encoding="utf-8"))
				if str(interaction.guild.id) not in custom_guilds:
					custom_guilds[str(interaction.guild.id)] = {}
				if len(on.value['path']) == 2:
					if on.value['path'][0] not in custom_guilds[str(interaction.guild.id)]:
						custom_guilds[str(interaction.guild.id)][on.value['path'][0]] = {}
					if on.value['path'][1] not in custom_guilds[str(interaction.guild.id)][on.value['path'][0]]:
						custom_guilds[str(interaction.guild.id)][on.value['path'][0]][on.value['path'][1]] = {}
					custom_guilds[str(interaction.guild.id)][on.value['path'][0]][on.value['path'][1]][on.value['param']] = True
				with open(botConfig.path_db_cspl_custom_guilds, "w", encoding="utf-8") as write_file: json.dump(custom_guilds, write_file, ensure_ascii=False, indent=4)
				interaction_txt += f'{botConfig.emoji_mark_success} Включен {on.value['name']}'

			if off: 
				interaction_txt += off.value

			await interaction.edit_original_response(content=interaction_txt)
		except Exception as e:
			print(repr(e))
	
	
	async def setup_biography_commands(self):
		await self.bot.add_cog(self.biography_commands)


async def setup(bot):
	settings = Settings(bot)
	await settings.setup_biography_commands()
	await bot.add_cog(settings)


"""
identification_key = f'{interaction.user.id}&{interaction.guild.id}'

single_user = get_single_user(interaction.user.id, interaction.guild.id)

biography = single_user.get('biography', {})

if identification_key == single_user['identification']:
	biography[param] = str(content)  # обновляем локально

	supabase_update_data(
		'crossplatform_custom_users', 
		{'biography': biography},  # сохраняем весь объект JSON
		[('user_id', interaction.user.id), ('guild_id', interaction.guild.id)]
	)
else:
	biography[param] = str(content)  # добавляем новый параметр
	supabase_insert_data(
		'crossplatform_custom_users', 
		{
			'user_id': interaction.user.id, 
			'guild_id': interaction.guild.id, 
			'identification': f'{interaction.user.id}&{interaction.guild.id}', 
			'biography': biography
		}
	)
"""