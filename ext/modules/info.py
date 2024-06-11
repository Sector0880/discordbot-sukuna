import discord
from discord.ext import commands
from discord import app_commands
import yaml

import datetime, time
from time import *
from botConfig import *
from datetime import *
from dbVars import *
from botFunctions import *

class Info(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
	
	@app_commands.command(
		name = "help",
		description = "Получить информацию о командах бота"
	)
	@app_commands.choices(command = [
		app_commands.Choice(name = "time", value = 1)
	])
	async def help(self, interaction: discord.Interaction, command: app_commands.Choice[int] = None):
		try:
			if command == None:
				list_cmds_info = [
					{'command': '</help:1250144368837529692>',   'permission': None},
					{'command': '</ping:1249321143983145034>',   'permission': None},
					{'command': '</avatar:1249321144469950546>', 'permission': None},
					{'command': '</about:1250159784683114496>',  'permission': None},
				]
				list_cmds_fun = [
					{'command': '</time:1250150935280357376>', 'permission': None},
					{'command': '</fact:1250150935280357377>', 'permission': None}
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
					{'command': '</mute:>', 'permission': discord.Permissions.mute_members},
					{'command': '</ban:>', 'permission': discord.Permissions.ban_members}
				]

				filtered_list_cmds_info = [cmd for cmd in list_cmds_info if cmd['permission'] is None or interaction.user.guild_permissions.ban_members]
				filtered_list_cmds_fun = [cmd for cmd in list_cmds_fun if cmd['permission'] is None or interaction.user.guild_permissions.ban_members]
				filtered_list_cmds_settings = [cmd for cmd in list_cmds_settings if cmd['permission'] is None or interaction.user.guild_permissions.ban_members]
				filtered_list_cmds_moderation = [cmd for cmd in list_cmds_moderation if cmd['permission'] is None or interaction.user.guild_permissions.ban_members]

				lists_len = len(filtered_list_cmds_info) + len(filtered_list_cmds_fun) + len(filtered_list_cmds_settings) + len(filtered_list_cmds_moderation)
				emb = discord.Embed(
					title = f"Доступные техники ({lists_len})",
					description = '\n'.join([
						"Есть сложности использования моих техник? Не расстраивайся, постарайся все запомнить.",
						"Все мои техники начинаются с `/` (потому что используются слеш-техники).",
						"Я разделил свои команды на несколько модулей, чтобы твоя бошка тыквенная не сдохла от моей гениальности :)))"
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
					name = f'Настройки [{len(filtered_list_cmds_settings)}]',
					value=' '.join([cmd['command'] for cmd in filtered_list_cmds_settings]),
					inline = False
				)
				emb.add_field(
					name=f'<:Mod_Shield:1142795808945745970> Модерация (команды не существуют) [{len(filtered_list_cmds_moderation)}]',
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
			await interaction.response.send_message(embed = emb, ephemeral = True)
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
			guilds = ''
			for guild in self.bot.guilds:
				guilds += '1'

			members = len(list(self.bot.get_all_members()))

			emb = discord.Embed()
			emb.set_author(name = f'{self.bot.user} | ID: {self.bot.user.id}', icon_url = self.bot.user.avatar)

			maks = self.bot.get_user(980175834373562439)
			emb.add_field(name = 'Разработчик', value = f'<@980175834373562439>', inline=False)
			emb.add_field(name = 'Библиотека', value = f'discord.py {discord.__version__}', inline=False)

			emb.add_field(name = 'Кол-во серверов', value = f'{str(len(guilds))}', inline=True)
			emb.add_field(name = 'Кол-во юзеров', value = f'{members}', inline=True)

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

			TimeFromStart = datetime.now() - start_time

			emb.set_footer(text = f'Длительность работы: {str(TimeFromStart)[:-7]}')

			emb.add_field(name = 'Пинг', value = shard_ping, inline = False)

			await interaction.response.send_message(embed = emb)
		except Exception as e:
			print(e)

async def setup(bot):
	await bot.add_cog(Info(bot))