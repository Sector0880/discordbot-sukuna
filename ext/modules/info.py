import discord
from discord.ext import commands
from discord import app_commands
import yaml

import datetime, time
import locale
from typing import Any, Dict, Generic, List, TYPE_CHECKING, Optional, TypeVar, Union
from time import *
import requests
import enum
from bs4 import BeautifulSoup

from botConfig import *
from datetime import *
from dbVars import *
from botFunctions import *
import botConfig
import botDecorators

def get_items_list(interaction: discord.Interaction, _module, item_type):
	valid_item_types = ['commands', 'events']
	if item_type not in valid_item_types:
		return [{'error': 'Неверный тип элемента', 'desc': 'None'}]

	module = cspl_get_param_with_merge(interaction, 'g', 'modules').get(_module, {})
	if not module:
		return [{'error': f'Не найден список {item_type}', 'desc': 'None'}]

	items = []
	for item_name, item_info in module.get(item_type, {}).items():
		item = {
			'status': item_info['status']
		}
		if item_type == 'commands':
			item['txt'] = item_info.get('txt', 'Без текста') 
			item['desc'] = item_info.get('desc', 'Без описания') 
			item['permission'] = item_info.get('permission', None)
		elif item_type == 'events':
			item['txt'] = item_info.get('txt', 'Без текста') 
			item['desc'] = item_info.get('desc', 'Без описания') 
		items.append(item)

	return items

class CmdHelp_ModuleList(discord.ui.View):
	def __init__(self, bot: commands.Bot):
		super().__init__(timeout=120)
		self.bot = bot
	
	@discord.ui.select(placeholder="Выберите модуль...", options=[
		discord.SelectOption(label="Информация", value="info"),
		discord.SelectOption(label="Веселье", value="fun"),
		discord.SelectOption(label="Настройки", value="settings"),
		discord.SelectOption(label="Модерация", value="moderation"),
		discord.SelectOption(label="Экономика", value="economy"),
		discord.SelectOption(label="Аудит", value="audit")
	])
	async def select_module(self, interaction: discord.Interaction, select: discord.ui.Select):
		try:
			await interaction.response.defer(ephemeral = True, thinking = True)

			modules = cspl_get_param_with_merge(interaction, 'g', 'modules')
			
			selected_category = select.values[0]
			module = modules.get(selected_category, {})

			commands = module.get('commands', {})
			filtered_commands = [
				{'command': cmd_info['txt'], 'desc': cmd_info['desc'], 'status': cmd_info['status']}
				for cmd_info in commands.values()
				if cmd_info['status']
				if not cmd_info.get('permission') or getattr(interaction.user.guild_permissions, cmd_info.get('permission', ''), False)
			]
			
			if not filtered_commands:
				await interaction.edit_original_response(content="Нет доступных команд в этом модуле.")
				return

			emb = discord.Embed(
				title=f"Доступные техники ({len(filtered_commands)})",
				description='\n'.join([f"{cmd['command']} — {cmd['desc']}" for cmd in filtered_commands]),
				color=0x2b2d31
			)
			emb.set_footer(text=f"Модуль: {module['name']}")
			emb.set_thumbnail(url=self.bot.user.avatar)

			await interaction.edit_original_response(embed = emb)
		except discord.InteractionResponded:
			await interaction.edit_original_response(content = "Это взаимодействие устарело. Пожалуйста, повторите команду.")
		except Exception as e:
			await interaction.edit_original_response(content = f"Произошла ошибка: {repr(e)}")

class DashboardBtns(discord.ui.View):
	def __init__(self, bot: commands.Bot):
		super().__init__(timeout=120)
		self.bot = bot
	
	@discord.ui.button(label="Модули", style=discord.ButtonStyle.gray)
	async def modules(self, interaction: discord.Interaction, button: discord.ui.Button):
		try:
			await interaction.response.defer(ephemeral = True, thinking = True)

			emb = discord.Embed()
			
			for module in cspl_get_param_with_merge(interaction, 'g', 'modules'):
				module_cmds = get_items_list(interaction, module, 'commands')
				module_events = get_items_list(interaction, module, 'events')

				module_cmds_str = '\n'.join([
					('<:switch_on:818125506309652490> ' if cmd['status'] and cspl_get_param_with_merge(interaction, 'g', 'status', ['modules', module]) else '<:switch_off:818125535951323177> ') + cmd['txt']
					for cmd in module_cmds
				])

				module_events_str = '\n'.join([
					('<:switch_on:818125506309652490> ' if event['status'] and cspl_get_param_with_merge(interaction, 'g', 'status', ['modules', module]) else '<:switch_off:818125535951323177> ') + event['txt']
					for event in module_events
				])

				try:
					emb.add_field(
						name = ('<:switch_on:818125506309652490> ' if cspl_get_param_with_merge(interaction, 'g', 'status', ['modules', module]) else '<:switch_off:818125535951323177> ') + cspl_get_param_with_merge(interaction, 'g', 'name', ['modules', module]),
						value = module_cmds_str + '\n' + module_events_str
					)
				except Exception:
					pass
			emb.set_thumbnail(url = self.bot.user.avatar)
			emb.set_footer(text = f"/ Панель управления / Модули")

			interaction_txt = '\n'.join([
				"**Включить / Выключить модуль:**  `/switch on:module`  `/switch off:module`",
				"**Включить / Выключить команду:** `/switch on:command` `/switch off:command`",
				"**Включить / Выключить событие:** `/switch on:event`   `/switch off:event`",
			])
			await interaction.edit_original_response(content = interaction_txt, embed = emb)
			#interaction.message.view.stop() должно скрывать кнопку после нажатия но не скрывает
		except discord.InteractionResponded:
			await interaction.edit_original_response(content = "Это взаимодействие устарело. Пожалуйста, повторите команду.")
		except Exception as e:
			await interaction.edit_original_response(content = f"Произошла ошибка: {repr(e)}")
	
	@discord.ui.button(label="Экономика", style=discord.ButtonStyle.gray)
	async def economy(self, interaction: discord.Interaction, button: discord.ui.Button):
		try:
			await interaction.response.defer(ephemeral = True, thinking = True)
			await interaction.edit_original_response(content = "Скоро")
		except discord.InteractionResponded:
			await interaction.edit_original_response("Это взаимодействие устарело. Пожалуйста, повторите команду.")
		except Exception as e:
			await interaction.edit_original_response(f"Произошла ошибка: {repr(e)}")

class Info(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
	
	@app_commands.command(
		name = "help",
		description = "Информация о командах бота",
	)
	@botDecorators.check_cmd_work()
	async def help(self, interaction: discord.Interaction, selected_command: str = None):
		try:
			if selected_command == None:
				modules = cspl_get_param_with_merge(interaction, 'g', 'modules')

				emb = discord.Embed(
					title="Доступные техники",
					description=f"Мои техники начинаются с префикса `/`. Для получения доп. информации по категории выберите её из списка.",
					color=0x2b2d31
				)
				emb.set_thumbnail(url=self.bot.user.avatar)

				total_commands = 0
				for i, module in modules.items():
					module_name = module.get('name', 'Без названия')
					commands = module.get('commands', {})
					filtered_commands = [
						{'command': cmd['txt'], 'desc': cmd['desc'], 'status': cmd['status']}
						for cmd in commands.values()
						if cmd['status']
						if not cmd.get('permission') or getattr(interaction.user.guild_permissions, cmd.get('permission', ''), False)
					]
					if filtered_commands:
						emb.add_field(
							name=f'{module_name} ({len(filtered_commands)})',
							value=' '.join([cmd['command'] for cmd in filtered_commands]),
							inline=False
						)
						total_commands += len(filtered_commands)

				emb.title += f" ({total_commands})"
				iam = self.bot.get_user(980175834373562439)
				emb.set_footer(text="dev: Sectormain, 2024", icon_url=iam.avatar)
				#emb.set_footer(text = "creators: Sectormain, minus7yingzi | 2024")
				await interaction.response.send_message(embed=emb, ephemeral=True, view=CmdHelp_ModuleList(self.bot))
			elif selected_command:
				modules = cspl_get_param_with_merge(interaction, 'g', 'modules')
				selected_command_name = selected_command
				command_info = None
				command_patterns = None

				for category, module in modules.items():
					commands = module.get('commands', {})
					if selected_command_name in commands:
						command_info = commands[selected_command_name]
						break

				if not command_info:
					return await interaction.response.send_message("Команда не найдена.", ephemeral=True)
				
				emb = discord.Embed(title=f'Команда: {command_info["txt"]}', color=0x2b2d31)
				emb.add_field(
					name="Информация",
					value=command_info["desc"],
					inline=False
				)

				if "parameters" in command_info:
					emb.add_field(
						name="Параметры",
						value="\n".join([f"`{key}` — {value}" for key, value in command_info["parameters"].items()]),
						inline=False
					)
				
				exmp_value = ' '.join([f'```ansi\n{exmp}\n```' for exmp in command_info.get("example", {})])
				if len(exmp_value) > 0:
					emb.add_field(
						name="Примеры",
						value=exmp_value,
						inline=False
					)
				await interaction.response.send_message(embed=emb, ephemeral=False)
			else:
				return await interaction.response.send_message("Команда не найдена.", ephemeral = True)
		except Exception as e:
			await interaction.response.send_message(f'||{e}||')
	
	@app_commands.command(
		name = 'ping',
		description = 'Время отклика бота'
	)
	@botDecorators.check_cmd_work()
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
	
	@app_commands.command(
		name = "dashboard",
		description = "Панель управления настройками бота"
	)
	@app_commands.checks.has_permissions(administrator = True)
	@app_commands.default_permissions(administrator = True)
	@botDecorators.check_cmd_work()
	async def dashboard(self, interaction: discord.Interaction):
		try:
			await interaction.response.defer(ephemeral = True, thinking = True)

			modules_on = []
			modules_off = []
			for module in cspl_get_param_with_merge(interaction, 'g', 'modules'):
				if cspl_get_param_with_merge(interaction, 'g', 'status', ['modules', module]):
					modules_on.append(cspl_get_param_with_merge(interaction, 'g', 'name', ['modules', module]))
				else:
					modules_off.append(cspl_get_param_with_merge(interaction, 'g', 'name', ['modules', module]))

			modules_on_str = ', '.join([f'**{module}**' for module in modules_on])
			modules_off_str = ', '.join([f'**{module}**' for module in modules_off])

			emb = discord.Embed(
				title=f"{interaction.guild.name}"
			)
			emb.add_field(
				name = "Модули",
				value = "\n".join([
					'<:switch_on:818125506309652490> ' + modules_on_str,
					'<:switch_off:818125535951323177> ' + modules_off_str
				])
			)


			economy_data = cspl_get_param(interaction, "g", "lvls", ["economy"])
			economy_data.insert(0, cspl_get_param(interaction, "g", "lvlFirst", ["economy"]))
			first_lvl = economy_data[0]['lvl']
			first_lvl_xp = economy_data[0]['xp']
			first_lvl_name = economy_data[0].get('lvlName', False)
			first_lvl_name_text = f' {first_lvl_name}' if first_lvl_name else ''

			last_lvl = economy_data[-1]['lvl']
			last_lvl_xp = economy_data[-1]['xp']
			last_lvl_name = economy_data[-1].get('lvlName', False)
			last_lvl_name_text = f' {last_lvl_name}' if last_lvl_name else ''
			level_range = f'`{first_lvl}{cspl_get_param(interaction, "g", "lvlTxt", ["economy"])[0]}{first_lvl_name_text} ({first_lvl_xp}{cspl_get_param(interaction, "g", "xpTxt", ["economy"])[0]})` → `{last_lvl}{cspl_get_param(interaction, "g", "lvlTxt", ["economy"])[0]}{last_lvl_name_text} ({last_lvl_xp}{cspl_get_param(interaction, "g", "xpTxt", ["economy"])[0]})`'
			
			if cspl_get_param(interaction, 'g', 'status', ['modules', 'economy']) and cspl_get_param(interaction, 'g', 'status', ['modules', 'economy', 'events', 'economy_system']):
				emb.add_field(
					name = "Экономика",
					value = '\n'.join([
						f"**{cspl_get_param(interaction, 'g', 'lvlTxt', ['economy'])[2]}:** {level_range}",
						f'**Награда за сообщение:** `{cspl_get_param(interaction, "g", "xp", ["economy", "msgAward"])}{cspl_get_param(interaction, "g", "xpTxt", ["economy"])[0]}, {cspl_get_param(interaction, "g", "coins", ["economy", "msgAward"])}{cspl_get_param(interaction, "g", "coinsTxt", ["economy"])[0]} / {cspl_get_param(interaction, "g", "cooldown", ["economy", "msgAward"])} сек.`',
					]),
					inline=False
				)
			emb.set_thumbnail(url = self.bot.user.avatar)
			emb.set_footer(text = f"/ Панель управления")
			await interaction.edit_original_response(embed = emb, view = DashboardBtns(self.bot))
		except Exception as e:
			await interaction.edit_original_response(repr(e))
	
	
	# Получить детальную информацию о боте
	@app_commands.command(
		name = "about",
		description = 'Информация о боте'
	)
	@botDecorators.check_cmd_work()
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
			emb.add_field(name = 'Разработчик', value = f'<@980175834373562439>', inline=True)
			#emb.add_field(name = 'Создатели', value = creators, inline=True)
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
		description="Информация о сервере"
	)
	@botDecorators.check_cmd_work()
	async def serverinfo(self, interaction: discord.Interaction):
		try:
			emb = discord.Embed(
				title = f'Сервер: {interaction.guild.name}'
			)
			await interaction.response.send_message("скоро...", ephemeral = False)
		except Exception as e:
			await interaction.response.send_message(repr(e))
	
	@app_commands.command(
		name = "member",
		description = 'Информация об участнике'
	)
	@botDecorators.check_cmd_work()
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
			bio_txt_send_message = ''
			if user != self.bot.user:
				bio_list = []
				if cspl_get_param(interaction, 'u', 'about', ['biography'], user):
					bio_list.append(f"**О себе:** {cspl_get_param(interaction, 'u', 'about', ['biography'], user)}")
				if cspl_get_param(interaction, 'u', 'age', ['biography'], user):
					bio_list.append(f"**Возраст:** {cspl_get_param(interaction, 'u', 'age', ['biography'], user)}")
				if cspl_get_param(interaction, 'u', 'city', ['biography'], user):
					bio_list.append(f"**Город:** {cspl_get_param(interaction, 'u', 'city', ['biography'], user)}")
				if cspl_get_param(interaction, 'u', 'vk', ['biography'], user):
					bio_list.append(f"**VK:** {cspl_get_param(interaction, 'u', 'vk', ['biography'], user)}")
				if cspl_get_param(interaction, 'u', 'tg', ['biography'], user):
					bio_list.append(f"**TG:** {cspl_get_param(interaction, 'u', 'tg', ['biography'], user)}")
				if len(bio_list) > 0:
					emb.add_field(name = 'Биография', value = '\n'.join(bio_list), inline = False)
					bio_txt_send_message = ''
				else:
					bio_txt_send_message = '||Создайте свою биографию с помощью команды </biography set:1251828637473439767>||'
			else:
				emb.add_field(name = 'Биография', value = '\n'.join([
					f"**О себе:** 3990см хуй блять нахуй",
					f"**Возраст:** 2000+",
					f"**Город:** Залупа",
				]), inline = False)
			#emb.add_field(name = 'Статус', value = status)

			economy_levels = cspl_get_param(interaction, 'g', 'lvls', ['economy'])
			economy_levels.insert(0, cspl_get_param(interaction, 'g', 'lvlFirst', ['economy']))

			def find_current_level_xp(xp):
				current_level = 1  # Начальный уровень 1
				next_level = 2  # Следующий уровень 2

				for i in range(1, len(economy_levels)):
					if xp >= economy_levels[i]["xp"]:
						current_level = economy_levels[i]["lvl"]
						if i + 1 < len(economy_levels):
							next_level = economy_levels[i + 1]["lvl"]
						else:
							next_level = None  # Нет следующего уровня
					else:
						break  # Если текущий xp меньше требуемого, остановить цикл

				current_xp = economy_levels[current_level - 1]["xp"]
				if next_level is not None:
					next_xp = economy_levels[next_level - 1]["xp"]
					percent_to_next_level = int(((xp - current_xp) / (next_xp - current_xp)) * 100)
				else:
					percent_to_next_level = 100  # Достигнут максимальный уровень

				return current_level, next_level, percent_to_next_level

			current_level, next_level, percent_to_next_level = find_current_level_xp(cspl_get_param(interaction, 'u', 'xp', ['economy'], user))

			progress_bar_length = 10
			filled_blocks = int(percent_to_next_level / 100 * progress_bar_length)
			empty_blocks = progress_bar_length - filled_blocks

			progress_bar = f"\n`[{'▰' * filled_blocks}{'═' * empty_blocks}]{percent_to_next_level:02d}%`"
			#progress_bar = ''

			current_xp_needed = economy_levels[current_level - 1]["xp"]
			current_level_name = economy_levels[current_level - 1].get("lvlName", False)
			current_level_name_text = f" {current_level_name}" if current_level_name else ""
			if next_level is not None:
				next_xp_needed = economy_levels[next_level - 1]["xp"]
				next_level_name = economy_levels[next_level - 1].get("lvlName", False)
				next_level_name_text = f" {next_level_name}" if next_level_name else ""
				economy_lvl_txt = f"**{cspl_get_param(interaction, 'g', 'lvlTxt', ['economy'])[1]}:** `{current_level}{cspl_get_param(interaction, 'g', 'lvlTxt', ['economy'])[0]}{current_level_name_text} ({cspl_get_param(interaction, 'u', 'xp', ['economy'], user)}{cspl_get_param(interaction, 'g', 'xpTxt', ['economy'])[0]})` {progress_bar} \n`{next_xp_needed - cspl_get_param(interaction, 'u', 'xp', ['economy'], user)}{cspl_get_param(interaction, 'g', 'xpTxt', ['economy'])[0]}` до `{next_level}{cspl_get_param(interaction, 'g', 'lvlTxt', ['economy'])[0]}{next_level_name_text} ({next_xp_needed}{cspl_get_param(interaction, 'g', 'xpTxt', ['economy'])[0]})`"
			else:
				economy_lvl_txt = f"**{cspl_get_param(interaction, 'g', 'lvlTxt', ['economy'])[1]}:** `{current_level}{cspl_get_param(interaction, 'g', 'lvlTxt', ['economy'])[0]}{current_level_name_text} ({cspl_get_param(interaction, 'u', 'xp', ['economy'], user)}{cspl_get_param(interaction, 'g', 'xpTxt', ['economy'])[0]})` {progress_bar} \n`Макс. {cspl_get_param(interaction, 'g', 'lvlTxt', ['economy'])[1].lower()} достигнут`"

			emb.add_field(
				name = "Экономика",
				value = '\n'.join([
					economy_lvl_txt,
					f"**{cspl_get_param(interaction, 'g', 'coinsTxt', ['economy'])[1]}:** `{cspl_get_param(interaction, 'u', 'coins', ['economy'], user)}{cspl_get_param(interaction, 'g', 'coinsTxt', ['economy'])[0]}`"
				])
			)
			emb.add_field(name = f'Роли ({role_list_number})', value = 'Отсутствуют' if role_list == '' else role_list, inline = False)
			# Время создания пользователя в Discord
			created_at_timestamp = int(interaction.user.created_at.timestamp())
			emb.add_field(
				name = 'В Discord', 
				value = f'**Дата:** <t:{created_at_timestamp}:d>\n**Время:** <t:{created_at_timestamp}:T>'
			)
			# Время присоединения пользователя к серверу
			joined_at_timestamp = int(interaction.user.joined_at.timestamp())
			emb.add_field(
				name = 'На сервере', 
				value = f'**Дата:** <t:{joined_at_timestamp}:d>\n**Время:** <t:{joined_at_timestamp}:T>'
			)
			emb.set_footer(text = f'ID: {user.id}')
			emb.timestamp = datetime.now()
			if user.id == 980175834373562439 or user.id == 522136072151367691:
				emb.set_image(url = 'https://media1.tenor.com/m/aW1paWTKpZMAAAAd/%D1%85%D0%B0%D0%BA%D0%B5%D1%80%D1%8B-hackers.gif')
				#emb.set_image(url = 'https://cdn.discordapp.com/attachments/817116435351863306/1251902055375831080/photo1718438465.jpeg?ex=6678d5e5&is=66778465&hm=84845127e2c75af4dbcb1058a483656704885ba47f8f045646f1c236443135ca&')
				#emb.set_image(url = 'https://cdn.discordapp.com/attachments/817116435351863306/1221372466350522368/D82A2342.jpg?ex=667142bf&is=666ff13f&hm=7cd87d621f9cb941e5d301b9abbd3f4a914873d9faa9fdad53b731705002bc41&')
				#emb.set_image(url = "attachment://.db/content/owner/wlp1.jpeg")
			else:
				req = await self.bot.http.request(discord.http.Route("GET", f"/users/{user.id}"))
				banner_id = req["banner"]
				if banner_id:
					banner_url = f"https://cdn.discordapp.com/banners/{user.id}/{banner_id}?size=1024"
					emb.set_image(url = banner_url)

			await interaction.response.send_message(content = bio_txt_send_message if user == interaction.user else '', embed = emb, ephemeral = False)
		except Exception as e:
			await interaction.response.send_message(repr(e), ephemeral = False)
	
	@app_commands.command(
		name = "avatar",
		description = 'Аватарка участника сервера'
	)
	@botDecorators.check_cmd_work()
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
		name = "dev",
		description="А сейчас о моем разработчике))"
	)
	@botDecorators.check_cmd_work()
	async def dev(self, interaction: discord.Interaction):
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

	
def find_current_level_xp(xp):
				economy_levels = cspl_get_param(interaction, 'g', 'lvls', 'economy')
				current_level = cspl_get_param(interaction, 'u', 'lvl', 'economy')
				next_level = cspl_get_param(interaction, 'u', 'lvl', 'economy') + 1

				for i in range(1, len(economy_levels)):
					if xp >= economy_levels[i]["xp"]:
						current_level = economy_levels[i]["lvl"]
						next_level = economy_levels[i + 1]["lvl"]

				current_xp = economy_levels[current_level - 1]["xp"]
				next_xp = economy_levels[next_level - 1]["xp"]

				percent_to_next_level = int(((xp - current_xp) / (next_xp - current_xp)) * 100)

				return current_level, next_level, percent_to_next_level
			current_level, next_level, percent_to_next_level = find_current_level_xp(cspl_get_param(interaction, 'u', 'xp', 'economy'))

			progress_bar_length = 10
			filled_blocks = int(percent_to_next_level / 100 * progress_bar_length)
			empty_blocks = progress_bar_length - filled_blocks

			progress_bar = f"[{'▰' * filled_blocks}{'═' * empty_blocks}]"

			economy_levels = cspl_get_param(interaction, 'g', 'lvls', 'economy')
			current_xp_needed = economy_levels[current_level - 1]["xp"]
			next_xp_needed = economy_levels[next_level - 1]["xp"]

			emb.add_field(
				name = "Экономика",
				value = '\n'.join([
					f"**Уровень:** \n`{current_level}{cspl_get_param(interaction, 'g', 'lvlTxt', ['economy'])[0]} ({current_xp_needed}{cspl_get_param(interaction, 'g', 'xpTxt', 'economy')[0]})` `{progress_bar}{percent_to_next_level:02d}%` `{next_level}{cspl_get_param(interaction, 'g', 'lvlTxt', ['economy'])[0]} ({next_xp_needed}{cspl_get_param(interaction, 'g', 'xpTxt', 'economy')[0]})`",
					f"**{cspl_get_param(interaction, 'g', 'xpTxt', 'economy')[1]}:** `{cspl_get_param(interaction, 'u', 'xp', 'economy')}{cspl_get_param(interaction, 'g', 'xpTxt', 'economy')[0]}`",
					f"**{cspl_get_param(interaction, 'g', 'coinsTxt', 'economy')[1]}:** `{cspl_get_param(interaction, 'u', 'coins', 'economy')}{cspl_get_param(interaction, 'g', 'coinsTxt', 'economy')[0]}`"
				])
			)
"""