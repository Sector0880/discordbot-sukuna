# проверка на uuid-history
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
	bot_activity, bot_tasks_loop_premium_check_premiumtime, bot_tasks_loop_premium_change_premiumtimeremaining,
	# Параметры гильдий
	guild_name, guild_prefix, guild_language, guild_owner_id,
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

	# проверка
	@commands.command(aliases = ["gtpr", "pr1"])
	async def get_premium(self, ctx, time_count: int):
		# command work for staff with special permissions
		if ctx.author.id not in staff_staffList_SpecialPerms() and not guild_bot_output(ctx): return await botFunctions.bot_output_blocked(ctx)
		if ctx.author.id not in staff_staffList_SpecialPerms(): return await botFunctions.command_for_staff(ctx)
		
		# open db
		with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "r", encoding="utf-8") as read_file: guilds_config_data = json.load(read_file)
		privileges_0 = guilds_config_data[str(ctx.guild.id)]["additional-features"]["privileges"][0] # path to privileges in server

		if privileges_0["premium"] == False:
			privileges_0["premium"] = True
			privileges_0["premium-uuid"] = f"prem_{str(uuid.uuid4().hex)[:10]}"
			privileges_0["premium-time-start"] = f"{datetime.now()}"
			privileges_0["premium-time-set"] = f"{timedelta(seconds = time_count)}"
			privileges_0["premium-time-extra"] = None
			privileges_0["premium-time-extra-count"] = 0
			privileges_0["premium-time-extra-history"] = None
			privileges_0["premium-time-end"] = f"{datetime.now() + timedelta(seconds = time_count)}"
			privileges_0["premium-time-remaining"] = f"{timedelta(seconds = time_count)}"

			# write db
			with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "w", encoding="utf-8") as write_file: json.dump(guilds_config_data, write_file, ensure_ascii = False, indent = 4)

			sleep(0.1)
			await ctx.send(
				f'{emoji_mark_success} Успешно, сервер получил премиум-статус на `{time_count} секунд`!'
				+ f'\nДата окончания премиума: `{str(guild_premium_time_end(ctx))[:-7]}`'
			)
		else:
			# РАБОТАЕТ ЕБААААТЬ (нужен тест этого кода, ОБЯЗАТЕЛНЬО)
			if privileges_0["premium-time-extra"] == None:
				privileges_0["premium-time-extra"] = f'{timedelta(seconds = time_count)}'
			else:
				time_parts = privileges_0["premium-time-extra"].split(',')
				days = 0  # Изначально количество дней равно 0
				# Проверяем, есть ли дни в значении
				if len(time_parts) == 2:
					days = int(time_parts[0].split()[0])
				# Получить оставшуюся часть времени
				time_remaining = time_parts[-1].strip()
				# Разделить время на часы, минуты и секунды
				hours, minutes, seconds = map(int, time_remaining.split(':'))
				# Создать timedelta объект
				time_delta = timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
				# Обновить значение privileges_0["premium-time-extra"]
				privileges_0["premium-time-extra"] = f'{time_delta + timedelta(seconds=time_count)}'
			privileges_0["premium-time-extra-count"] += 1
			privileges_0["premium-time-extra-history"] = f'{timedelta(seconds = time_count)}' if privileges_0["premium-time-extra-history"] == None else f'{str(privileges_0["premium-time-extra-history"]) + " | " + str(timedelta(seconds = time_count))}'
			privileges_0["premium-time-end"] = f'{datetime.fromisoformat(privileges_0["premium-time-end"]) + timedelta(seconds = time_count)}'
			privileges_0["premium-time-remaining"] = f'{str(datetime.fromisoformat(privileges_0["premium-time-end"]) - datetime.now())[:-7]}'

			# write db
			with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "w", encoding="utf-8") as write_file: json.dump(guilds_config_data, write_file, ensure_ascii = False, indent = 4)

			sleep(0.1)
			await ctx.send(
				f'{emoji_mark_success} Успешно, сервер получил продление премиум-статуса на `{time_count} секунд`!'
				+ f'\nОсталось: `{str(datetime.fromisoformat(guild_premium_time_end(ctx)) - datetime.now())[:-7]}`'
				+ f'\nДата окончания премиума: `{str(guild_premium_time_end(ctx))[:-7]}`'
			)

	# проверка
	@commands.command(aliases = ["dlpr", "pr2"])
	async def delete_premium(self, ctx):
		# command work for staff with special permissions
		if ctx.author.id not in staff_staffList_SpecialPerms() and not guild_bot_output(ctx): return await botFunctions.bot_output_blocked(ctx)
		if ctx.author.id not in staff_staffList_SpecialPerms(): return await botFunctions.command_for_staff(ctx)

		# open db
		with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "r", encoding="utf-8") as read_file: guilds_config_data = json.load(read_file)
		privileges_0 = guilds_config_data[str(ctx.guild.id)]["additional-features"]["privileges"][0]  # path to privileges in server

		if "premium-uuid" not in privileges_0:
			if privileges_0["premium"] == False: return await ctx.send("Премиум отсутствует на этом сервере")

			privileges_0["premium"] = False

			# write db
			with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "w", encoding="utf-8") as write_file: json.dump(guilds_config_data, write_file, ensure_ascii = False, indent = 4)

			return await ctx.send("Сервер лишен вечного премиума.")

		if "premium-uuid" in privileges_0:
			privileges_0["premium-uuid-history"] = f'{privileges_0["premium-uuid"]}' if "premium-uuid-history" not in privileges_0 else f'{privileges_0["premium-uuid-history"] + ", " + privileges_0["premium-uuid"]}'

		if "premium-uuid-history-count" not in privileges_0:
			privileges_0["premium-uuid-history-count"] = 0
		if "premium-uuid-history-count" in privileges_0:
			privileges_0["premium-uuid-history-count"] += 1

		if privileges_0["premium"] == False: return await ctx.send("Премиум отсутствует на этом сервере")
	
		privileges_0["premium"] = False
		del privileges_0["premium-uuid"]
		del privileges_0["premium-time-start"]
		del privileges_0["premium-time-set"]
		del privileges_0["premium-time-extra"]
		del privileges_0["premium-time-extra-count"]
		del privileges_0["premium-time-extra-history"]
		del privileges_0["premium-time-end"]
		del privileges_0["premium-time-remaining"]

		# write db
		with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "w", encoding="utf-8") as write_file: json.dump(guilds_config_data, write_file, ensure_ascii = False, indent = 4)

		user_dmchannel = self.bot.get_user(guild_owner_id(ctx))
		await user_dmchannel.send(f'премиум подписка на сервере `{guild_name(ctx)}` закончилась')
		await ctx.send("успешно")

	# проверка
	@commands.command(aliases = ["dlpr_as", "pr3"])
	async def delete_premium_allservers(self, ctx):
		# command work for staff with special permissions
		if ctx.author.id not in staff_staffList_SpecialPerms() and not guild_bot_output(ctx): return await botFunctions.bot_output_blocked(ctx)
		if ctx.author.id not in staff_staffList_SpecialPerms(): return await botFunctions.command_for_staff(ctx)

		for guild in self.bot.guilds:
			# open db
			with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "r", encoding="utf-8") as read_file: guilds_config_data = json.load(read_file)
			privileges_0 = guilds_config_data[str(guild.id)]["additional-features"]["privileges"][0]  # path to privileges in server

			if "premium-uuid" in privileges_0:
				privileges_0["premium-uuid-history"] = f'{privileges_0["premium-uuid"]}' if "premium-uuid-history" not in privileges_0 else f'{privileges_0["premium-uuid-history"] + ", " + privileges_0["premium-uuid"]}'

			if "premium-uuid-history-count" not in privileges_0:
				privileges_0["premium-uuid-history-count"] = 0
			if "premium-uuid-history-count" in privileges_0:
				privileges_0["premium-uuid-history-count"] += 1

			privileges_0["premium"] = False
			if "premium-uuid" in privileges_0: del privileges_0["premium-uuid"]
			if "premium-time-start" in privileges_0: del privileges_0["premium-time-start"]
			if "premium-time-set" in privileges_0: del privileges_0["premium-time-set"]
			if "premium-time-extra" in privileges_0: del privileges_0["premium-time-extra"]
			if "premium-time-extra-count" in privileges_0: del privileges_0["premium-time-extra-count"]
			if "premium-time-extra-history" in privileges_0: del privileges_0["premium-time-extra-history"]
			if "premium-time-end" in privileges_0: del privileges_0["premium-time-end"]
			if "premium-time-remaining" in privileges_0: del privileges_0["premium-time-remaining"]

			# write db
			with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "w", encoding="utf-8") as write_file: json.dump(guilds_config_data, write_file, ensure_ascii = False, indent = 4)

			user_dmchannel = self.bot.get_user(guilds_config_data[str(guild.id)]["overview"]["owner-id"])
			await user_dmchannel.send(f'премиум подписка на сервере `{guilds_config_data[str(guild.id)]["overview"]["guild_name"]}` закончилась')
		await ctx.send(f"Успешно.")
	
	# проверка
	@commands.command(aliases = ["dlprhis", "pr4"])
	async def delete_premium_uuid_history(self, ctx):
		# command work for staff with special permissions
		if ctx.author.id not in staff_staffList_SpecialPerms() and not guild_bot_output(ctx): return await botFunctions.bot_output_blocked(ctx)
		if ctx.author.id not in staff_staffList_SpecialPerms(): return await botFunctions.command_for_staff(ctx)

		# open db
		with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "r", encoding="utf-8") as read_file: guilds_config_data = json.load(read_file)
		privileges_0 = guilds_config_data[str(ctx.guild.id)]["additional-features"]["privileges"][0]  # path to privileges in server

		if "premium-uuid-history" in privileges_0:
			del privileges_0["premium-uuid-history"]
			del privileges_0["premium-uuid-history-count"]

			# write db
			with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "w", encoding="utf-8") as write_file: json.dump(guilds_config_data, write_file, ensure_ascii = False, indent = 4)

			await ctx.send("Успешно")
		else: await ctx.send("Истории приобретения премиум-подписки нету")

	
	# проверка
	@commands.command(aliases = ["chpr", "pr5"])
	async def check_premium(self, ctx):
		# command work for staff with special permissions
		if ctx.author.id not in staff_staffList_SpecialPerms() and not guild_bot_output(ctx): return await botFunctions.bot_output_blocked(ctx)
		if ctx.author.id not in staff_staffList_SpecialPerms(): return await botFunctions.command_for_staff(ctx)

		# open db
		with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "r", encoding="utf-8") as read_file: guilds_config_data = json.load(read_file)
		privileges_0 = guilds_config_data[str(ctx.guild.id)]["additional-features"]["privileges"][0]  # path to privileges in server

		#await ctx.send(f'```json\n{json.dumps(guilds_config_data[str(ctx.guild.id)]["overview"], ensure_ascii = False, indent = 4)}\n```')
		await ctx.send(f'```json\n{json.dumps(privileges_0, ensure_ascii = False, indent = 4)}\n```')
		if guild_premium(ctx):
			await ctx.send(f'Осталось: `{str(datetime.fromisoformat(guild_premium_time_end(ctx)) - datetime.now())[:-7]}`')
		else:
			await ctx.send("Премиум отсутствует")

	# проверка
	# проверка окончания премиума
	@tasks.loop(seconds = bot_tasks_loop_premium_check_premiumtime())
	async def premium_check_premiumtime(self):
		for guild in self.bot.guilds:
			# open db
			with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "r", encoding="utf-8") as read_file: guilds_config_data = json.load(read_file)
			privileges_0 = guilds_config_data[str(guild.id)]["additional-features"]["privileges"][0]  # path to privileges in server

			if "premium-time-end" in privileges_0:
				if datetime.fromisoformat(privileges_0["premium-time-end"]) < datetime.now():
					if "premium-uuid" in privileges_0:
						privileges_0["premium-uuid-history"] = f'{privileges_0["premium-uuid"]}' if "premium-uuid-history" not in privileges_0 else f'{privileges_0["premium-uuid-history"] + ", " + privileges_0["premium-uuid"]}'

					if "premium-uuid-history-count" not in privileges_0:
						privileges_0["premium-uuid-history-count"] = 0
					if "premium-uuid-history-count" in privileges_0:
						privileges_0["premium-uuid-history-count"] += 1

					privileges_0["premium"] = False
					del privileges_0["premium-uuid"]
					del privileges_0["premium-time-start"]
					del privileges_0["premium-time-set"]
					del privileges_0["premium-time-extra"]
					del privileges_0["premium-time-extra-count"]
					del privileges_0["premium-time-extra-history"]
					del privileges_0["premium-time-end"]
					del privileges_0["premium-time-remaining"]

					# write db
					with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "w", encoding="utf-8") as write_file: json.dump(guilds_config_data, write_file, ensure_ascii = False, indent = 4)

					user_dmchannel = self.bot.get_user(guilds_config_data[str(guild.id)]["overview"]["owner-id"])
					await user_dmchannel.send(f'Премиум подписка на сервере `{guilds_config_data[str(guild.id)]["overview"]["guild_name"]}` закончилась')
	
	# проверка
	# обновление окончания времени премиума (на код не влияет, это информационная проверка)
	@tasks.loop(seconds = bot_tasks_loop_premium_change_premiumtimeremaining())
	async def premium_change_premiumtimeremaining(self):
		for guild in self.bot.guilds:
			# open db
			with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "r", encoding="utf-8") as read_file: guilds_config_data = json.load(read_file)
			privileges_0 = guilds_config_data[str(guild.id)]["additional-features"]["privileges"][0]  # path to privileges in server

			if "premium-time-remaining" in privileges_0:
				privileges_0["premium-time-remaining"] = f'{str(datetime.fromisoformat(privileges_0["premium-time-end"]) - datetime.now())[:-7]}'

				# write db
				with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "w", encoding="utf-8") as write_file: json.dump(guilds_config_data, write_file, ensure_ascii = False, indent = 4)

	# готово
	@commands.Cog.listener()
	async def on_ready(self):
		await self.bot.wait_until_ready()

		self.premium_check_premiumtime.start()
		self.premium_change_premiumtimeremaining.start()


async def setup(bot):
	await bot.add_cog(Premium(bot))