import discord
from discord.ext import commands

from datetime import *
import random
import asyncio
import traceback

# Импорты всех данных с botConfig:
from botConfig import (
	info as bot_info, version as bot_version, avatar as bot_avatar, languages as bot_languages,
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
	guild_name, guild_prefix, guild_language,
	guild_premium,
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


class BotEvents(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_message(self, message):
		try:
			# блокировка ответа в лс
			if isinstance(message.channel, discord.DMChannel) or message.author.bot: return

			# ответ если произошел @пинг
			if self.bot.user.mention in message.content or f"<@!{self.bot.user.id}>" in message.content:
				bot_name = self.bot.user.name

				def status():
					ping = f"{round(self.bot.latency * 1000)}ms"

					if self.bot.latency > 0.25000000000000000: return f"{emoji_load_partial_lag} `{ping}`"
					if self.bot.latency > 0.35000000000000000: return f"{emoji_load_lag} `{ping}`"
					return f"{emoji_load_ok} `{ping}`"

				
				embs_title = {
					"title": f"Карта бота (БУДУ РЕВАМПАТЬ)",
					"description": f"Основные данные бота на сервере **{guild_name(ctx = message)}**.",
					"color": random.choice(colors_bot)
				}

				emb_1 = discord.Embed(
					title = embs_title["title"],
					description = embs_title["description"],
					color = embs_title["color"]
				)

				emb_1.add_field(
					name = "Настройки",
					value = "\n".join([
						f"**Префикс:** loading(gif_emoji) `...`",
							"**Язык:** loading(gif_emoji) `...`"
					])
				)
				emb_1.add_field(
					name = "Состояние",
					value = "\n".join([
						f"**Пинг:** loading(gif_emoji) `...ms`",
						f"**База данных:** loading(gif_emoji) `None`"
					])
				)
				emb_1.add_field(
					name = "Расширенные возможности",
					value = f"**Nexus +:** loading(gif_emoji) `None`"
						+ f"\n**Просмотр ID:** loading(gif_emoji) `None`"
						+ f"\n**Моды:** loading(gif_emoji) `None`",
					inline = False
				)

				emb_2 = discord.Embed(
					title = embs_title["title"],
					description = embs_title["description"],
					color = embs_title["color"]
				)

				emb_3 = discord.Embed(
					title = embs_title["title"],
					description = embs_title["description"],
					color = embs_title["color"]
				)

				for embs in [emb_2, emb_3]:
					embs.add_field(
						name = "Настройки",
						value = "\n".join([
							f"**Префикс:** `{guild_prefix(ctx = message)}`",
							f"**Язык:** :flag_ru: Русский"
						])
					)
					embs.add_field(
						name = "Состояние",
						value = "\n".join([
							f"**Пинг:** {status()}",
							"**Шард:** #1. Obscura",
							#f"**База данных:** {(f'{emoji_db_ok} `OK`' if bot_switches_output_emoji() else '`OK`') if bot_switches_output_correct() else 'None'}"
							#f"**БД сервера(бета):** "
							#+ (
								#f"{emoji_db_rework} `CODE REWRITING`" if bot_switches_output_emoji() else "`OK`"
							#) if bot_switches_output_correct() else "None"
						])
					)
					embs.add_field(
						name = "Расширенные возможности",
						value = "\n".join([
							#f"**Nexus +:** {((f'{emoji_lock_unlock} Доступен' if bot_switches_output_emoji() else 'Доступен') if guild_premium(ctx = message) else (f'{emoji_lock_lock} Недоступен' if bot_switches_output_emoji() else 'Недоступен')) if bot_switches_output_correct() else guild_premium}",
							f"**Nexus +:** "
							+ (
								(
									f"{emoji_lock_unlock} Доступен"
								) if guild_premium(ctx = message) else (
									f"{emoji_lock_lock} Недоступен"
								)
							),
							#f"**Просмотр ID:** {(f'{emoji_switch_on if bot_switches_output_emoji() else ''} Включен' if guild_show_id(ctx = message) else f'{emoji_switch_off if bot_switches_output_emoji() else ''} Выключен') if bot_switches_output_correct() else guild_show_id}",
							f"**Просмотр ID:** "
							+ (
								(
									f"{emoji_switch_on} Включен"
								) if guild_show_id(ctx = message) else (
									f"{emoji_switch_off} Выключен"
								)
							),
							#f"**Моды (ревамп):** {('tester' if guild_tester(ctx = message) else 'Отсутствуют') if bot_switches_output_correct() else guild_tester}"
							f"**Моды (ревамп):** "
							+ (
								"Отсутствуют"
							)
						]),
						inline = False
					)

				emb_2.set_footer(text = "Используйте реакции для выполнения базовых команд (не законченная функция).")

				emb_3.set_footer(text = "Время вышло (10s).")
				#elif guild_language(ctx = message) == "uk":
				
				for embs in [emb_2, emb_3]:
					embs.set_thumbnail(url = bot_avatar)


				msg = await message.channel.send(embed = emb_1)
				await msg.edit(embed = emb_2)
				await msg.add_reaction(emoji_mark_none)


				try: await self.bot.wait_for("reaction_add", timeout = 10.0, check = lambda r, u: str(r.emoji) == emoji_mark_none and not u.bot and u.id == message.author.id)
				except asyncio.TimeoutError: await msg.edit(embed = emb_3)
				else:
					if guild_language(ctx = message) == "ru": await message.channel.send("Быстрый доступ разрабатывается, просим немного подождать.")
					elif guild_language(ctx = message) == "uk": await message.channel.send("Швидкий доступ розробляється, просимо трохи почекати.")
					else:
						await message.channel.send(embed = discord.Embed(
							description = "\n".join([
								error_invalid_language()["ru"]["error"]["description1"].format(
									emoji_mark_error,
									guild_language(ctx = message)
								),
								error_invalid_language()["ru"]["error"]["description2"].format(", ".join(bot_languages))
							]),
							color = color_error
						))
						return await message.channel.send(embed = discord.Embed(
							description = "\n".join([
								error_invalid_language()["uk"]["error"]["description1"].format(
									emoji_mark_error,
									guild_language(ctx = message)
								),
								error_invalid_language()["uk"]["error"]["description2"].format(", ".join(bot_languages))
							]),
							color = color_error
						))
		except:
			if guild_language(ctx = message) == "ru": await message.channel.send(error_terminal_traceback_error()["ru"]["error"]["output"].format(traceback.format_exc()))
			elif guild_language(ctx = message) == "uk": await message.channel.send(error_terminal_traceback_error()["uk"]["error"]["output"].format(traceback.format_exc()))
			else:
				await message.channel.send(embed = discord.Embed(
					description = "\n".join([
						#title = f"{emoji_mark_error if bot_switches_output_emoji() else ''} Стоит неподдерживаемый язык `{guild_language(ctx = message)}`.",
						error_invalid_language()["ru"]["error"]["description1"].format(
							emoji_mark_error,
							guild_language(ctx = message)
						),
						#f"Языки бота: `{', '.join(bot_languages)}`."
						error_invalid_language()["ru"]["error"]["description2"].format(", ".join(bot_languages))
					]),
					color = color_error
				))
				return await message.channel.send(embed = discord.Embed(
					description = "\n".join([
						#title = f"{emoji_mark_error if bot_switches_output_emoji() else ''} Варто підтримуваний мову `{guild_language(ctx = message)}`.",
						error_invalid_language()["uk"]["error"]["description1"].format(
							emoji_mark_error,
							guild_language(ctx = message)
						),
						#f"Мови бота: `{', '.join(bot_languages)}`."
						error_invalid_language()["uk"]["error"]["description2"].format(", ".join(bot_languages))
					]),
					color = color_error
				))


	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		try:
			if isinstance(ctx.channel, discord.DMChannel): return


			if not guild_bot_output(ctx ):
				if guild_language(ctx) == "ru": return await ctx.send(
					embed = discord.Embed(
						description = "\n".join([
							#f"{emoji_mark_error if bot_switches_output_emoji() else ''} **На этом сервере работоспособность бота заблокирована.**",
							error_server_blocked()["ru"]["error"]["description1"].format(emoji_mark_error),
							#f"Для разблокировки обратитесь к разработчику бота (<@{staff_owner_id() if bot_switches_output_correct() else staff_owner_id}>)."
							error_server_blocked()["ru"]["error"]["description2"].format(staff_creator_id())
						]),
						color = color_error
					)
				)
				elif guild_language(ctx) == "uk": return await ctx.send(
					embed = discord.Embed(
						description = "\n".join([
							#f"{emoji_mark_error} **На цьому сервері працездатність бота заблокована.**",
							error_server_blocked()["uk"]["error"]["description1"].format(emoji_mark_error),
							#f"Для розблокування зверніться до розробника бота (<@{staff_owner_id() if bot_switches_output_correct() else staff_owner_id}>)."
							error_server_blocked()["uk"]["error"]["description2"].format(staff_creator_id())
						]),
						color = color_error
					)
				)
				else:
					await ctx.send(embed = discord.Embed(
						description = "\n".join([
							error_invalid_language()["ru"]["error"]["description1"].format(
								emoji_mark_error,
								guild_language(ctx)
							),
							error_invalid_language()["ru"]["error"]["description2"].format(", ".join(bot_languages))
						]),
						color = color_error
					))
					return await ctx.send(embed = discord.Embed(
						description = "\n".join([
							error_invalid_language()["uk"]["error"]["description1"].format(
								emoji_mark_error,
								guild_language(ctx)
							),
							error_invalid_language()["uk"]["error"]["description2"].format(", ".join(bot_languages))
						]),
						color = color_error
					))


			if isinstance(error, commands.CommandNotFound):
				if guild_language(ctx = ctx) == "ru":
					return await ctx.send(embed = discord.Embed(
						description = "\n".join([
							#f"{emoji_mark_error} **Команда** `{ctx.invoked_with}` {f'**вместе с аргументом(ами)** `{ctx.args}`' if ctx.args else ''} **не найдена.**",
							error_command_not_found()["ru"]["error"]["description1"].format(
								emoji_mark_error,
								ctx.invoked_with
							),
							#f"Выполните команду `{guild_prefix(ctx = ctx)}хелп` чтобы получить список команд."
							#error_command_not_found()["ru"]["error"]["description2"].format(guild_prefix(ctx = ctx) if bot_switches_output_correct() else guild_prefix)
							#f"Пока не будет разработана команда `{guild_prefix(ctx = ctx) if bot_switches_output_correct() else guild_prefix}хелп` просим связаться с разработчиком бота (<@{staff_owner_id() if bot_switches_output_correct() else staff_owner_id}>) для получения списка команд."
							error_command_not_found()["ru"]["error"]["description2"].format(
								guild_prefix(ctx = ctx),
								staff_creator_id()
							)
						]),
						color = color_error
					))
				elif guild_language(ctx = ctx) == "uk":
					return await ctx.send(embed = discord.Embed(
						description = "\n".join([
							#f"{emoji_mark_error} **Команда** `{ctx.invoked_with}` {f'**разом з аргументом(ами)** `{ctx.args}`' if ctx.args else ''} **не знайдено.**",
							error_command_not_found()["uk"]["error"]["description1"].format(
								emoji_mark_error,
								ctx.invoked_with
							),
							#f"Виконайте команду `{guild_prefix(ctx = ctx)} хелп` щоб отримати список команд."
							#error_command_not_found()["ru"]["error"]["description2"].format(guild_prefix(ctx = ctx) if bot_switches_output_correct() else guild_prefix)
							#f"Поки не буде розроблена команда `{guild_prefix(ctx = ctx) if bot_switches_output_correct() else guild_prefix}хелп` просимо зв'язатися з розробником бота (<@{staff_owner_id() if bot_switches_output_correct() else staff_owner_id}>) для отримання списку команд."
							error_command_not_found()["uk"]["error"]["description2"].format(
								guild_prefix(ctx = ctx),
								staff_creator_id()
							)
						]),
						color = color_error
					))
				else:
					await ctx.send(embed = discord.Embed(
						description = "\n".join([
							#title = f"{emoji_mark_error if bot_switches_output_emoji() else ''} Стоит неподдерживаемый язык `{guild_language(ctx = ctx)}`.",
							error_invalid_language()["ru"]["error"]["description1"].format(
								emoji_mark_error,
								guild_language(ctx = ctx)
							),
							#f"Языки бота: `{', '.join(bot_languages)}`."
							error_invalid_language()["ru"]["error"]["description2"].format(", ".join(bot_languages))
						]),
						color = color_error
					))
					return await ctx.send(embed = discord.Embed(
						description = "\n".join([
							#title = f"{emoji_mark_error if bot_switches_output_emoji() else ''} Варто підтримуваний мову `{guild_language(ctx = ctx)}`.",
							error_invalid_language()["uk"]["error"]["description1"].format(
								emoji_mark_error,
								guild_language(ctx = ctx)
							),
							#f"Мови бота: `{', '.join(bot_languages)}`."
							error_invalid_language()["uk"]["error"]["description2"].format(", ".join(bot_languages))
						]),
						color = color_error
					))

			if isinstance(error, commands.CommandError):
				if guild_language(ctx = ctx) == "ru":
					await ctx.send("Неаргументированная ошибка перехвачена:")
					await ctx.send(error_terminal_traceback_error()["ru"]["error"]["output"].format(traceback.format_exc()))
					await ctx.send("_ _")
					await ctx.send(error_terminal_command_error()["ru"]["error"]["output"].format(error))
				elif guild_language(ctx = ctx) == "uk":
					await ctx.send("Неаргументована помилка перехоплена:")
					await ctx.send(error_terminal_traceback_error()["uk"]["error"]["output"].format(traceback.format_exc()))
					await ctx.send("_ _")
					await ctx.send(error_terminal_command_error()["uk"]["error"]["output"].format(error))
				else:
					await ctx.send(embed = discord.Embed(
						description = "\n".join([
							#title = f"{emoji_mark_error if bot_switches_output_emoji() else ''} Стоит неподдерживаемый язык `{guild_language(ctx = ctx)}`.",
							error_invalid_language()["ru"]["error"]["description1"].format(
								emoji_mark_error,
								guild_language(ctx = ctx)
							),
							#f"Языки бота: `{', '.join(bot_languages)}`."
							error_invalid_language()["ru"]["error"]["description2"].format(", ".join(bot_languages))
						]),
						color = color_error
					))
					return await ctx.send(embed = discord.Embed(
						description = "\n".join([
							#title = f"{emoji_mark_error if bot_switches_output_emoji() else ''} Варто підтримуваний мову `{guild_language(ctx = ctx)}`.",
							error_invalid_language()["uk"]["error"]["description1"].format(
								emoji_mark_error,
								guild_language(ctx = ctx)
							),
							#f"Мови бота: `{', '.join(bot_languages)}`."
							error_invalid_language()["uk"]["error"]["description2"].format(", ".join(bot_languages))
						]),
						color = color_error
					))
		except:
			if guild_language(ctx = ctx) == "ru": await ctx.send(error_terminal_traceback_error()["ru"]["error"]["output"].format(traceback.format_exc()))
			elif guild_language(ctx = ctx) == "uk": await ctx.send(error_terminal_traceback_error()["uk"]["error"]["output"].format(traceback.format_exc()))
			else:
				await ctx.send(embed = discord.Embed(
					description = "\n".join([
						#title = f"{emoji_mark_error if bot_switches_output_emoji() else ''} Стоит неподдерживаемый язык `{guild_language(ctx = ctx)}`.",
						error_invalid_language()["ru"]["error"]["description1"].format(
							emoji_mark_error,
							guild_language(ctx = ctx)
						),
						#f"Языки бота: `{', '.join(bot_languages)}`."
						error_invalid_language()["ru"]["error"]["description2"].format(", ".join(bot_languages))
					]),
					color = color_error
				))
				return await ctx.send(embed = discord.Embed(
					description = "\n".join([
						#title = f"{emoji_mark_error if bot_switches_output_emoji() else ''} Варто підтримуваний мову `{guild_language(ctx = ctx)}`.",
						error_invalid_language()["uk"]["error"]["description1"].format(
							emoji_mark_error,
							guild_language(ctx = ctx)
						),
						#f"Мови бота: `{', '.join(bot_languages)}`."
						error_invalid_language()["uk"]["error"]["description2"].format(", ".join(bot_languages))
					]),
					color = color_error
				))
	
	#@commands.Cog.listener()
	#async def on_command(self, message):
		#if not guild_bot_output(ctx = message):
			#if guild_language(ctx = message) == "ru": return await message.channel.send(
				#embed = discord.Embed(
					#description = "\n".join([
						#f"{emoji_mark_error if bot_switches_output_emoji() else ''} **На этом сервере работоспособность бота заблокирована.**",
						#error_server_blocked()["ru"]["error"]["description1"].format(emoji_mark_error if bot_switches_output_emoji() else ""),
						#f"Для разблокировки обратитесь к разработчику бота (<@{staff_owner_id() if bot_switches_output_correct() else staff_owner_id}>)."
						#error_server_blocked()["ru"]["error"]["description2"].format(staff_owner_id() if bot_switches_output_correct() else staff_owner_id)
					#]),
					#color = color_error
				#)
			#)
			#elif guild_language(ctx = message) == "uk": return await message.channel.send(
				#embed = discord.Embed(
					#description = "\n".join([
						#f"{emoji_mark_error} **На цьому сервері працездатність бота заблокована.**",
						#error_server_blocked()["uk"]["error"]["description1"].format(emoji_mark_error if bot_switches_output_emoji() else ""),
						#f"Для розблокування зверніться до розробника бота (<@{staff_owner_id() if bot_switches_output_correct() else staff_owner_id}>)."
						#error_server_blocked()["uk"]["error"]["description2"].format(staff_owner_id() if bot_switches_output_correct() else staff_owner_id)
					#]),
					#color = color_error
				#)
			#)
			#else:
				#await message.channel.send(embed = discord.Embed(
					#description = "\n".join([
						#title = f"{emoji_mark_error if bot_switches_output_emoji() else ''} Стоит неподдерживаемый язык `{guild_language(ctx = message)}`.",
						#error_invalid_language()["ru"]["error"]["description1"].format(
							#emoji_mark_error if bot_switches_output_emoji() else "",
							#guild_language(ctx = message)
						#),
						#f"Языки бота: `{', '.join(bot_languages)}`."
						#error_invalid_language()["ru"]["error"]["description2"].format(", ".join(bot_languages))
					#]),
					#color = color_error
				#))
				#return await message.channel.send(embed = discord.Embed(
					#description = "\n".join([
						#title = f"{emoji_mark_error if bot_switches_output_emoji() else ''} Варто підтримуваний мову `{guild_language(ctx = message)}`.",
						#error_invalid_language()["uk"]["error"]["description1"].format(
							#emoji_mark_error if bot_switches_output_emoji() else "",
							#guild_language(ctx = message)
						#),
						#f"Мови бота: `{', '.join(bot_languages)}`."
						#error_invalid_language()["uk"]["error"]["description2"].format(", ".join(bot_languages))
					#]),
					#color = color_error
				#))


	@commands.Cog.listener()
	async def on_ready(self):
		await self.bot.change_presence(status = discord.Status.online, activity = discord.Game(bot_activity()))

		print("\n".join([
			"/ " *20,
			f"\x1b[30;47m{datetime.now()}\x1b[0m {self.bot.user} успешно запустился!"
			# \x1b[30;47m                \x1b[0m
		]))


async def setup(bot):
	await bot.add_cog(BotEvents(bot))