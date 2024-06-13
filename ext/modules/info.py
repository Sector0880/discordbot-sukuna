import discord
from discord.ext import commands
from discord import app_commands
import yaml

import datetime, time
import locale
from time import *
from botConfig import *
from datetime import *
from dbVars import *
from botFunctions import *

locale.setlocale(
    category=locale.LC_ALL,
    locale="Russian"  # Note: do not use "de_DE" as it doesn't work
)

class Info(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
	
	@app_commands.command(
		name = "help",
		description = "Получить информацию о командах бота"
	)
	@app_commands.choices(command = [
		app_commands.Choice(name = "help", value = 1),
		app_commands.Choice(name = "ping", value = 2),
		app_commands.Choice(name = "avatar", value = 3),
		app_commands.Choice(name = "about", value = 4),
		app_commands.Choice(name = "time", value = 5),
		app_commands.Choice(name = "fact", value = 6),
		app_commands.Choice(name = "profile show", value = 7),
		app_commands.Choice(name = "profile set_about", value = 8),
		app_commands.Choice(name = "profile set_age", value = 9),
		app_commands.Choice(name = "profile set_city", value = 10),
		app_commands.Choice(name = "profile del_about", value = 11),
		app_commands.Choice(name = "profile del_age", value = 12),
		app_commands.Choice(name = "profile del_city", value = 13)
	])
	async def help(self, interaction: discord.Interaction, command: app_commands.Choice[int] = None):
		try:
			if command == None:
				list_cmds_info = [
					{'command': '</help:1250144368837529692>',   'permission': None},
					{'command': '</about:1250159784683114496>',  'permission': None},
					{'command': '</serverinfo:1250362239341301760>',  'permission': None},
					{'command': '</ping:1249321143983145034>',   'permission': None},
					{'command': '</avatar:1249321144469950546>', 'permission': None},
					{'command': '</myowner:1250743777077755915>', 'permission': None},
				]
				list_cmds_fun = [
					{'command': '</time:1250150935280357376>', 'permission': None},
					{'command': '</fact:1250150935280357377>', 'permission': None},
					{'command': '</battle:1250720060344107019>', 'permission': None}
				]
				list_cmds_settings = [
					{'command': '</profile show:1250158028435751013>',      'permission': None},
					{'command': '</profile set_about:1250158028435751013>', 'permission': None},
					{'command': '</profile set_age:1250158028435751013>',   'permission': None},
					{'command': '</profile set_city:1250158028435751013>',  'permission': None},
					{'command': '</profile del_about:1250158028435751013>', 'permission': None},
					{'command': '</profile del_age:1250158028435751013>',   'permission': None},
					{'command': '</profile del_city:1250158028435751013>',  'permission': None},
				]
				list_cmds_moderation = [
					{'command': '</mute:1250456425742995456>', 'permission': interaction.user.guild_permissions.mute_members},
					{'command': '</ban:1250456425742995457>', 'permission': interaction.user.guild_permissions.ban_members}
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
				emb.set_footer(text = "dev: Sectormain, 2024", icon_url = iam.avatar)
				#emb.set_author(name = "Sukuna рассказывает о себе, читай внимательно", icon_url = self.bot.user.avatar)
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
			else:
				return await interaction.response.send_message("Команда не найдена.", ephemeral = True)
			await interaction.response.send_message(embed = emb, ephemeral = False)
		except Exception as e:
			await interaction.response.send_message(f'||{e}||')
	
	@app_commands.command(
		name = 'ping',
		description = 'Узнать время отклика бота.'
	)
	async def ping(self, interaction: discord.Interaction):
		try:
			await interaction.response.defer(ephemeral=True, thinking=True)

			ping = self.bot.latency
			ping_emoji = '🟩🔳🔳🔳🔳'

			if ping > 0.10000000000000000:
				ping_emoji = '🟧🟩🔳🔳🔳'

			if ping > 0.15000000000000000:
				ping_emoji = '🟥🟧🟩🔳🔳'

			if ping > 0.20000000000000000:
				ping_emoji = '🟥🟥🟧🟩🔳'

			if ping > 0.25000000000000000:
				ping_emoji = '🟥🟥🟥🟧🟩'

			if ping > 0.30000000000000000:
				ping_emoji = '🟥🟥🟥🟥🟧'

			if ping > 0.35000000000000000:
				ping_emoji = '🟥🟥🟥🟥🟥'

			# Переменная с пингом бота до текущего шарда
			shard_ping = f'{ping_emoji} `{round(self.bot.latency * 1000)}ms`'

			message = await interaction.edit_original_response(content = 'Отбиваю...  \n🔳🔳🔳🔳🔳 `секунду...`')
			await message.edit(content = f'Понг! 🏓  \n{shard_ping}')
		except Exception as e:
			await interaction.edit_original_response(content = e)
	
	@app_commands.command(
		name = "avatar",
		description = 'Получить аватарку юзера.'
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
	
	# Получить детальную информацию о боте
	@app_commands.command(
		name = "about",
		description = 'Получить информацию о боте.'
	)
	async def about(self, interaction: discord.Interaction):
		try:
			guilds = 0
			for guild in self.bot.guilds:
				guilds += 1

			members = len(list(self.bot.get_all_members()))

			emb = discord.Embed(color=0x2b2d31)
			#emb.set_author(name = f'{self.bot.user} | ID: {self.bot.user.id}', icon_url = self.bot.user.avatar)

			maks = self.bot.get_user(980175834373562439)
			emb.add_field(name = 'Разработчик', value = f'<@980175834373562439>', inline=True)
			emb.add_field(name = 'Кол-во серверов', value = f'{str(guilds)}', inline=True)
			emb.add_field(name = 'Кол-во юзеров', value = f'{members}', inline=True)

			#emb.add_field(name = 'Библиотека', value = f'discord.py {discord.__version__}', inline=True)

			emb.add_field(name = 'Версия', value = f'v0.9', inline=True)

			ping = self.bot.latency
			ping_emoji = '🟩🔳🔳🔳🔳'

			if ping > 0.10000000000000000:
				ping_emoji = '🟧🟩🔳🔳🔳'

			if ping > 0.15000000000000000:
				ping_emoji = '🟥🟧🟩🔳🔳'

			if ping > 0.20000000000000000:
				ping_emoji = '🟥🟥🟧🟩🔳'

			if ping > 0.25000000000000000:
				ping_emoji = '🟥🟥🟥🟧🟩'

			if ping > 0.30000000000000000:
				ping_emoji = '🟥🟥🟥🟥🟧'

			if ping > 0.35000000000000000:
				ping_emoji = '🟥🟥🟥🟥🟥'

			# Переменная с пингом бота до текущего шарда
			shard_id = interaction.guild.shard_id
			shard = self.bot.get_shard(shard_id)
			shard_ping = f'{ping_emoji} `{round(shard.latency * 1000)}ms`'
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
		description="Получить информацию о сервере."
	)
	async def serverinfo(self, interaction: discord.Interaction):
		try:
			await interaction.response.send_message('скоро', ephemeral=True)
		except Exception as e:
			await interaction.response.send_message(repr(e))
	
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
"""