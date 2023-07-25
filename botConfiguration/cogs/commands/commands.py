import discord
from discord.ext import commands

import yaml
import json
import asyncio

from googletrans import Translator
from datetime import *

# Импорты всех данных с botConfig:
from botConfig import (
	info, version, avatar, languages,
	colors_bot, color_success, color_error,
	emoji_mark_none, emoji_mark_error, emoji_mark_success,
	emoji_switch_off, emoji_switch_on,
	emoji_lock_lock, emoji_lock_unlock,
	emoji_load_none, emoji_load_lag, emoji_load_partial_lag, emoji_load_ok,
	emoji_db_rework, emoji_db_ok
)

# Импорты всех данных с dbVars:
from dbVars import (
	# Параметры бота
	bot_activity, bot_delete_after,
	# Параметры гильдий
	guild_name, guild_owner_id,
	guild_prefix, guild_language,
	guild_premium, guild_premium_start_date, guild_premium_end_date,
	guild_show_id,
	guild_bot_output,
	# Параметры сотрудников
	staff_creator_id,
	# Параметры ошибок
	error_terminal_command_error, error_terminal_traceback_error,
	error_command_not_found, error_server_blocked, error_invalid_language,
	# Дополнительные параметры
	files_status_txt
)

async def command_counter(ctx):
	command = ctx.invoked_with
	with open("./botConfiguration/.db/bot/botConfiguration/botInfo.yml", "r") as read_file: botInfo = yaml.safe_load(read_file)
	botInfo["used"]["commands"]["all"] += 1 # все команды
	botInfo["used"]["commands"][command] += 1 # вызываемая команда
	with open("./botConfiguration/.db/bot/botConfiguration/botInfo.yml", "w") as write_file: yaml.safe_dump(botInfo, write_file, sort_keys = False, allow_unicode = True)


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

		await command_counter(ctx = ctx)
	
	@commands.command()
	async def files_status(self, ctx):
		await ctx.send(f"```dts\n{files_status_txt.read()}```")

		#await command_counter(ctx = ctx)

	@commands.command()
	async def botinfo_used_reset(self, ctx):
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
		await ctx.send(guild_premium_end_date(ctx))


async def setup(bot):
	await bot.add_cog(BotCommands(bot))