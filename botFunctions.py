import discord
from discord.ext import commands
import yaml
from datetime import datetime
import sys

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

# работает
async def command_counter(ctx):
	#command = ctx.invoked_with
	command = ctx.command.name # работает лучше
	with open("./botConfiguration/.db/info/commandsCount.yml", "r") as read_file: commandsInfo = yaml.safe_load(read_file)
	commandsInfo["all"] += 1 # все команды
	commandsInfo[command] += 1 # вызываемая команда
	with open("./botConfiguration/.db/info/commandsCount.yml", "w") as write_file: yaml.safe_dump(commandsInfo, write_file, sort_keys = False, allow_unicode = True)

# работает
async def bot_output_blocked(ctx):
	emb = discord.Embed(
		description = "\n".join([
			error_server_blocked()[guild_language(ctx)]["error"]["description1"].format(emoji_mark_error),
			error_server_blocked()[guild_language(ctx)]["error"]["description2"].format(staff_creator_id())
		]),
		color = color_error,
		timestamp = datetime.now()
	)
	emb.set_image(url = "https://cdn.discordapp.com/attachments/817101575289176064/1137345466875518986/black__200px.gif")
	emb.set_footer(text = ctx.author.name, icon_url = ctx.author.avatar)
	await ctx.send(embed = emb)

async def command_for_staff(ctx):
	await ctx.send(f"{emoji_mark_error} Команда предназначена только для определенных лиц, относящихся к разработке бота.")