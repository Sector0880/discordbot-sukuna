# проверка
import discord
from discord.ext import commands, tasks

import yaml
import json
import re
import asyncio

import uuid

from dateutil.parser import parse

from time import sleep

from datetime import datetime, timedelta


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
	emoji_db_rework, emoji_db_ok,
	emoji_shield
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
import botsFunctions

class BotOutput(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command(aliases = ["bob", "bo1"])
	async def botoutput_block(self, ctx, time_count: int = None, *, reason = None):
		# если сервер заблокирован то staff игнорируют это ограничение
		if ctx.author.id not in staff_staffList_SpecialPerms() and not guild_bot_output(ctx): return await botsFunctions.bot_output_blocked(ctx)
		# команда работает только для staff с специальными правами (список staffList_SpecialPerms)
		if ctx.author.id not in staff_staffList_SpecialPerms(): return await botsFunctions.command_for_staff(ctx)

		# open db
		with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "r", encoding="utf-8") as read_file: guilds_config_data = json.load(read_file)
		prot_gateaway_bo = guilds_config_data[str(ctx.guild.id)]["protection"]["gateaway"][0] # path to privileges in server

		if time_count == None:
			if prot_gateaway_bo["bot-output"] == False: return await ctx.send("Сервер уже заблокирован.")
			prot_gateaway_bo["bot-output"] = False
			# write db
			with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "w", encoding="utf-8") as write_file: json.dump(guilds_config_data, write_file, ensure_ascii = False, indent = 4)
			await ctx.send(emoji_shield + "Сервер заблокирован.")
			return

		if prot_gateaway_bo["bot-output"]:
			prot_gateaway_bo["bot-output"] = False
			prot_gateaway_bo["bot-output-block-uuid"] = f"bl_{str(uuid.uuid4().hex)[:10]}"
			# код работает отлично, надо сделать систему сохранения истории премиумов в файлах (скорее всего это будет yml)
			#prot_gateaway_bo["bot-output-block-uuid-history"] = f'{prot_gateaway_bo["bot-output-block-uuid"]}' if "bot-output-block-uuid-history" not in prot_gateaway_bo else f'{prot_gateaway_bo["bot-output-block-uuid-history"] + ", " + prot_gateaway_bo["bot-output-block-uuid"]}'
			#prot_gateaway_bo["bot-output-block-uuid-history-count"] = 1 if "bot-output-block-uuid-history-count" not in prot_gateaway_bo else prot_gateaway_bo["bot-output-block-uuid-history-count"] + 1
			prot_gateaway_bo["bot-output-block-reason"] = None if reason == None else f'{reason}'
			prot_gateaway_bo["bot-output-block-time-start"] = f"{datetime.now()}"
			prot_gateaway_bo["bot-output-block-time-set"] = f"{timedelta(seconds = time_count)}"
			prot_gateaway_bo["bot-output-block-time-extra"] = None
			prot_gateaway_bo["bot-output-block-time-extra-count"] = 0
			prot_gateaway_bo["bot-output-block-time-extra-history"] = None
			prot_gateaway_bo["bot-output-block-time-total"] = f"{timedelta(seconds = time_count)}"
			prot_gateaway_bo["bot-output-block-time-end"] = f"{datetime.now() + timedelta(seconds = time_count)}"
			prot_gateaway_bo["bot-output-block-time-remaining"] = f"{timedelta(seconds = time_count)}"

		
			# write db
			with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "w", encoding="utf-8") as write_file: json.dump(guilds_config_data, write_file, ensure_ascii = False, indent = 4)

			sleep(0.1)
			await ctx.send(
				f'{emoji_shield} Успешно, сервер заблокирован на `{time_count} секунд`!'
				+ f'\nДата окончания блокировки: `{str(prot_gateaway_bo["bot-output-block-time-end"])[:-7]}`'
			)
			await ctx.send(f'Причина не указана.' if reason == None else f'Причина: {reason}')
		else:
			# РАБОТАЕТ ЕБААААТЬ (нужен тест этого кода, ОБЯЗАТЕЛНЬО)
			if prot_gateaway_bo["bot-output-block-time-extra"] == None:
				prot_gateaway_bo["bot-output-block-time-extra"] = f'{timedelta(seconds = time_count)}'
			else:
				time_parts = prot_gateaway_bo["bot-output-block-time-extra"].split(',')
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
				# Обновить значение prot_gateaway_bo["bot-output-block-time-extra"]
				prot_gateaway_bo["bot-output-block-time-extra"] = f'{time_delta + timedelta(seconds=time_count)}'
			prot_gateaway_bo["bot-output-block-time-extra-count"] += 1
			prot_gateaway_bo["bot-output-block-time-extra-history"] = f'{timedelta(seconds = time_count)}' if prot_gateaway_bo["bot-output-block-time-extra-history"] == None else f'{str(prot_gateaway_bo["bot-output-block-time-extra-history"]) + " | " + str(timedelta(seconds = time_count))}'
			def time_total_arifm():
				time_parts = prot_gateaway_bo["bot-output-block-time-total"].split(',')
				days = 0  # Изначально количество дней равно 0
				# Проверяем, есть ли дни в значении
				if len(time_parts) == 2:
					days = int(time_parts[0].split()[0])
				# Получить оставшуюся часть времени
				time_remaining = time_parts[-1].strip()
				# Разделить время на часы, минуты и секунды
				hours, minutes, seconds = map(int, time_remaining.split(':'))
				# Создать timedelta объект
				return timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
			prot_gateaway_bo["bot-output-block-time-total"] = f'{time_total_arifm() + timedelta(seconds=time_count)}'
			prot_gateaway_bo["bot-output-block-time-end"] = f'{datetime.fromisoformat(prot_gateaway_bo["bot-output-block-time-end"]) + timedelta(seconds = time_count)}'
			prot_gateaway_bo["bot-output-block-time-remaining"] = f'{str(datetime.fromisoformat(prot_gateaway_bo["bot-output-block-time-end"]) - datetime.now())[:-7]}'

			# write db
			with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "w", encoding="utf-8") as write_file: json.dump(guilds_config_data, write_file, ensure_ascii = False, indent = 4)

			sleep(0.1)
			await ctx.send(
				f'{emoji_shield} Успешно, сервер получил продление блокировки на `{time_count} секунд`!'
				+ f'\nОсталось: `{str(datetime.fromisoformat(prot_gateaway_bo["bot-output-block-time-end"]) - datetime.now())[:-7]}`'
				+ f'\nДата окончания премиума: `{str(prot_gateaway_bo["bot-output-block-time-end"])[:-7]}`'
			)
	
	@commands.command(aliases = ["boub", "bo2"])
	async def botoutput_unblock(self, ctx):
		# если сервер заблокирован то staff игнорируют это ограничение
		if ctx.author.id not in staff_staffList_SpecialPerms() and not guild_bot_output(ctx): return await botsFunctions.bot_output_blocked(ctx)
		# команда работает только для staff с специальными правами (список staffList_SpecialPerms)
		if ctx.author.id not in staff_staffList_SpecialPerms(): return await botsFunctions.command_for_staff(ctx)

		# open db
		with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "r", encoding="utf-8") as read_file: guilds_config_data = json.load(read_file)
		prot_gateaway_bo = guilds_config_data[str(ctx.guild.id)]["protection"]["gateaway"][0] # path to privileges in server

		if "bot-output-block-uuid" not in prot_gateaway_bo:

			prot_gateaway_bo["bot-output"] = True

			# write db
			with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "w", encoding="utf-8") as write_file: json.dump(guilds_config_data, write_file, ensure_ascii = False, indent = 4)

			return await ctx.send("Сервер разблокирован.")

		prot_gateaway_bo["bot-output"] = True
		del prot_gateaway_bo["bot-output-block-uuid"]
		del prot_gateaway_bo["bot-output-block-reason"]
		del prot_gateaway_bo["bot-output-block-time-start"]
		del prot_gateaway_bo["bot-output-block-time-set"]
		del prot_gateaway_bo["bot-output-block-time-extra"]
		del prot_gateaway_bo["bot-output-block-time-extra-count"]
		del prot_gateaway_bo["bot-output-block-time-extra-history"]
		del prot_gateaway_bo["bot-output-block-time-total"]
		del prot_gateaway_bo["bot-output-block-time-end"]
		del prot_gateaway_bo["bot-output-block-time-remaining"]

		# write db
		with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "w", encoding="utf-8") as write_file: json.dump(guilds_config_data, write_file, ensure_ascii = False, indent = 4)

		await ctx.send("успешно")
	
	# ЗАБЛОКИРОВАНО
	@commands.command(aliases = ["dlbob_uh", "bo3"])
	async def delete_bot_output_block_uuid_history(self, ctx):
		message = await ctx.channel.fetch_message(int(ctx.message.id))
		return await message.add_reaction(emoji_mark_error)

		# если сервер заблокирован то staff игнорируют это ограничение
		if ctx.author.id not in staff_staffList_SpecialPerms() and not guild_bot_output(ctx): return await botsFunctions.bot_output_blocked(ctx)
		# команда работает только для staff с специальными правами (список staffList_SpecialPerms)
		if ctx.author.id not in staff_staffList_SpecialPerms(): return await botsFunctions.command_for_staff(ctx)

		# open db
		with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "r", encoding="utf-8") as read_file: guilds_config_data = json.load(read_file)
		prot_gateaway_bo = guilds_config_data[str(ctx.guild.id)]["protection"]["gateaway"][0] # path to privileges in server

		if "bot-output-block-uuid-history" in prot_gateaway_bo:
			del prot_gateaway_bo["bot-output-block-uuid-history"]
			del prot_gateaway_bo["bot-output-block-uuid-history-count"]

			# write db
			with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "w", encoding="utf-8") as write_file: json.dump(guilds_config_data, write_file, ensure_ascii = False, indent = 4)

			await ctx.send(emoji_mark_success + "Успешно удалена история блокировок.")
		else: await ctx.send(emoji_mark_error + "История блокировок отсутствует, либо вы её уже удалили.")
	
	
	@commands.command(aliases = ["chbo", "bo4"])
	async def check_bot_output(self, ctx, code = None):
		# если сервер заблокирован то staff игнорируют это ограничение
		if ctx.author.id not in staff_staffList_SpecialPerms() and not guild_bot_output(ctx): return await botsFunctions.bot_output_blocked(ctx)
		# команда работает только для staff с специальными правами (список staffList_SpecialPerms)
		if ctx.author.id not in staff_staffList_SpecialPerms(): return await botsFunctions.command_for_staff(ctx)

		# open db
		with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "r", encoding="utf-8") as read_file: guilds_config_data = json.load(read_file)
		prot_gateaway_bo = guilds_config_data[str(ctx.guild.id)]["protection"]["gateaway"][0] # path to privileges in server

		#await ctx.send(f'```json\n{json.dumps(guilds_config_data[str(ctx.guild.id)]["overview"], ensure_ascii = False, indent = 4)}\n```')
		if code != None: await ctx.send(f'```ansi\n\u001b[{0};{31}m{json.dumps(prot_gateaway_bo, ensure_ascii = False, indent = 4)}\u001b[0m\n```')
		if "bot-output-block-time-end" in prot_gateaway_bo:
			await ctx.send(f'До окончания блокировки: `{str(datetime.fromisoformat(prot_gateaway_bo["bot-output-block-time-end"]) - datetime.now())[:-7]}`')
		else:
			await ctx.send("Блокировка отсутствует.")
			if "bot-output-block-reason" in prot_gateaway_bo != None: await ctx.send(f'Записанная причина: {prot_gateaway_bo["bot-output-block-reason"]}')
	
	
	# проверка окончания блокировки
	@tasks.loop(seconds = 1)
	async def botoutput_check_blocktime(self):
		for guild in self.bot.guilds:
			# open db
			with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "r", encoding="utf-8") as read_file: guilds_config_data = json.load(read_file)
			prot_gateaway_bo = guilds_config_data[str(guild.id)]["protection"]["gateaway"][0] # path to privileges in server

			if "bot-output-block-time-end" in prot_gateaway_bo:
				if datetime.fromisoformat(prot_gateaway_bo["bot-output-block-time-end"]) < datetime.now():
					prot_gateaway_bo["bot-output"] = True
					del prot_gateaway_bo["bot-output-block-uuid"]
					del prot_gateaway_bo["bot-output-block-reason"]
					del prot_gateaway_bo["bot-output-block-time-start"]
					del prot_gateaway_bo["bot-output-block-time-set"]
					del prot_gateaway_bo["bot-output-block-time-extra"]
					del prot_gateaway_bo["bot-output-block-time-extra-count"]
					del prot_gateaway_bo["bot-output-block-time-extra-history"]
					del prot_gateaway_bo["bot-output-block-time-total"]
					del prot_gateaway_bo["bot-output-block-time-end"]
					del prot_gateaway_bo["bot-output-block-time-remaining"]

					# write db
					with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "w", encoding="utf-8") as write_file: json.dump(guilds_config_data, write_file, ensure_ascii = False, indent = 4)

					user_dmchannel = self.bot.get_user(guilds_config_data[str(guild.id)]["overview"]["owner-id"])
					await user_dmchannel.send(f'Премиум подписка на сервере `{guilds_config_data[str(guild.id)]["overview"]["guild_name"]}` закончилась')
	
	
	# обновление окончания времени блокировки (на код не влияет, это информационная проверка)
	@tasks.loop(seconds = 1)
	async def botoutput_change_blocktimeremaining(self):
		for guild in self.bot.guilds:
			# open db
			with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "r", encoding="utf-8") as read_file: guilds_config_data = json.load(read_file)
			prot_gateaway_bo = guilds_config_data[str(guild.id)]["protection"]["gateaway"][0] # path to privileges in server

			if "bot-output-block-time-remaining" in prot_gateaway_bo:
				prot_gateaway_bo["bot-output-block-time-remaining"] = f'{str(datetime.fromisoformat(prot_gateaway_bo["bot-output-block-time-end"]) - datetime.now())[:-7]}'

				# write db
				with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "w", encoding="utf-8") as write_file: json.dump(guilds_config_data, write_file, ensure_ascii = False, indent = 4)

	# готово
	@commands.Cog.listener()
	async def on_ready(self):
		await self.bot.wait_until_ready()

		self.botoutput_check_blocktime.start()
		self.botoutput_change_blocktimeremaining.start()
	

async def setup(bot):
	await bot.add_cog(BotOutput(bot))