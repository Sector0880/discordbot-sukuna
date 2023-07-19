import discord
from discord.ext import commands

import asyncio

import yaml

import nekos
from googletrans import Translator
from datetime import *

from botConfig import (
	version as bot_version,
	languages as bot_languages,
	avatar as bot_avatar,
	colors_bot, color_success, color_error,
	emoji_mark_success, emoji_mark_error, emoji_mark_none,
	emoji_switch_on, emoji_switch_off,
	emoji_lock_unlock, emoji_lock_lock,
	emoji_load_ok, emoji_load_partial_lag, emoji_load_lag, emoji_load_none,
	emoji_db_ok, emoji_db_rework
)

from dbVars import (
	bot_presence,
	bot_switches_testers_work_commands_mention,
	bot_switches_testers_work_commands_db_info, bot_switches_testers_work_commands_update_check,
	bot_switches_output_correct, bot_switches_output_partial_sleep, bot_switches_output_emoji,
	bot_switches_message_output_delete_after,
	bot_switches_updates_mention_embs_stopwatch, bot_switches_updates_mention_embs_check,
	guild_name, guild_prefix, guild_language, guild_premium, guild_show_id, guild_tester, guild_bot_output,
	staff_owner_id,
	staff_testers_main_testers,
	staff_testers_divided_testers_for_commands_mention,
	staff_testers_divided_testers_for_commands_db_info, staff_testers_divided_testers_for_commands_update_check,
	error_switch_false_command_offed,
	error_switch_false_command_testing,
	error_command_not_found, error_server_blocked, error_invalid_language,
	error_terminal_traceback_error, error_terminal_command_error
)

class BotCommands(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	# Узнать время
	@commands.command(aliases = ['время'])
	async def time(self, ctx):
		emb = discord.Embed(title = 'Время онлаин:')
		emb.add_field(name = 'Текущее время МСК', value = (datetime.utcnow() + timedelta(hours = 3)).strftime('**Дата:** %Y.%m.%d\n**Время:** %H:%M:%S'))
		emb.add_field(name = 'Текущее время UTC', value = datetime.utcnow().strftime('**Дата:** %Y.%m.%d\n**Время:** %H:%M:%S'))
		emb.set_footer(text = ctx.author, icon_url = ctx.author.avatar.url)
		await ctx.send(embed = emb)

async def setup(bot):
	await bot.add_cog(BotCommands(bot))