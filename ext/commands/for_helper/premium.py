import discord
from discord.ext import commands, tasks
from discord import app_commands

import yaml
import json
import re
import asyncio
import uuid
from time import sleep
from datetime import datetime, timedelta

from botConfig import *
from dbVars import *
import botFunctions

class Premium(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot


	@app_commands.command(
		name = command_get_premium()["name"], 
		description = command_get_premium()["description"]
	)
	@app_commands.describe(
		server = command_get_premium()["describe"]["server!"], 
		time = command_get_premium()["describe"]["time!"]
	)
	@botFunctions.check_command_permissions()
	async def get_premium(self, interaction: discord.Interaction, server: str, *, time: int):
		# open db
		with open("./.db/multiplayer/guilds.json", "r", encoding="utf-8") as read_file: guilds_config_data = json.load(read_file)
		
		# path to privileges in server
		if not isinstance(server, int) and not server.isdigit(): return await interaction.response.send_message("Я понимаю только id сервера.", ephemeral = True)
		#guild = self.bot.get_guild(int(server)) # получаем название сервера
		#if not guild: return await interaction.response.send_message("Сервер не найден.", ephemeral = True) # проверка на наличие сервера
		#server = guild.id # получаем id сервера
		#guild_id = str(server)
		if str(server) not in guilds_config_data: return await interaction.response.send_message("Сервер не найден.", ephemeral = True) # проверка на наличие сервера

		
		privileges_0 = guilds_config_data[str(server)]["additional-features"]["privileges"][0]

		if privileges_0["premium"] == False:
			privileges_0["premium"] = True
			privileges_0["premium-uuid"] = f"prem_{str(uuid.uuid4().hex)}"
			privileges_0["premium-uuid-history"] = f'{privileges_0["premium-uuid"]}' if "premium-uuid-history" not in privileges_0 else f'{privileges_0["premium-uuid-history"] + ", " + privileges_0["premium-uuid"]}'
			privileges_0["premium-uuid-history-count"] = 1 if "premium-uuid-history-count" not in privileges_0 else privileges_0["premium-uuid-history-count"] + 1
			privileges_0["premium-time-start"] = f"{datetime.now()}"
			privileges_0["premium-time-set"] = f"{timedelta(seconds = time)}"
			privileges_0["premium-time-extra"] = None
			privileges_0["premium-time-extra-count"] = 0
			privileges_0["premium-time-extra-history"] = None
			privileges_0["premium-time-total"] = f"{timedelta(seconds = time)}"
			privileges_0["premium-time-end"] = f"{datetime.now() + timedelta(seconds = time)}"
			privileges_0["premium-time-remaining"] = f"{timedelta(seconds = time)}"

			# open db, premium info in filedoc
			with open("./.db/info/premiumHistory.json", "r", encoding="utf-8") as read_file: premium_history_data = json.load(read_file)
			premium_history_data[privileges_0["premium-uuid"]] = {
				"premium": privileges_0["premium"],
				"premium-time-start": privileges_0["premium-time-start"],
				"premium-time-set": privileges_0["premium-time-set"],
				"premium-time-extra": privileges_0["premium-time-extra"],
				"premium-time-extra-count": privileges_0["premium-time-extra-count"],
				"premium-time-extra-history": privileges_0["premium-time-extra-history"],
				"premium-time-total": privileges_0["premium-time-total"],
				"premium-time-end": privileges_0["premium-time-end"]
			}
			# write db, premium info in filedoc
			with open("./.db/info/premiumHistory.json", "w", encoding="utf-8") as write_file: json.dump(premium_history_data, write_file, ensure_ascii = False, indent = 4)

			# write db
			with open("./.db/multiplayer/guilds.json", "w", encoding="utf-8") as write_file: json.dump(guilds_config_data, write_file, ensure_ascii = False, indent = 4)

			#sleep(0.1)
			await interaction.response.send_message(
				f'{emoji_mark_success} Успешно, сервер `{guilds_config_data[str(server)]["overview"]["guild_name"]}` получил премиум-статус на `{time} секунд`!'
				+ f'\nДата окончания премиума: `{str(privileges_0["premium-time-end"])[:-7]}`'
			)
		else:
			# РАБОТАЕТ ЕБААААТЬ (нужен тест этого кода, ОБЯЗАТЕЛНЬО)
			if privileges_0["premium-time-extra"] == None:
				privileges_0["premium-time-extra"] = f'{timedelta(seconds = time)}'
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
				privileges_0["premium-time-extra"] = f'{time_delta + timedelta(seconds=time)}'
			privileges_0["premium-time-extra-count"] += 1
			privileges_0["premium-time-extra-history"] = f'{timedelta(seconds = time)}' if privileges_0["premium-time-extra-history"] == None else f'{str(privileges_0["premium-time-extra-history"]) + " | " + str(timedelta(seconds = time))}'
			def time_total_arifm():
				time_parts = privileges_0["premium-time-total"].split(',')
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
			privileges_0["premium-time-total"] = f'{time_total_arifm() + timedelta(seconds=time)}'
			privileges_0["premium-time-end"] = f'{datetime.fromisoformat(privileges_0["premium-time-end"]) + timedelta(seconds = time)}'
			privileges_0["premium-time-remaining"] = f'{str(datetime.fromisoformat(privileges_0["premium-time-end"]) - datetime.now())[:-7]}'

			# open db, premium info in filedoc
			with open("./.db/info/premiumHistory.json", "r", encoding="utf-8") as read_file: premium_history_data = json.load(read_file)
			if "premium-uuid" not in premium_history_data: 
				premium_history_data[privileges_0["premium-uuid"]] = {
					"premium": privileges_0["premium"],
					"premium-time-start": privileges_0["premium-time-start"],
					"premium-time-set": privileges_0["premium-time-set"],
					"premium-time-extra": privileges_0["premium-time-extra"],
					"premium-time-extra-count": privileges_0["premium-time-extra-count"],
					"premium-time-extra-history": privileges_0["premium-time-extra-history"],
					"premium-time-total": privileges_0["premium-time-total"],
					"premium-time-end": privileges_0["premium-time-end"]
				}
			premium_history_data[privileges_0["premium-uuid"]]["premium-time-extra"] = privileges_0["premium-time-extra"]
			premium_history_data[privileges_0["premium-uuid"]]["premium-time-extra-count"] = privileges_0["premium-time-extra-count"]
			premium_history_data[privileges_0["premium-uuid"]]["premium-time-extra-history"] = privileges_0["premium-time-extra-history"]
			premium_history_data[privileges_0["premium-uuid"]]["premium-time-total"] = privileges_0["premium-time-total"]
			premium_history_data[privileges_0["premium-uuid"]]["premium-time-end"] = privileges_0["premium-time-end"]
			# write db, premium info in filedoc
			with open("./.db/info/premiumHistory.json", "w", encoding="utf-8") as write_file: json.dump(premium_history_data, write_file, ensure_ascii = False, indent = 4)

			# write db
			with open("./.db/multiplayer/guilds.json", "w", encoding="utf-8") as write_file: json.dump(guilds_config_data, write_file, ensure_ascii = False, indent = 4)

			#sleep(0.1)
			await interaction.response.send_message(
				f'{emoji_mark_success} Успешно, сервер `{guilds_config_data[str(server)]["overview"]["guild_name"]}` получил продление премиум-статуса на `{time} секунд`!'
				+ f'\nОсталось: `{str(datetime.fromisoformat(privileges_0["premium-time-end"]) - datetime.now())[:-7]}`'
				+ f'\nДата окончания премиума: `{str(privileges_0["premium-time-end"])[:-7]}`'
			)
	
	@app_commands.command(
		name = "delete_premium",
		description = "Лишить сервер премиум."
	)
	@app_commands.describe(server = "Сервер, который лишается премиума.")
	@botFunctions.check_command_permissions()
	async def delete_premium(self, interaction: discord.Interaction, server: str):
		# open db
		with open("./.db/multiplayer/guilds.json", "r", encoding="utf-8") as read_file: guilds_config_data = json.load(read_file)
		if not isinstance(server, int) and not server.isdigit(): return await interaction.response.send_message("Я понимаю только id сервера.", ephemeral = True)
		if str(server) not in guilds_config_data: return await interaction.response.send_message("Сервер не найден.", ephemeral = True) # проверка на наличие сервера
		privileges_0 = guilds_config_data[str(server)]["additional-features"]["privileges"][0]

		if "premium-uuid" not in privileges_0:
			if privileges_0["premium"] == False: return await interaction.response.send_message("Премиум отсутствует на этом сервере", ephemeral = True)

			privileges_0["premium"] = False

			# write db
			with open("./.db/multiplayer/guilds.json", "w", encoding="utf-8") as write_file: json.dump(guilds_config_data, write_file, ensure_ascii = False, indent = 4)

			return await interaction.response.send_message("Сервер лишен вечного премиума.", ephemeral = True)

		if privileges_0["premium"] == False: return await interaction.response.send_message("Премиум отсутствует на этом сервере", ephemeral = True)
	
		privileges_0["premium"] = False
		# open db, premium info in filedoc
		with open("./.db/info/premiumHistory.json", "r", encoding="utf-8") as read_file: premium_history_data = json.load(read_file)
		if "premium-uuid" not in premium_history_data: 
			premium_history_data[privileges_0["premium-uuid"]] = {
				"premium": privileges_0["premium"],
				"premium-time-start": privileges_0["premium-time-start"],
				"premium-time-set": privileges_0["premium-time-set"],
				"premium-time-extra": privileges_0["premium-time-extra"],
				"premium-time-extra-count": privileges_0["premium-time-extra-count"],
				"premium-time-extra-history": privileges_0["premium-time-extra-history"],
				"premium-time-total": privileges_0["premium-time-total"],
				"premium-time-end": privileges_0["premium-time-end"]
			}
		premium_history_data[privileges_0["premium-uuid"]]["premium"] = False
		premium_history_data[privileges_0["premium-uuid"]]["premium-time-end"] += " /!/ Премиум-подписка лишена"
		# write db, premium info in filedoc
		with open("./.db/info/premiumHistory.json", "w", encoding="utf-8") as write_file: json.dump(premium_history_data, write_file, ensure_ascii = False, indent = 4)

		del privileges_0["premium-uuid"]
		del privileges_0["premium-time-start"]
		del privileges_0["premium-time-set"]
		del privileges_0["premium-time-extra"]
		del privileges_0["premium-time-extra-count"]
		del privileges_0["premium-time-extra-history"]
		del privileges_0["premium-time-total"]
		del privileges_0["premium-time-end"]
		del privileges_0["premium-time-remaining"]

		# write db
		with open("./.db/multiplayer/guilds.json", "w", encoding="utf-8") as write_file: json.dump(guilds_config_data, write_file, ensure_ascii = False, indent = 4)

		#rework
		user_dmchannel = self.bot.get_user(guild_owner_id(interaction))
		await user_dmchannel.send(f'премиум подписка на сервере `{guild_name(interaction)}` закончилась', ephemeral = True)
		await interaction.response.send_message("успешно", ephemeral = True)

async def setup(bot: commands.Bot):
	await bot.add_cog(Premium(bot))