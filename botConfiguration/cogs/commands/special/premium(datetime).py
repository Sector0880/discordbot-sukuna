# файл скоро будет готов, осталось описать его и можно выкатывать
# найдено несколько нелогичных алгоритмов, надо переписывать
import discord
from discord.ext import commands, tasks

import yaml
import json
import re

import uuid

from dateutil.parser import parse

from time import sleep

from datetime import datetime, timedelta


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
	guild_premium, guild_premium_uuid, guild_premium_time_start, guild_premium_time_set, guild_premium_time_extra, guild_premium_time_extra_history, guild_premium_time_extra_count, guild_premium_time_end, guild_premium_time_remaining,
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
import botFunctions

class Premium(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	# готово
	@commands.command(aliases = ["gtpr", "pr1"])
	async def get_premium(self, ctx, time_count: int):
		if ctx.author.id not in staff_staffList_SpecialPerms() and not guild_bot_output(ctx): return await botFunctions.bot_output_blocked(ctx)
		if ctx.author.id not in staff_staffList_SpecialPerms(): return await botFunctions.command_for_staff(ctx)
		# open db
		with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "r", encoding="utf-8") as read_file: guilds_config_data = json.load(read_file)
		if guilds_config_data[str(ctx.guild.id)]["additional-features"]["privileges"][0]["premium"] == False:
			guilds_config_data[str(ctx.guild.id)]["additional-features"]["privileges"][0]["premium"] = True
			guilds_config_data[str(ctx.guild.id)]["additional-features"]["privileges"][0]["premium-uuid"] = f"prem_{str(uuid.uuid4().hex)}"
			guilds_config_data[str(ctx.guild.id)]["additional-features"]["privileges"][0]["premium-time-start"] = f"{datetime.now()}"
			guilds_config_data[str(ctx.guild.id)]["additional-features"]["privileges"][0]["premium-time-set"] = f"{timedelta(seconds = time_count)}"
			guilds_config_data[str(ctx.guild.id)]["additional-features"]["privileges"][0]["premium-time-extra"] = None
			guilds_config_data[str(ctx.guild.id)]["additional-features"]["privileges"][0]["premium-time-extra-count"] = 0
			guilds_config_data[str(ctx.guild.id)]["additional-features"]["privileges"][0]["premium-time-extra-history"] = None
			guilds_config_data[str(ctx.guild.id)]["additional-features"]["privileges"][0]["premium-time-end"] = f"{datetime.now() + timedelta(seconds = time_count)}"
			guilds_config_data[str(ctx.guild.id)]["additional-features"]["privileges"][0]["premium-time-remaining"] = f"{timedelta(seconds = time_count)}"
			# write db
			with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "w", encoding="utf-8") as write_file: json.dump(guilds_config_data, write_file, ensure_ascii = False, indent = 4)
			sleep(0.1)
			await ctx.send(
				f'{emoji_mark_success} Успешно, сервер получил премиум-статус на `{time_count} секунд`!'
				+ f'\nДата окончания премиума: `{str(guild_premium_time_end(ctx = ctx))[:-7]}`'
			)
		else:
			# нужно переделать концепцию premium-time-extra
			#if guilds_config_data[str(ctx.guild.id)]["additional-features"]["privileges"][0]["premium-time-extra"] == None:
				#guilds_config_data[str(ctx.guild.id)]["additional-features"]["privileges"][0]["premium-time-extra"] = f'{timedelta(seconds = time_count)}'
			#else: 
				#time_obj = datetime.strptime(guilds_config_data[str(ctx.guild.id)]["additional-features"]["privileges"][0]["premium-time-extra"], "%H:%M:%S")
				#guilds_config_data[str(ctx.guild.id)]["additional-features"]["privileges"][0]["premium-time-extra"] = f'{timedelta(seconds = (time_obj).second, minutes = (time_obj).minute, hours = (time_obj).hour) + timedelta(seconds = time_count)}'
			guilds_config_data[str(ctx.guild.id)]["additional-features"]["privileges"][0]["premium-time-extra-count"] += 1
			guilds_config_data[str(ctx.guild.id)]["additional-features"]["privileges"][0]["premium-time-extra-history"] = f'{timedelta(seconds = time_count)}' if guilds_config_data[str(ctx.guild.id)]["additional-features"]["privileges"][0]["premium-time-extra-history"] == None else f'{str(guilds_config_data[str(ctx.guild.id)]["additional-features"]["privileges"][0]["premium-time-extra-history"]) + " | " + str(timedelta(seconds = time_count))}'
			guilds_config_data[str(ctx.guild.id)]["additional-features"]["privileges"][0]["premium-time-end"] = f'{datetime.fromisoformat(guilds_config_data[str(ctx.guild.id)]["additional-features"]["privileges"][0]["premium-time-end"]) + timedelta(seconds = time_count)}'
			guilds_config_data[str(ctx.guild.id)]["additional-features"]["privileges"][0]["premium-time-remaining"] = f'{str(datetime.fromisoformat(guilds_config_data[str(ctx.guild.id)]["additional-features"]["privileges"][0]["premium-time-end"]) - datetime.now())[:-7]}'
			# write db
			with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "w", encoding="utf-8") as write_file: json.dump(guilds_config_data, write_file, ensure_ascii = False, indent = 4)
			sleep(0.1)
			await ctx.send(
				f'{emoji_mark_success} Успешно, сервер получил продление премиум-статуса на `{time_count} секунд`!'
				+ f'\nОсталось: `{str(datetime.fromisoformat(guild_premium_time_end(ctx = ctx)) - datetime.now())[:-7]}`'
				+ f'\nДата окончания премиума: `{str(guild_premium_time_end(ctx = ctx))[:-7]}`'
			)

	# проверка
	@commands.command(aliases = ["dlpr", "pr2"])
	async def delete_premium(self, ctx):
		if ctx.author.id not in staff_staffList_SpecialPerms() and not guild_bot_output(ctx): return await botFunctions.bot_output_blocked(ctx)
		if ctx.author.id not in staff_staffList_SpecialPerms(): return await botFunctions.command_for_staff(ctx)
		# open db
		with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "r", encoding="utf-8") as read_file: guilds_config_data = json.load(read_file)
		if "premium-uuid" not in guilds_config_data[str(ctx.guild.id)]["additional-features"]["privileges"][0]:
			if guilds_config_data[str(ctx.guild.id)]["additional-features"]["privileges"][0]["premium"] ==  False: return await ctx.send("Премиум отсутствует на этом сервере")
			guilds_config_data[str(ctx.guild.id)]["additional-features"]["privileges"][0]["premium"] = False
			# write db
			with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "w", encoding="utf-8") as write_file: json.dump(guilds_config_data, write_file, ensure_ascii = False, indent = 4)
			return await ctx.send("Сервер лишен вечного премиума.")
		if guilds_config_data[str(ctx.guild.id)]["additional-features"]["privileges"][0]["premium"] == True:
			guilds_config_data[str(ctx.guild.id)]["additional-features"]["privileges"][0]["premium"] = False
			del guilds_config_data[str(ctx.guild.id)]["additional-features"]["privileges"][0]["premium-uuid"]
			del guilds_config_data[str(ctx.guild.id)]["additional-features"]["privileges"][0]["premium-time-start"]
			del guilds_config_data[str(ctx.guild.id)]["additional-features"]["privileges"][0]["premium-time-set"]
			del guilds_config_data[str(ctx.guild.id)]["additional-features"]["privileges"][0]["premium-time-extra"]
			del guilds_config_data[str(ctx.guild.id)]["additional-features"]["privileges"][0]["premium-time-extra-count"]
			del guilds_config_data[str(ctx.guild.id)]["additional-features"]["privileges"][0]["premium-time-extra-history"]
			del guilds_config_data[str(ctx.guild.id)]["additional-features"]["privileges"][0]["premium-time-end"]
			del guilds_config_data[str(ctx.guild.id)]["additional-features"]["privileges"][0]["premium-time-remaining"]
			# write db
			with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "w", encoding="utf-8") as write_file: json.dump(guilds_config_data, write_file, ensure_ascii = False, indent = 4)
			#user_channel = self.bot.get_user(guild_owner_id(ctx = ctx))
			#await user_channel.send(f'премиум подписка на сервере `{guild_name(ctx = ctx)}` закончилась')
			await ctx.send("успешно")
		else:
			await ctx.send("Премиум отсутствует на этом сервере")

	@commands.command(aliases = ["dlpr_as", "pr3"])
	async def delete_premium_allservers(self, ctx):
		if ctx.author.id not in staff_staffList_SpecialPerms() and not guild_bot_output(ctx): return await botFunctions.bot_output_blocked(ctx)
		if ctx.author.id not in staff_staffList_SpecialPerms(): return await botFunctions.command_for_staff(ctx)
		# open db
		with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "r", encoding="utf-8") as read_file: guilds_config_data = json.load(read_file)
		for guild in self.bot.guilds:
			guilds_config_data[str(guild.id)]["additional-features"]["privileges"][0]["premium"] = False
			if "premium-uuid" in guilds_config_data[str(guild.id)]["additional-features"]["privileges"][0]: del guilds_config_data[str(guild.id)]["additional-features"]["privileges"][0]["premium-uuid"]
			if "premium-time-start" in guilds_config_data[str(guild.id)]["additional-features"]["privileges"][0]: del guilds_config_data[str(guild.id)]["additional-features"]["privileges"][0]["premium-time-start"]
			if "premium-time-set" in guilds_config_data[str(guild.id)]["additional-features"]["privileges"][0]: del guilds_config_data[str(guild.id)]["additional-features"]["privileges"][0]["premium-time-set"]
			if "premium-time-extra" in guilds_config_data[str(guild.id)]["additional-features"]["privileges"][0]: del guilds_config_data[str(guild.id)]["additional-features"]["privileges"][0]["premium-time-extra"]
			if "premium-time-extra-count" in guilds_config_data[str(guild.id)]["additional-features"]["privileges"][0]: del guilds_config_data[str(guild.id)]["additional-features"]["privileges"][0]["premium-time-extra-count"]
			if "premium-time-extra-history" in guilds_config_data[str(guild.id)]["additional-features"]["privileges"][0]: del guilds_config_data[str(guild.id)]["additional-features"]["privileges"][0]["premium-time-extra-history"]
			if "premium-time-end" in guilds_config_data[str(guild.id)]["additional-features"]["privileges"][0]: del guilds_config_data[str(guild.id)]["additional-features"]["privileges"][0]["premium-time-end"]
			if "premium-time-remaining" in guilds_config_data[str(guild.id)]["additional-features"]["privileges"][0]: del guilds_config_data[str(guild.id)]["additional-features"]["privileges"][0]["premium-time-remaining"]
			# write db
			with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "w", encoding="utf-8") as write_file: json.dump(guilds_config_data, write_file, ensure_ascii = False, indent = 4)
			#user_channel = self.bot.get_user(guilds_config_data[str(guild.id)]["overview"]["owner-id"])
			#await user_channel.send(f'премиум подписка на сервере `{guilds_config_data[str(guild.id)]["overview"]["guild_name"]}` закончилась')
		await ctx.send(f"Успешно.")
	
	@commands.command(aliases = ["chpr", "pr4"])
	async def check_premium(self, ctx):
		if ctx.author.id not in staff_staffList_SpecialPerms() and not guild_bot_output(ctx): return await botFunctions.bot_output_blocked(ctx)
		if ctx.author.id not in staff_staffList_SpecialPerms(): return await botFunctions.command_for_staff(ctx)
		with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "r", encoding="utf-8") as read_file: guilds_config_data = json.load(read_file)
		#await ctx.send(f'```json\n{json.dumps(guilds_config_data[str(ctx.guild.id)]["overview"], ensure_ascii = False, indent = 4)}\n```')
		await ctx.send(f'```json\n{json.dumps(guilds_config_data[str(ctx.guild.id)]["additional-features"]["privileges"][0], ensure_ascii = False, indent = 4)}\n```')
		if guild_premium(ctx = ctx) == True:
			await ctx.send(f'Осталось: `{str(datetime.fromisoformat(guild_premium_time_end(ctx = ctx)) - datetime.now())[:-7]}`')
		else:
			await ctx.send("Премиум отсутствует")

	# проверка окончания премиума
	@tasks.loop(seconds = 1.0)
	async def premium_checkdate(self):
		# open db
		with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "r", encoding="utf-8") as read_file: guilds_config_data = json.load(read_file)
		for guild in self.bot.guilds:
			if "premium-time-end" in guilds_config_data[str(guild.id)]["additional-features"]["privileges"][0]:
				if datetime.fromisoformat(guilds_config_data[str(guild.id)]["additional-features"]["privileges"][0]["premium-time-end"]) < datetime.now():
					guilds_config_data[str(guild.id)]["additional-features"]["privileges"][0]["premium"] = False
					del guilds_config_data[str(guild.id)]["additional-features"]["privileges"][0]["premium-uuid"]
					del guilds_config_data[str(guild.id)]["additional-features"]["privileges"][0]["premium-time-start"]
					del guilds_config_data[str(guild.id)]["additional-features"]["privileges"][0]["premium-time-set"]
					del guilds_config_data[str(guild.id)]["additional-features"]["privileges"][0]["premium-time-extra"]
					del guilds_config_data[str(guild.id)]["additional-features"]["privileges"][0]["premium-time-extra-count"]
					del guilds_config_data[str(guild.id)]["additional-features"]["privileges"][0]["premium-time-extra-history"]
					del guilds_config_data[str(guild.id)]["additional-features"]["privileges"][0]["premium-time-end"]
					del guilds_config_data[str(guild.id)]["additional-features"]["privileges"][0]["premium-time-remaining"]
					# write db
					with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "w", encoding="utf-8") as write_file: json.dump(guilds_config_data, write_file, ensure_ascii = False, indent = 4)
					#user_channel = self.bot.get_user(guilds_config_data[str(guild.id)]["overview"]["owner-id"])
					#await user_channel.send(f'Премиум подписка на сервере `{guilds_config_data[str(guild.id)]["overview"]["guild_name"]}` закончилась')
	
	# обновление окончания времени премиума (на код не влияет, это информационная проверка)
	@tasks.loop(seconds = 1.0)
	async def premium_change_timeremaining(self):
		# open db
		with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "r", encoding="utf-8") as read_file: guilds_config_data = json.load(read_file)
		for guild in self.bot.guilds:
			if "premium-time-remaining" in guilds_config_data[str(guild.id)]["additional-features"]["privileges"][0]:
				guilds_config_data[str(guild.id)]["additional-features"]["privileges"][0]["premium-time-remaining"] = f'{str(datetime.fromisoformat(guilds_config_data[str(guild.id)]["additional-features"]["privileges"][0]["premium-time-end"]) - datetime.now())[:-7]}'
				# write db
				with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "w", encoding="utf-8") as write_file: json.dump(guilds_config_data, write_file, ensure_ascii = False, indent = 4)

	@commands.Cog.listener()
	async def on_ready(self):
		await self.bot.wait_until_ready()
		self.premium_checkdate.start()
		self.premium_change_timeremaining.start()


async def setup(bot):
	await bot.add_cog(Premium(bot))