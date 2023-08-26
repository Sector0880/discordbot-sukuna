import discord
from discord.ext import commands

import yaml
import json
import asyncio
import datetime
import sys
from time import sleep
import uuid

from googletrans import Translator
from datetime import *

# Импорты всех данных с botConfig:
from botsConfig import (
	# базовые настройки бота
	info as bot_info, version as bot_version, avatar as bot_avatar, languages as bot_languages,
	# цветовая схема
	colors_bot, color_success, color_error,
	# эмодзи
	emoji_mark_none, emoji_mark_error, emoji_mark_success,
	emoji_switch_off, emoji_switch_on,
	emoji_lock_lock, emoji_lock_unlock,
	emoji_load_none, emoji_load_lag, emoji_load_partial_lag, emoji_load_ok,
	emoji_db_rework, emoji_db_ok
)

# Импорты всех данных с dbVars:
from dbVars import (
	# Параметры бота
	bot_activity, bot_tasks_loop_premium_check_premiumtime, bot_tasks_loop_premium_change_premiumtimeremaining,
	# Параметры гильдий
	guild_name, guild_prefix, guild_language,
	guild_premium, guild_premium_uuid, guild_premium_time_start, guild_premium_time_set, guild_premium_time_extra_history, guild_premium_time_end, guild_premium_time_remaining,
	guild_show_id,
	guild_bot_output,
	# Параметры сотрудников
	staff_creator_id, staff_ada_id, staff_staffList_SpecialPerms,
	# Параметры ошибок
	error_terminal_command_error, error_terminal_traceback_error,
	error_command_not_found, error_server_blocked, error_invalid_language,
	# Дополнительные параметры
	files_status_txt
)

import botsFunctions


class BotCommands(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command(aliases = ['время'])
	async def time(self, ctx):
		emb = discord.Embed(title = 'Время онлаин:')
		emb.add_field(name = 'Текущее время UTC (Всемирное)', value = datetime.utcnow().strftime('**Дата:** %Y-%m-%d\n**Время:** %H:%M:%S'))
		emb.add_field(name = 'Текущее время Калининградское', value = (datetime.utcnow() + timedelta(hours = 2)).strftime('**Дата:** %Y-%m-%d\n**Время:** %H:%M:%S'))
		emb.add_field(name = 'Текущее время Московское', value = (datetime.utcnow() + timedelta(hours = 3)).strftime('**Дата:** %Y-%m-%d\n**Время:** %H:%M:%S'))
		emb.add_field(name = 'Текущее время Самарское', value = (datetime.utcnow() + timedelta(hours = 4)).strftime('**Дата:** %Y-%m-%d\n**Время:** %H:%M:%S'))
		emb.add_field(name = 'Текущее время Иркутское', value = (datetime.utcnow() + timedelta(hours = 5)).strftime('**Дата:** %Y-%m-%d\n**Время:** %H:%M:%S'))
		emb.add_field(name = 'Текущее время Омское', value = (datetime.utcnow() + timedelta(hours = 6)).strftime('**Дата:** %Y-%m-%d\n**Время:** %H:%M:%S'))
		emb.add_field(name = 'Текущее время Красноярское', value = (datetime.utcnow() + timedelta(hours = 7)).strftime('**Дата:** %Y-%m-%d\n**Время:** %H:%M:%S'))
		emb.add_field(name = 'Текущее время Иркутское', value = (datetime.utcnow() + timedelta(hours = 8)).strftime('**Дата:** %Y-%m-%d\n**Время:** %H:%M:%S'))
		emb.add_field(name = 'Текущее время Якутское', value = (datetime.utcnow() + timedelta(hours = 9)).strftime('**Дата:** %Y-%m-%d\n**Время:** %H:%M:%S'))
		emb.add_field(name = 'Текущее время Владивостокское', value = (datetime.utcnow() + timedelta(hours = 10)).strftime('**Дата:** %Y-%m-%d\n**Время:** %H:%M:%S'))
		emb.add_field(name = 'Текущее время Магаданское', value = (datetime.utcnow() + timedelta(hours = 11)).strftime('**Дата:** %Y-%m-%d\n**Время:** %H:%M:%S'))
		emb.add_field(name = 'Текущее время Камчатское', value = (datetime.utcnow() + timedelta(hours = 12)).strftime('**Дата:** %Y-%m-%d\n**Время:** %H:%M:%S'))
		emb.add_field(name = 'Текущее время КЗ', value = (datetime.utcnow() + timedelta(hours = 6)).strftime('**Дата:** %Y-%m-%d\n**Время:** %H:%M:%S'))
		emb.set_footer(text = ctx.author, icon_url = ctx.author.avatar.url)
		await ctx.send(embed = emb)

		asyncio.run(botsFunctions.command_counter(ctx = ctx))
	
	@commands.command()
	async def files_status(self, ctx):
		await ctx.send(f"```dts\n{files_status_txt.read()}```")

		#await command_counter(ctx = ctx)

	@commands.command()
	async def botinfo_reset_used(self, ctx):
		with open("./botConfiguration/.db/bot/botConfiguration/botInfo.yml", "r") as read_file: botInfo = yaml.safe_load(read_file)
		botInfo["used"]["commands"]["all"] = 0
		botInfo["used"]["commands"]["mention"] = 0
		botInfo["used"]["commands"]["files_status"] = 0
		botInfo["used"]["commands"]["time"] = 0
		with open("./botConfiguration/.db/bot/botConfiguration/botInfo.yml", "w") as write_file: yaml.safe_dump(botInfo, write_file, sort_keys = False, allow_unicode = True)
		message = await ctx.channel.fetch_message(int(ctx.message.id))
		await message.add_reaction(emoji_mark_success)
	

	# Узнать пинг
	@commands.command(aliases = ['пинг'])
	async def ping(self, ctx):
		#ping = self.bot.latency
		ping = round(self.bot.latency * 1000)
		ping_emoji = '🟩🔳🔳🔳🔳'

		#if ping > 0.10000000000000000:
		if ping > 100:
			ping_emoji = '🟧🟩🔳🔳🔳'

		if ping > 150:
			ping_emoji = '🟥🟧🟩🔳🔳'

		if ping > 200:
			ping_emoji = '🟥🟥🟧🟩🔳'

		if ping > 250:
			ping_emoji = '🟥🟥🟥🟧🟩'

		if ping > 300:
			ping_emoji = '🟥🟥🟥🟥🟧'

		if ping > 350:
			ping_emoji = '🟥🟥🟥🟥🟥'

		# Переменная с пингом бота до текущего шарда
		shard_ping = f'`{ping_emoji}` `{ping}ms`'

		message = await ctx.send('Понг! 🏓  `🔳🔳🔳🔳🔳` `секунду...`')
		await message.edit(content = f'Понг! 🏓  {shard_ping}')
	
	@commands.command(aliases = ["chm"])
	async def checkmessage(self, ctx):
		if ctx.author.id not in [staff_creator_id(), staff_ada_id()] and not guild_bot_output(ctx): return await botsFunctions.bot_output_blocked(ctx)
		if ctx.author.id in [staff_creator_id(), staff_ada_id()]: 
			await ctx.send("Повенуюсь!")
			
		#if not guild_bot_output(ctx): 
			#if ctx.author.id == staff_creator_id(): asyncio.run(functions.bot_output_blocked_forcreator(ctx))
			#else: return asyncio.run(functions.bot_output_blocked(ctx))
		await ctx.send(staff_staffList_SpecialPerms())
		await ctx.send(str(uuid.uuid4().hex))
		await ctx.send(ctx.author.id not in staff_staffList_SpecialPerms() and not guild_bot_output(ctx))

	@commands.command(aliases = ["e"])
	async def exit(self, ctx):
		if ctx.author.id not in [staff_creator_id(), staff_ada_id()]: return await ctx.send("Нету прав.") # на автора сообщения
		await ctx.send("Выключен.")
		await self.bot.change_presence(status = discord.Status.offline)
		sys.exit()
	
	@commands.command()
	async def cmdC(self, ctx):
		if ctx.author.id not in staff_staffList_SpecialPerms() and not guild_bot_output(ctx): return await botsFunctions.bot_output_blocked(ctx)
		if ctx.author.id not in staff_staffList_SpecialPerms(): return await ctx.send("Нету прав.") # на автора сообщения
		# импорты
		cmd_Count = open("./botConfiguration/.db/info/commandsCount.yml", encoding="utf-8")
 
		# команда
		# я потом это все удалю
		msg1 = await ctx.send("```Загрузка счетчика команд: []```")
		sleep(.2)
		msg2 = await msg1.edit(content = "```Загрузка счетчика команд: 0% \ [……………………………]```")
		sleep(.2)
		msg3 = await msg2.edit(content = "```Загрузка счетчика команд: 24% | [■■………………………]```")
		sleep(.2)
		msg4 = await msg3.edit(content = "```Загрузка счетчика команд: 60% / [■■■■■■■…………]```")
		sleep(.2)
		await msg4.edit(content = "```Загрузка счетчика команд: 100% \ [■■■■■■■■■■]```")
		await ctx.channel.purge(limit = 1)
		sleep(.1)
		await ctx.send(content = "```Счетчик команд:```")
		sleep(.2)
		await ctx.send(f"```dts\n{cmd_Count.read()}\n```")
	
	@commands.command()
	async def spam_ada(self, ctx):
		if ctx.author.id not in staff_staffList_SpecialPerms() and not guild_bot_output(ctx): return await botsFunctions.bot_output_blocked(ctx)
		if ctx.author.id not in staff_staffList_SpecialPerms(): return await ctx.send("Нету прав.") # на автора сообщения
		
		user_id = self.bot.get_user(int(224632121879166976))
		user_id_maks = self.bot.get_user(int(980175834373562439))
		await ctx.send(user_id)
		await ctx.send("спамлю")
		num = 0
		nim_chat = await user_id_maks.send(f'Отправлено сообщений: {num}')
		while True:
			await user_id.send("тебе пиздец")
			num +=1
			await nim_chat.edit(content = f'Отправлено сообщений: {num}')
			sleep(.5)


async def setup(bot):
	await bot.add_cog(BotCommands(bot))