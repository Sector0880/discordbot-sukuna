import discord
from discord.ext import commands

import asyncio

import yaml

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
	work_functions_mention,
	work_functions_commands_db_info, work_functions_commands_update_check,
	bot_output_correct, bot_output_partial_sleep, bot_output_emoji,
	bot_message_output_delete_after,
	bot_updates_mention_embs_stopwatch, bot_updates_mention_embs_check,
	bot_testers_work_code_conditions,
	guild_name, guild_prefix, guild_language,
	guild_premium, guild_show_id, guild_tester,
	guild_bot_output,
	staff_owner_id, staff_testers_list,
	error_server_blocked, error_user_not_tester,
	error_invalid_language,
	error_terminal_traceback_error, error_terminal_command_error
)


class Cmd_update_check(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	

	@commands.command()
	@commands.is_owner()
	async def update_check(self, ctx, arg):
		if not guild_bot_output(ctx = ctx):
			if guild_language(ctx = ctx) == "ru": return await ctx.send("\n".join([
				#f"{emoji_mark_error if bot_output_emoji() else ''} **На этом сервере работоспособность бота заблокирована.**",
				error_server_blocked()["ru"]["error"]["title"].format(emoji_mark_error if bot_output_emoji() else ""),
				#f"Для разблокировки обратитесь к разработчику бота (<@{staff_owner_id() if bot_output_correct() else staff_owner_id}>)."
				error_server_blocked()["ru"]["error"]["description"].format(staff_owner_id() if bot_output_correct() else staff_owner_id)
			]))
			elif guild_language(ctx = ctx) == "uk": return await ctx.send("\n".join([
				#f"{emoji_mark_error} **На цьому сервері працездатність бота заблокована.**",
				error_server_blocked()["uk"]["error"]["title"].format(emoji_mark_error if bot_output_emoji() else ""),
				#f"Для розблокування зверніться до розробника бота (<@{staff_owner_id() if bot_output_correct() else staff_owner_id}>)."
				error_server_blocked()["uk"]["error"]["description"].format(staff_owner_id() if bot_output_correct() else staff_owner_id)
			]))
			else:
				#await ctx.send("\n".join([
					#f"{emoji_mark_error if bot_output_emoji() else ''} Стоит неподдерживаемый язык `{guild_language(ctx = ctx)}`.",
					#error_invalid_language()["ru"]["error"]["title"].format(
						#emoji_mark_error if bot_output_emoji() else "",
						#guild_language(ctx = ctx)
					#),
					#f"Языки бота: `{', '.join(bot_languages)}`."
					#error_invalid_language()["ru"]["error"]["description"].format(", ".join(bot_languages))
				#]))
				#await ctx.send("▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬ ▬")
				#return await ctx.send("\n".join([
					#f"{emoji_mark_error if bot_output_emoji() else ''} Варто підтримуваний мову `{guild_language(ctx = ctx)}`.",
					#error_invalid_language()["uk"]["error"]["title"].format(
						#emoji_mark_error if bot_output_emoji() else "",
						#guild_language(ctx = ctx)
					#),
					#f"Мови бота: `{', '.join(bot_languages)}`."
					#error_invalid_language()["uk"]["error"]["description"].format(", ".join(bot_languages))
				#]))
				await ctx.send(embed = discord.Embed(
					#title = f"{emoji_mark_error if bot_output_emoji() else ''} Стоит неподдерживаемый язык `{guild_language(ctx = ctx)}`.",
					description = "\n".join([
						error_invalid_language()["ru"]["error"]["title"].format(
							emoji_mark_error if bot_output_emoji() else "",
							guild_language(ctx = ctx)
						),
						error_invalid_language()["ru"]["error"]["description"].format(", ".join(bot_languages))
					])
				))
				return await ctx.send(embed = discord.Embed(
					#title = f"{emoji_mark_error if bot_output_emoji() else ''} Стоит неподдерживаемый язык `{guild_language(ctx = ctx)}`.",
					description = "\n".join([
						error_invalid_language()["uk"]["error"]["title"].format(
							emoji_mark_error if bot_output_emoji() else "",
							guild_language(ctx = ctx)
						),
						error_invalid_language()["uk"]["error"]["description"].format(", ".join(bot_languages))
					])
				))


		if arg in ["db_info", "di"]:
			#await ctx.send(embed = discord.Embed(description = "Никаких обновлений не запланировано."))
			await ctx.send("Никаких обновлений для команды `db_info` не запланировано.")


def setup(bot):
	bot.add_cog(Cmd_update_check(bot))