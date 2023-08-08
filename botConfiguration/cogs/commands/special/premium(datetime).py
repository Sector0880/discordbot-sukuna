# файл скоро будет готов, осталось описать его и можно выкатывать
# найдено несколько нелогичных алгоритмов, надо переписывать
import discord
from discord.ext import commands, tasks

import yaml
import json

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
	guild_owner_id,
	guild_name, guild_prefix, guild_language,
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

class Premium(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	# проверка
	@commands.command()
	async def get_premium(self, ctx, date_count: int):
		with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "r", encoding="utf-8") as read_file: guilds_config_data = json.load(read_file)
		if guilds_config_data[str(ctx.guild.id)]["additional-features"]["privileges"][0]["premium"] == False:
			guilds_config_data[str(ctx.guild.id)]["additional-features"]["privileges"][0]["premium-start-date"] = f"{datetime.now()}"
			guilds_config_data[str(ctx.guild.id)]["additional-features"]["privileges"][0]["premium-end-date"] = f"{datetime.now() + timedelta(minutes = date_count)}"
			guilds_config_data[str(ctx.guild.id)]["additional-features"]["privileges"][0]["premium"] = True
			with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "w", encoding="utf-8") as write_file: json.dump(guilds_config_data, write_file, ensure_ascii = False, indent = 4)
			sleep(0.1)
			with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "r", encoding="utf-8") as read_file: guilds_config_data = json.load(read_file)
			await ctx.send(
				f'{emoji_mark_success} Успешно, сервер получил премиум-статус на `{date_count}m`!'
				+ f'\nДата окончания премиума: `{str(guild_premium_end_date(ctx = ctx))[:-7]}`'
			)
		else:
			guilds_config_data[str(ctx.guild.id)]["additional-features"]["privileges"][0]["premium-end-date"] = f'{datetime.fromisoformat(guilds_config_data[str(ctx.guild.id)]["additional-features"]["privileges"][0]["premium-end-date"]) + timedelta(minutes = date_count)}'
			with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "w", encoding="utf-8") as write_file: json.dump(guilds_config_data, write_file, ensure_ascii = False, indent = 4)
			sleep(0.1)
			await ctx.send(
				f'{emoji_mark_success} Успешно, сервер получил продление премиум-статуса на `{date_count}m`!'
				+ f'\nОсталось: `{str(datetime.fromisoformat(guild_premium_end_date(ctx = ctx)) - datetime.now())[:-7]}`'
				+ f'\nДата окончания премиума: `{str(guild_premium_end_date(ctx = ctx))[:-7]}`'
			)

	@commands.command()
	async def delete_premium(self, ctx):
		with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "r", encoding="utf-8") as read_file: guilds_config_data = json.load(read_file)
		guilds_config_data[str(ctx.guild.id)]["additional-features"]["privileges"][0]["premium"] = False
		guilds_config_data[str(ctx.guild.id)]["additional-features"]["privileges"][0]["premium-start-date"] = None
		guilds_config_data[str(ctx.guild.id)]["additional-features"]["privileges"][0]["premium-end-date"] = None
		with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "w", encoding="utf-8") as write_file: json.dump(guilds_config_data, write_file, ensure_ascii = False, indent = 4)
		user_channel = self.bot.get_user(guild_owner_id(ctx = ctx))
		await user_channel.send(f'премиум подписка на сервере `{guild_name(ctx = ctx)}` закончилась')
		await ctx.send("успешно")

	@commands.command()
	async def delete_premium_allservers(self, ctx):
		with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "r", encoding="utf-8") as read_file: guilds_config_data = json.load(read_file)
		for guild in self.bot.guilds:
			guilds_config_data[str(guild.id)]["additional-features"]["privileges"][0]["premium"] = False
			guilds_config_data[str(guild.id)]["additional-features"]["privileges"][0]["premium-start-date"] = None
			guilds_config_data[str(guild.id)]["additional-features"]["privileges"][0]["premium-end-date"] = None
			with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "w", encoding="utf-8") as write_file: json.dump(guilds_config_data, write_file, ensure_ascii = False, indent = 4)
			user_channel = self.bot.get_user(guilds_config_data[str(guild.id)]["overview"]["owner-id"])
			await user_channel.send(f'премиум подписка на сервере `{guilds_config_data[str(guild.id)]["overview"]["guild_name"]}` закончилась')
		await ctx.send("успешно")
	
	@commands.command()
	async def check_premium(self, ctx):
		if guild_premium(ctx = ctx) == True:
			await ctx.send(f'Осталось: `{str(datetime.fromisoformat(guild_premium_end_date(ctx = ctx)) - datetime.now())[:-7]}`')
		else:
			await ctx.send("Премиум отсутствует")

	# проверка окончания премиума
	@tasks.loop(seconds = 1.0) # неувеличенное кол-во времени
	async def premium_checkdate(self):
		for guild in self.bot.guilds:
			with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "r", encoding="utf-8") as read_file: guilds_config_data = json.load(read_file)
			if guilds_config_data[str(guild.id)]["additional-features"]["privileges"][0]["premium"] == True and datetime.fromisoformat(guilds_config_data[str(guild.id)]["additional-features"]["privileges"][0]["premium-end-date"]) < datetime.now():
				with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "r", encoding="utf-8") as read_file: guilds_config_data = json.load(read_file)
				guilds_config_data[str(guild.id)]["additional-features"]["privileges"][0]["premium"] = False
				#guilds_config_data[str(guild.id)]["additional-features"]["privileges"][0]["premium-start-date"] = None
				#guilds_config_data[str(guild.id)]["additional-features"]["privileges"][0]["premium-end-date"] = None
				del guilds_config_data[str(guild.id)]["additional-features"]["privileges"][0]["premium-start-date"]
				del guilds_config_data[str(guild.id)]["additional-features"]["privileges"][0]["premium-end-date"]
				with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "w", encoding="utf-8") as write_file: json.dump(guilds_config_data, write_file, ensure_ascii = False, indent = 4)
				user_channel = self.bot.get_user(guilds_config_data[str(guild.id)]["overview"]["owner-id"])
				await user_channel.send(f'Премиум подписка на сервере `{guilds_config_data[str(guild.id)]["overview"]["guild_name"]}` закончилась')

	@commands.Cog.listener()
	async def on_ready(self):
		await self.bot.wait_until_ready()
		self.premium_checkdate.start()


async def setup(bot):
	await bot.add_cog(Premium(bot))