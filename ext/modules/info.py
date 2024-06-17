import discord
from discord.ext import commands
from discord import app_commands
import yaml

import datetime, time
import locale
from typing import Any, Dict, Generic, List, TYPE_CHECKING, Optional, TypeVar, Union
from time import *
import requests
from bs4 import BeautifulSoup

from botConfig import *
from datetime import *
from dbVars import *
from botFunctions import *
import botConfig

locale.setlocale(
    category=locale.LC_ALL,
    locale="Russian"  # Note: do not use "de_DE" as it doesn't work
)

class CmdHelp_CategoryList(discord.ui.View):
	def __init__(self, bot: commands.Bot):
		super().__init__()
		self.bot = bot
	
	@discord.ui.select(placeholder="Выберите категорию...", options= [
		discord.SelectOption(label = "Информация", value = 1),
		discord.SelectOption(label = "Веселье", value = 2),
		discord.SelectOption(label = "Настройки", value = 3),
		discord.SelectOption(label = "Модерация", value = 4)
	])
	async def select_category(self, interaction: discord.Interaction, select: discord.ui.Select):
		try:
			list_cmds_info = [
				{'command': '</help:1250144368837529692>',              'permission': None,
	 			'desc': 'Получить информацию о командах бота'},
				{'command': '</ping:1249321143983145034>',              'permission': None,
	 			'desc': 'Узнать время отклика бота'},
				{'command': '</about:1250159784683114496>',             'permission': None,
	 			'desc': 'Получить информацию о боте'},
				{'command': '</serverinfo:1250362239341301760>',        'permission': None,
	 			'desc': 'Получить информацию о сервере'},
				{'command': '</member:1251828637473439765>',        'permission': None,
	 			'desc': 'Показать информацию об участнике'},
				{'command': '</avatar:1249321144469950546>',            'permission': None,
	 			'desc': 'Получить аватарку юзера'},
				{'command': '</myowner:1250743777077755915>',           'permission': None,
	 			'desc': 'А сейчас о моем разработчике))'},
			]
			list_cmds_fun = [
				{'command': '</time:1250150935280357376>',              'permission': None,
	 			'desc': 'Узнать время'},
				{'command': '</fact:1250150935280357377>',              'permission': None,
	 			'desc': 'Рандомный факт'},
				{'command': '</battle:1250720060344107019>',            'permission': None,
	 			'desc': 'У кого сильнее удача?'},
				{'command': '</opinion:1251281683001643139>',           'permission': None,
	 			'desc': 'Мнение бота о чем-либо'}
			]
			list_cmds_settings = [
				{'command': '</biography set:1251828637473439767>', 'permission': None,
	 			'desc': 'Добавить информацию для своей биографии'},
				{'command': '</biography del:1251828637473439767>', 'permission': None,
	 			'desc': 'Удалить информацию из своей биографии'},
				{'command': '</switch:1251498351816478760>',  'permission': interaction.user.guild_permissions.administrator,
	 			'desc': 'Изменить состояние переключателей настроек бота'},
			]
			list_cmds_moderation = [
				{'command': '</timeout:1251267335613059296>',           'permission': interaction.user.guild_permissions.mute_members,
	 			'desc': 'Временная блокировка разрешений писать/подключаться в чат/войс'},
				{'command': '</untimeout:1251267335613059297>',         'permission': interaction.user.guild_permissions.mute_members,
	 			'desc': 'Отменить блокировку разрешений писать/подключаться в чат/войс'},
				 {'command': '</mute:1251497656266526730>',           'permission': interaction.user.guild_permissions.mute_members,
	 			'desc': 'Замутить юзера'},
				{'command': '</unmute:1251497656266526731>',         'permission': interaction.user.guild_permissions.mute_members,
	 			'desc': 'Размьютить юзера'},
				{'command': '</ban:1250456425742995457>',               'permission': interaction.user.guild_permissions.ban_members,
	 			'desc': 'Забанить юзера'}
			]

			filtered_list_cmds_info = []
			filtered_list_cmds_fun = []
			filtered_list_cmds_settings = []
			filtered_list_cmds_moderation = []
			for cmd in list_cmds_info:
				if bool(cmd['permission']) or cmd['permission'] is None:
					filtered_list_cmds_info.append(cmd)
			for cmd in list_cmds_fun:
				if bool(cmd['permission']) or cmd['permission'] is None:
					filtered_list_cmds_fun.append(cmd)
			for cmd in list_cmds_settings:
				if bool(cmd['permission']) or cmd['permission'] is None:
					filtered_list_cmds_settings.append(cmd)
			for cmd in list_cmds_moderation:
				if bool(cmd['permission']) or cmd['permission'] is None:
					filtered_list_cmds_moderation.append(cmd)

			if select.values[0] == '1':
				emb = discord.Embed(
					title = f"Доступные команды ({len(filtered_list_cmds_info)})",
					description = '\n'.join([
						f"{cmd['command']} — {cmd['desc']}" for cmd in filtered_list_cmds_info
					])
				)
				emb.set_footer(text = "Категория: Информация")
			if select.values[0] == '2':
				emb = discord.Embed(
					title = f"Доступные команды ({len(filtered_list_cmds_fun)})",
					description = '\n'.join([
						f"{cmd['command']} — {cmd['desc']}" for cmd in filtered_list_cmds_fun
					])
				)
				emb.set_footer(text = "Категория: Веселье")
			if select.values[0] == '3':
				emb = discord.Embed(
					title = f"Доступные команды ({len(filtered_list_cmds_settings)})",
					description = '\n'.join([
						f"{cmd['command']} — {cmd['desc']}" for cmd in filtered_list_cmds_settings
					])
				)
				emb.set_footer(text = "Категория: Настройки")
			if select.values[0] == '4':
				emb = discord.Embed(
					title = f"Доступные команды ({len(filtered_list_cmds_moderation)})",
					description = '\n'.join([
						f"{cmd['command']} — {cmd['desc']}" for cmd in filtered_list_cmds_moderation
					])
				)
				emb.set_footer(text = "Категория: Модерация")
			emb.color = 0x2b2d31
			emb.set_thumbnail(url = self.bot.user.avatar)
			await interaction.response.send_message(embed = emb, ephemeral = True)
		except Exception as e:
			await interaction.response.send_message(repr(e))

class Info(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
	
	@app_commands.command(
		name = "help",
		description = "Получить информацию о командах бота",
	)
	@app_commands.choices(
		command = [
			app_commands.Choice(name = "help", value = 1),
			app_commands.Choice(name = "about", value = 2),
			app_commands.Choice(name = "serverinfo", value = 3),
		]
	)
	async def help(self, interaction: discord.Interaction, command: app_commands.Choice[int] = None):
		try:
			if command == None:
				list_cmds_info = [
					{'command': '</help:1250144368837529692>',              'permission': None,
					'desc': 'Получить информацию о командах бота'},
					{'command': '</ping:1249321143983145034>',              'permission': None,
					'desc': 'Узнать время отклика бота'},
					{'command': '</about:1250159784683114496>',             'permission': None,
					'desc': 'Получить информацию о боте'},
					{'command': '</serverinfo:1250362239341301760>',        'permission': None,
					'desc': 'Получить информацию о сервере'},
					{'command': '</member:1251828637473439765>',        'permission': None,
					'desc': 'Показать информацию об участнике'},
					{'command': '</avatar:1249321144469950546>',            'permission': None,
					'desc': 'Получить аватарку юзера'},
					{'command': '</myowner:1250743777077755915>',           'permission': None,
					'desc': 'А сейчас о моем разработчике))'},
				]
				list_cmds_fun = [
					{'command': '</time:1250150935280357376>',              'permission': None,
					'desc': 'Узнать время'},
					{'command': '</fact:1250150935280357377>',              'permission': None,
					'desc': 'Рандомный факт'},
					{'command': '</battle:1250720060344107019>',            'permission': None,
					'desc': 'У кого сильнее удача?'},
					{'command': '</opinion:1251281683001643139>',           'permission': None,
					'desc': 'Мнение бота о чем-либо'}
				]
				list_cmds_settings = [
					{'command': '</biography set:1251828637473439767>', 'permission': None,
					'desc': 'Добавить информацию для своей биографии'},
					{'command': '</biography del:1251828637473439767>', 'permission': None,
					'desc': 'Удалить информацию из своей биографии'},
					{'command': '</switch:1251498351816478760>',  'permission': interaction.user.guild_permissions.administrator,
					'desc': 'Изменить состояние переключателей настроек бота'},
				]
				list_cmds_moderation = [
					{'command': '</timeout:1251267335613059296>',           'permission': interaction.user.guild_permissions.mute_members,
					'desc': 'Временная блокировка разрешений писать/подключаться в чат/войс'},
					{'command': '</untimeout:1251267335613059297>',         'permission': interaction.user.guild_permissions.mute_members,
					'desc': 'Отменить блокировку разрешений писать/подключаться в чат/войс'},
					{'command': '</mute:1251497656266526730>',           'permission': interaction.user.guild_permissions.mute_members,
					'desc': 'Замутить юзера'},
					{'command': '</unmute:1251497656266526731>',         'permission': interaction.user.guild_permissions.mute_members,
					'desc': 'Размьютить юзера'},
					{'command': '</ban:1250456425742995457>',               'permission': interaction.user.guild_permissions.ban_members,
					'desc': 'Забанить юзера'}
				]

				"""
				filtered_list_cmds_info = [cmd for cmd in list_cmds_info if cmd['permission'] is None or getattr(interaction.user.guild_permissions, str(cmd['permission']))]
				filtered_list_cmds_fun = [cmd for cmd in list_cmds_fun if cmd['permission'] is None or getattr(interaction.user.guild_permissions, str(cmd['permission']))]
				filtered_list_cmds_settings = [cmd for cmd in list_cmds_settings if cmd['permission'] is None or getattr(interaction.user.guild_permissions, str(cmd['permission']))]
				filtered_list_cmds_moderation = [cmd for cmd in list_cmds_moderation if cmd['permission'] is None or getattr(interaction.user.guild_permissions, str(cmd['permission']))]
				"""
				# исправленный парс доступных команд
				filtered_list_cmds_info = []
				filtered_list_cmds_fun = []
				filtered_list_cmds_settings = []
				filtered_list_cmds_moderation = []
				for cmd in list_cmds_info:
					if bool(cmd['permission']) or cmd['permission'] is None:
						filtered_list_cmds_info.append(cmd)
				for cmd in list_cmds_fun:
					if bool(cmd['permission']) or cmd['permission'] is None:
						filtered_list_cmds_fun.append(cmd)
				for cmd in list_cmds_settings:
					if bool(cmd['permission']) or cmd['permission'] is None:
						filtered_list_cmds_settings.append(cmd)
				for cmd in list_cmds_moderation:
					if bool(cmd['permission']) or cmd['permission'] is None:
						filtered_list_cmds_moderation.append(cmd)
				
			

				lists_len = len(filtered_list_cmds_info) + len(filtered_list_cmds_fun) + len(filtered_list_cmds_settings) + len(filtered_list_cmds_moderation)
				emb = discord.Embed(
					title = f"Доступные техники ({lists_len})",
					description = '\n'.join([
						#"Есть сложности использования моих техник? Не расстраивайся, постарайся все запомнить.",
						#"Все мои техники начинаются с `/` (потому что используются слеш-техники).",
						#"Я разделил свои команды на несколько модулей, чтобы твоя бошка тыквенная не сдохла от моей гениальности :)))"
					]),
					color = 0x2b2d31
				)
				emb.add_field(
					name = f'Информация [{len(filtered_list_cmds_info)}]', 
					value = ' '.join([cmd['command'] for cmd in filtered_list_cmds_info]),
					inline = False
				)
				emb.add_field(
					name = f'Веселье [{len(filtered_list_cmds_fun)}]', 
					value = ' '.join([cmd['command'] for cmd in filtered_list_cmds_fun]),
					inline = False
				)
				emb.add_field(
					name = f'<:UtilitySettings:1250376547958001734> Настройки [{len(filtered_list_cmds_settings)}]',
					value=' '.join([cmd['command'] for cmd in filtered_list_cmds_settings]),
					inline = False
				)
				if len(filtered_list_cmds_moderation) > 0:
					emb.add_field(
						name=f'<:Mod_Shield:1142795808945745970> Модерация [{len(filtered_list_cmds_moderation)}]',
						value=' '.join([cmd['command'] for cmd in filtered_list_cmds_moderation]),
						inline = False
					)
				emb.set_thumbnail(url = self.bot.user.avatar)
				iam = self.bot.get_user(980175834373562439)
				#emb.set_footer(text = "dev: Sectormain, 2024", icon_url = iam.avatar)
				emb.set_footer(text = "creators: Sectormain, minus7yingzi | 2024")
				await interaction.response.send_message(embed = emb, ephemeral = True, view = CmdHelp_CategoryList(self.bot))
			elif command.name:
				self.text_footer = False
				with open(f"./.db/docs/commands/{command.name}.yml", encoding="utf-8") as read_file: cmd = yaml.safe_load(read_file)
				
				if "describe" in cmd:
					keys = list(cmd["describe"].keys())
					text = ' '.join(keys)
					def add_color_markers(text):
						words = text.split()  # Разделяем текст на отдельные слова
						result = ""
						for word in words:
							if word.endswith("!"):
								# Если слово заканчивается "*", добавляем закрашивающие маркеры
								result += "\u001b[0;31m" + word + "\u001b[0;0m" + " "
								self.text_footer = True
							else:
								result += word + " "
						return result.strip()  # Удаляем лишний пробел в конце строки
					formatted_text = add_color_markers(text)
				else:
					formatted_text = ""
				emb = discord.Embed(title = f'Команда: {command.name}', color = 0x2b2d31)
				emb.add_field(
					name = "Информация",
					value = cmd["description"],
					inline=False
				)
				if "prefix" in cmd["type"]:
					pattern_value = f'\n```ansi\n{cspl_get_param(interaction, "g", "prefix")}{command.name} {formatted_text}\n```'
				elif "hybrid" in cmd["type"]:
					pattern_value = '\n'.join([
						f'\n```ansi\n/{command.name} {formatted_text}',
						f'{cspl_get_param(interaction, "g", "prefix")}{command.name} {formatted_text}\n```'
					])
				else:
					pattern_value = f'\n```ansi\n/{command.name} {formatted_text}\n```'
				emb.add_field(
					name = "Паттерн",
					value = pattern_value,
					inline=False
				)
				if "describe" in cmd: emb.add_field(
					name = "Параметры",
					value = "\n".join([f"`{key}` — {value}" for key, value in cmd["describe"].items()]),
					inline=False
				)
				if self.text_footer: emb.set_footer(text = "! — обязательный параметр")
				await interaction.response.send_message(embed = emb, ephemeral = False)
			else:
				return await interaction.response.send_message("Команда не найдена.", ephemeral = True)
		except Exception as e:
			await interaction.response.send_message(f'||{e}||')
	
	@app_commands.command(
		name = 'ping',
		description = 'Узнать время отклика бота'
	)
	async def ping(self, interaction: discord.Interaction):
		try:
			await interaction.response.defer(ephemeral = False, thinking = True)

			ping = self.bot.latency
			ping_emoji = '🟩 🔳 🔳 🔳 🔳'

			if ping > 0.10000000000000000:
				ping_emoji = '🟧 🟩 🔳 🔳 🔳'

			if ping > 0.15000000000000000:
				ping_emoji = '🟥 🟧 🟩 🔳 🔳'

			if ping > 0.20000000000000000:
				ping_emoji = '🟥 🟥 🟧 🟩 🔳'

			if ping > 0.25000000000000000:
				ping_emoji = '🟥 🟥 🟥 🟧 🟩'

			if ping > 0.30000000000000000:
				ping_emoji = '🟥 🟥 🟥 🟥 🟧'

			if ping > 0.35000000000000000:
				ping_emoji = '🟥 🟥 🟥 🟥 🟥'

			# Переменная с пингом бота до текущего шарда
			shard_ping = f'{ping_emoji}  `{round(self.bot.latency * 1000)}ms`'

			message = await interaction.edit_original_response(content = 'Отбиваю...  \n🔳🔳🔳🔳🔳 `секунду...`')
			await message.edit(content = f'Понг! 🏓  \n{shard_ping}')
		except Exception as e:
			await interaction.edit_original_response(content = e)
	
	
	# Получить детальную информацию о боте
	@app_commands.command(
		name = "about",
		description = 'Получить информацию о боте'
	)
	async def about(self, interaction: discord.Interaction):
		try:
			guilds = 0
			for guild in self.bot.guilds:
				guilds += 1

			members = len(list(self.bot.get_all_members()))

			emb = discord.Embed(color=0x2b2d31)
			#emb.set_author(name = f'{self.bot.user} | ID: {self.bot.user.id}', icon_url = self.bot.user.avatar)
			
			creators = '\n'.join([
				f'<@{creator}>' for creator in sf_c()
			])
			#emb.add_field(name = 'Разработчик', value = f'<@980175834373562439>', inline=True)
			emb.add_field(name = 'Создатели', value = creators, inline=True)
			emb.add_field(name = 'Серверы', value = f'{str(guilds)}', inline=True)
			emb.add_field(name = 'Юзеры', value = f'{members}', inline=True)

			emb.add_field(name = 'Библиотека', value = f'discord.py {discord.__version__}', inline=True)

			emb.add_field(name = 'Версия', value = f"v{botConfig.version['number']}", inline=True)

			ping = self.bot.latency
			ping_emoji = '🟩 🔳 🔳 🔳 🔳'

			if ping > 0.10000000000000000:
				ping_emoji = '🟧 🟩 🔳 🔳 🔳'

			if ping > 0.15000000000000000:
				ping_emoji = '🟥 🟧 🟩 🔳 🔳'

			if ping > 0.20000000000000000:
				ping_emoji = '🟥 🟥 🟧 🟩 🔳'

			if ping > 0.25000000000000000:
				ping_emoji = '🟥 🟥 🟥 🟧 🟩'

			if ping > 0.30000000000000000:
				ping_emoji = '🟥 🟥 🟥 🟥 🟧'

			if ping > 0.35000000000000000:
				ping_emoji = '🟥 🟥 🟥 🟥 🟥'

			# Переменная с пингом бота до текущего шарда
			shard_id = interaction.guild.shard_id
			shard = self.bot.get_shard(shard_id)
			shard_ping = f'{ping_emoji}  `{round(shard.latency * 1000)}ms`'
			bot_shard_name = lambda: yaml.safe_load(open('./.db/bot/shards.yml', 'r', encoding='utf-8'))[shard_id]

			emb.add_field(name = 'Шард', value = f"{bot_shard_name()}#{shard.id}", inline = True)
			emb.add_field(name = 'Пинг', value = shard_ping, inline = True)
		
			def choose_correct_word(number, form1, form2, form3):
				if 10 <= number % 100 <= 20:
					return form3
				elif number % 10 == 1:
					return form1
				elif 2 <= number % 10 <= 4:
					return form2
				else:
					return form3
			
			TimeFromStart = datetime.now() - start_time
			if TimeFromStart.days > 0:
				days = TimeFromStart.days
				time_str = f"{days} {choose_correct_word(days, 'день', 'дня', 'дней')}, {TimeFromStart.seconds // 3600} {choose_correct_word(TimeFromStart.seconds // 3600, 'час', 'часа', 'часов')}, {(TimeFromStart.seconds % 3600) // 60} {choose_correct_word((TimeFromStart.seconds % 3600) // 60, 'минута', 'минуты', 'минут')}, {TimeFromStart.seconds % 60} {choose_correct_word(TimeFromStart.seconds % 60, 'секунда', 'секунды', 'секунд')}"
			elif TimeFromStart.seconds >= 3600:
				time_str = f"{TimeFromStart.seconds // 3600} {choose_correct_word(TimeFromStart.seconds // 3600, 'час', 'часа', 'часов')}, {(TimeFromStart.seconds % 3600) // 60} {choose_correct_word((TimeFromStart.seconds % 3600) // 60, 'минута', 'минуты', 'минут')}, {TimeFromStart.seconds % 60} {choose_correct_word(TimeFromStart.seconds % 60, 'секунда', 'секунды', 'секунд')}"
			elif TimeFromStart.seconds >= 60:
				time_str = f"{(TimeFromStart.seconds % 3600) // 60} {choose_correct_word((TimeFromStart.seconds % 3600) // 60, 'минута', 'минуты', 'минут')}, {TimeFromStart.seconds % 60} {choose_correct_word(TimeFromStart.seconds % 60, 'секунда', 'секунды', 'секунд')}"
			else:
				time_str = f"{TimeFromStart.seconds} {choose_correct_word(TimeFromStart.seconds, 'секунда', 'секунды', 'секунд')}"

			emb.set_footer(text=f"{self.bot.user} | Время работы: {time_str}", icon_url=self.bot.user.avatar)
			
			emb.set_image(url = 'https://cdn.discordapp.com/attachments/817116435351863306/1250518361457033258/Sukuna_Ryoumen.jpg?ex=666b3b7a&is=6669e9fa&hm=b3cf1b6e92845d648199e515f84c8bef311e517aaed68298519f48d905d1e72f&')

			await interaction.response.send_message(embed = emb)
		except Exception as e:
			print(e)
	
	@app_commands.command(
		name = "serverinfo",
		description="Получить информацию о сервере"
	)
	async def serverinfo(self, interaction: discord.Interaction):
		try:
			await interaction.response.send_message('скоро', ephemeral=True)
		except Exception as e:
			await interaction.response.send_message(repr(e))
	
	@app_commands.command(
		name = "member",
		description = 'Показать информацию об участнике'
	)
	async def member(self, interaction: discord.Interaction, member: discord.Member = None):
		try:
			user = interaction.user if not member else member
			roles = user.roles

			role_list = ''
			role_list_number = 0
			for role in reversed(roles):
				if role != interaction.guild.default_role:
					role_list += f'<@&{role.id}> '
					role_list_number += 1
			
			emb = discord.Embed(colour = 0x2b2d31)
			emb.set_author(name = f'{user}', icon_url = user.avatar)
			emb.set_thumbnail(url = user.avatar)
			if user != self.bot.user:
				bio_list = []
				if cspl_get_param(interaction, 'u', 'about', 'biography', user if user else None):
					bio_list.append(f"**О себе:** {cspl_get_param(interaction, 'u', 'about', 'biography', user if user else None)}")
				if cspl_get_param(interaction, 'u', 'age', 'biography', user if user else None):
					bio_list.append(f"**Возраст:** {cspl_get_param(interaction, 'u', 'age', 'biography', user if user else None)}")
				if cspl_get_param(interaction, 'u', 'city', 'biography', user if user else None):
					bio_list.append(f"**Город:** {cspl_get_param(interaction, 'u', 'city', 'biography', user if user else None)}")
				if cspl_get_param(interaction, 'u', 'vk', 'biography', user if user else None):
					bio_list.append(f"**VK:** {cspl_get_param(interaction, 'u', 'vk', 'biography', user if user else None)}")
				if cspl_get_param(interaction, 'u', 'tg', 'biography', user if user else None):
					bio_list.append(f"**TG:** {cspl_get_param(interaction, 'u', 'tg', 'biography', user if user else None)}")
				if len(bio_list) > 0:
					emb.add_field(name = 'Биография', value = '\n'.join(bio_list), inline = False)
				else:
					if interaction.user == member or not member:
						emb.description = "Создайте свою биографию с помощью команды </biography set:1251828637473439767>"
			else:
				emb.add_field(name = 'Биография', value = '\n'.join([
					f"**О себе:** 3990см хуй блять нахуй",
					f"**Возраст:** 2000+",
					f"**Город:** Залупа",
				]), inline = False)
			#emb.add_field(name = 'Статус', value = status)
			emb.add_field(name = f'Роли [{role_list_number}]', value = 'Отсутствуют' if role_list == '' else role_list, inline = False)
			emb.add_field(name = 'В Discord', value = user.created_at.strftime('**Дата:** %d/%m/%Y\n**Время:** %H:%M:%S'))
			emb.add_field(name = 'На сервере', value = user.joined_at.strftime('**Дата:** %d/%m/%Y\n**Время:** %H:%M:%S'))
			emb.set_footer(text = f'ID: {user.id}')
			emb.timestamp = datetime.now()
			if user.id == 980175834373562439:
				#emb.set_image(url = 'https://cdn.discordapp.com/attachments/817116435351863306/1251902055375831080/photo1718438465.jpeg?ex=66704425&is=666ef2a5&hm=6fbe760673a386e62f00964be5c1422cf6df10cb6dd8da2a4cccd37a5d3fbdae&')
				emb.set_image(url = 'https://cdn.discordapp.com/attachments/817116435351863306/1252359093440479242/6dtr5mSE000.png?ex=6671edcb&is=66709c4b&hm=dc6d926cb4f6f737b07031cf64c425eeded60d4295757481bdfcde79d491b344&')
				#emb.set_image(url = 'https://cdn.discordapp.com/attachments/817116435351863306/1221372466350522368/D82A2342.jpg?ex=667142bf&is=666ff13f&hm=7cd87d621f9cb941e5d301b9abbd3f4a914873d9faa9fdad53b731705002bc41&')
				#emb.set_image(url = "attachment://.db/content/owner/wlp1.jpeg")
			else:
				req = await self.bot.http.request(discord.http.Route("GET", f"/users/{user.id}"))
				banner_id = req["banner"]
				if banner_id:
					banner_url = f"https://cdn.discordapp.com/banners/{user.id}/{banner_id}?size=1024"
					emb.set_image(url = banner_url)

			await interaction.response.send_message(embed = emb, ephemeral = False)
		except Exception as e:
			await interaction.response.send_message(repr(e), ephemeral = False)
	
	@app_commands.command(
		name = "avatar",
		description = 'Получить аватарку юзера'
	)
	async def avatar(self, interaction: discord.Interaction, user: discord.Member = None):
		try:
			user = interaction.user if not user else user

			emb = discord.Embed(colour = 0x2b2d31)
			emb.set_author(name = user, icon_url = user.avatar)
			emb.set_image(url = user.avatar)

			await interaction.response.send_message(embed = emb, ephemeral=True)
		except Exception as e:
			await interaction.response.send_message(e, ephemeral=True)
	
	@app_commands.command(
		name = "myowner",
		description="А сейчас о моем разработчике))"
	)
	async def myowner(self, interaction: discord.Interaction):
		try:
			await interaction.response.send_message('скоро', ephemeral=True)
		except Exception as e:
			await interaction.response.send_message(repr(e))

async def setup(bot):
	await bot.add_cog(Info(bot))

"""
shard_id = interaction.guild.shard_id
shard = self.bot.get_shard(shard_id)
shard_ping = shard.latency
shard_servers = len([guild for guild in self.bot.guilds if guild.shard_id == shard_id])
bot_shard_name = lambda: yaml.safe_load(open('./.db/bot/shards.yml', 'r', encoding='utf-8'))[shard_id]
await interaction.response.send_message(f"{bot_shard_name()}#{shard.id}\n{shard_ping}")


def get_member_status(user_id):
	url = f"https://discord.com/api/v9/users/{user_id}"
	headers = {
		"Authorization": botConfig.token
	}
	response = requests.get(url, headers=headers)
	if response.status_code == 200:
		user_data = response.json()
		return user_data['presence']['status']
	else:
		return None

user_id = user.id
user_status = get_member_status(user_id)

if user_status == discord.Status.online:
	status = '<:online:748149457396433016> В сети'
elif user_status == discord.Status.idle:
	status = '<:idle:748149485707984907> Не активен'
elif user_status == discord.Status.do_not_disturb:
	status = '<a:mark_none:815121643479236618> Не беспокоить'
else:
	status = '<:offline:748149539915038731> Не в сети'
"""