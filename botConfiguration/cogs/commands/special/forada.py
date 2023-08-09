import discord
from discord.ext import commands

import asyncio
import re

# Импорты всех данных с botConfig:
from botConfig import (
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
	bot_activity, bot_delete_after,
	# Параметры гильдий
	guild_name, guild_prefix, guild_language,
	guild_premium, guild_premium_start_date, guild_premium_end_date,
	guild_show_id,
	guild_bot_output,
	# Параметры сотрудников
	staff_creator_id, staff_ada_id, 
	# Параметры ошибок
	error_terminal_command_error, error_terminal_traceback_error,
	error_command_not_found, error_server_blocked, error_invalid_language,
	# Дополнительные параметры
	files_status_txt
)

from botFunctions import *

class ForADA(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command(aliases = ["дубляж"])
	async def message_dublite(self, ctx, channel = None):
		# проверки
		if ctx.author.id not in [staff_creator_id(), staff_ada_id()]: return await ctx.send("Нету прав.") # на автора сообщения
		if channel is None: return await ctx.send("Напиши id чата") # на наличие channel_id
		if not isinstance(channel, int) and not channel.isdigit(): # слава богам всевышним что пока этот try except работает, раньше команда и без него нормально выводила ошибку если написано str но ожидали int, но чтото сломалось и пизда
			return await ctx.send("Я понимаю только id чата, не ссылку или имя, ID!") # на тип channel_id
		else: channel = int(channel)
		channel_id = self.bot.get_channel(channel) # получаем id канала
		if not channel_id: return await ctx.send(f"Чат не найден → <#{channel}>") # если id канала не найден
		await ctx.send(f"Напиши сообщение, я его продублирую\nСервер: `{channel_id.guild.name}`\nЧат: <#{channel}>")
		time_waiting = 60.0 # время ожидания
		try:
			message = await self.bot.wait_for("message", check = lambda ctx: ctx.author == ctx.author and ctx.channel == ctx.channel, timeout = time_waiting)
			#if message.content == "ОТМЕНА" or "ОТ": return await ctx.send("Команда отменена принужденно.")
			if re.fullmatch("ОТМЕНА", message.content): return await ctx.send("Команда отменена принужденно.")
			message_output = await channel_id.send(message.content)
			await ctx.send(f"Успешно, сообщение: {message_output.jump_url}")
		except asyncio.TimeoutError:
			await ctx.send(f"Время ожидания истекло ({time_waiting} секунд)")
		
	@commands.command(aliases = ["изменить_статус", "chac"])
	async def change_activity(self, ctx, *, activity_text = None):
		# проверки
		if ctx.author.id not in [staff_creator_id(), staff_ada_id()]: return await ctx.send("Нету прав.") # на автора сообщения
		if activity_text == None: return await ctx.send("Напиши мне статус")
		if re.fullmatch("RESET", activity_text):
			#activity = self.bot.activity
			#if isinstance(activity, discord.Game): game_name = activity.name
			#if re.fullmatch(bot_activity(), game_name):
				#return await ctx.send("Статус реснуть нельзя.")
			await self.bot.change_presence(activity = discord.Game(bot_activity()))
			await command_counter(ctx)
			return await ctx.send(f"Статус бота был сброшен.")

		# команда
		await self.bot.change_presence(activity = discord.Game(activity_text))
		await ctx.send(f"Статус бота изменен на `{activity_text}`")
		await command_counter(ctx)
			
async def setup(bot):
	await bot.add_cog(ForADA(bot))