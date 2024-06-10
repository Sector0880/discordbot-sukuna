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
	
	app_commands_group_info = app_commands.Group(name = "info", description="Информационные команды")
	
	@app_commands_group_info.command(
		name = "help",
		description = "Получить информацию о командах бота"
	)
	@app_commands.choices(command = [
		app_commands.Choice(name = "time", value = 1)
	])
	async def help(self, interaction: discord.Interaction, command: app_commands.Choice[int] = None):
		try:
			if command == None:
				list_cmds_info = []
				list_cmds_fun = []
				list_cmds_settings = [
					'`set_profile_about`',
					'`set_profile_age`',
					'`set_profile_city`',
					'`del_profile_about`',
					'`del_profile_age`',
					'`del_profile_city`',
				]
				# https://stackoverflow.com/questions/75372569/how-to-get-a-list-of-slash-commands-discord-py ПОЧИТАТЬ
				for slash_command in self.bot.tree.walk_commands():
					list_cmds_info.append(f"</{slash_command.name}:> ")

				emb = discord.Embed(
					description = '\n'.join([
						"Есть сложности использования моих техник? Не расстраивайся, постарайся все запомнить."
						#"Я разделил свои команды на несколько модулей"
					]),
					color = 0x2b2d31
				)
				emb.add_field(
					name = f'Информация [{len(list_cmds_info)}]', 
					value = ', '.join(list_cmds_info),
					inline=True
				)
				emb.add_field(
					name = f'Веселье [{len(list_cmds_fun)}]', 
					value = ', '.join(list_cmds_fun),
					inline=True
				)
				emb.add_field(
					name = f'Настройки [{len(list_cmds_settings)}]', 
					value = ', '.join(list_cmds_settings),
					inline=False
				)
				lists_len = len(list_cmds_info) + len(list_cmds_fun) + len(list_cmds_settings)
				emb.set_footer(text = f"Доступно {lists_len} техник")
				emb.set_author(name = "Sukuna рассказывает о себе, читай внимательно", icon_url = self.bot.user.avatar)
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
	
	@commands.hybrid_command(
		name = 'ping',
		description = 'Узнать время отклика бота.',
		aliases = ['пинг']
	)
	async def ping(self, ctx):
		try:
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

			message = await ctx.send('Отбиваю...  🔳🔳🔳🔳🔳 `секунду...`')
			await message.edit(content = f'Понг! 🏓  {shard_ping}')
		except Exception as e:
			await ctx.send(e)
	
	@commands.hybrid_command(
		name = "profile",
		description = 'Показать информацию о юзере.',
		aliases = ['профиль']
	)
	async def profile(self, ctx, user: discord.Member = None):
		try:
			profile = ctx.author if not user else user
			roles = profile.roles
			role_list = ''
			role_list_number = 0

			for role in reversed(roles):
				if role != ctx.guild.default_role:
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
			#if len(cspl_get_param(ctx, 'u', 'profile')) > 0:
			emb.add_field(name = 'Профиль', value = '\n'.join([
				f"**О себе:** {cspl_get_param(ctx, 'u', 'about', 'profile', user if user else None)}" if cspl_get_param(ctx, 'u', 'about', 'profile', user if user else None) else "**О себе:** `нету`",
				f"**Возраст:** {cspl_get_param(ctx, 'u', 'age', 'profile', user if user else None)}" if cspl_get_param(ctx, 'u', 'age', 'profile', user if user else None) else "**Возраст:** `нету`",
				f"**Город:** {cspl_get_param(ctx, 'u', 'city', 'profile', user if user else None)}" if cspl_get_param(ctx, 'u', 'city', 'profile', user if user else None) else "**Город:** `нету`",
			]), inline = False)
			emb.add_field(name = 'Статус', value = status, inline = False)
			emb.add_field(name = f'Роли [{role_list_number}]', value = 'Отсутствуют' if role_list == '' else role_list, inline = False)
			emb.add_field(name = 'В Discord', value = profile.created_at.strftime('**Дата:** %d/%m/%Y\n**Время:** %H:%M:%S'))
			emb.add_field(name = 'На сервере', value = profile.joined_at.strftime('**Дата:** %d/%m/%Y\n**Время:** %H:%M:%S'))
			emb.set_footer(text = f'ID: {profile.id}')
			emb.timestamp = datetime.utcnow()

			await ctx.send(embed = emb, ephemeral=True)
		except Exception as e:
			await ctx.send(repr(e), ephemeral=True)
	
	@commands.hybrid_command(
		name = "avatar",
		description = 'Получить аватарку юзера.',
		aliases = ['аватарка']
	)
	async def avatar(self, ctx, user: discord.Member = None):
		try:
			user = ctx.author if not user else user

			emb = discord.Embed(colour = 0x2b2d31)
			emb.set_author(name = user, icon_url = user.avatar)
			emb.set_image(url = user.avatar)

			await ctx.send(embed = emb, ephemeral=True)
		except Exception as e:
			await ctx.send(e, ephemeral=True)
	
	# Получить детальную информацию о боте
	@commands.command(aliases = ['об'])
	async def about(self, ctx):
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

			await ctx.send(embed = emb)
		except Exception as e:
			print(e)

async def setup(bot):
	await bot.add_cog(Info(bot))