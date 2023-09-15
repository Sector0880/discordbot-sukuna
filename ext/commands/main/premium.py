import discord
from discord.ext import commands, tasks
from discord import app_commands
# не юзай блять
#from discord import Option

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

	"""
	
	# запись проверок
	@commands.hybrid_command(
		name = "delete_premium_allservers",
		description = "Удалить премиум-статус для всех серверов",
		aliases = ["dlpr_as", "pr3"],
		with_app_command = True
	)
	async def delete_premium_allservers(self, ctx):
		# если сервер заблокирован то staff игнорируют это ограничение
		if ctx.author.id not in staff_staffList_SpecialPerms() and not guild_bot_output(ctx): return await botFunctions.bot_output_blocked(ctx)
		# команда работает только для staff с специальными правами (список staffList_SpecialPerms)
		if ctx.author.id not in staff_staffList_SpecialPerms(): return await botFunctions.command_for_staff(ctx)

		for guild in self.bot.guilds:
			# open db
			with open("./.db/multiplayer/guilds.json", "r", encoding="utf-8") as read_file: guilds_config_data = json.load(read_file)
			privileges_0 = guilds_config_data[str(guild.id)]["additional-features"]["privileges"][0]  # path to privileges in server

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
			if "premium-uuid" in privileges_0: premium_history_data[privileges_0["premium-uuid"]]["premium"] = False
			# write db, premium info in filedoc
			with open("./.db/info/premiumHistory.json", "w", encoding="utf-8") as write_file: json.dump(premium_history_data, write_file, ensure_ascii = False, indent = 4)
			if "premium-uuid" in privileges_0: del privileges_0["premium-uuid"]
			if "premium-time-start" in privileges_0: del privileges_0["premium-time-start"]
			if "premium-time-set" in privileges_0: del privileges_0["premium-time-set"]
			if "premium-time-extra" in privileges_0: del privileges_0["premium-time-extra"]
			if "premium-time-extra-count" in privileges_0: del privileges_0["premium-time-extra-count"]
			if "premium-time-extra-history" in privileges_0: del privileges_0["premium-time-extra-history"]
			if "premium-time-total" in privileges_0: del privileges_0["premium-time-total"]
			if "premium-time-end" in privileges_0: del privileges_0["premium-time-end"]
			if "premium-time-remaining" in privileges_0: del privileges_0["premium-time-remaining"]

			# write db
			with open("./.db/multiplayer/guilds.json", "w", encoding="utf-8") as write_file: json.dump(guilds_config_data, write_file, ensure_ascii = False, indent = 4)

			user_dmchannel = self.bot.get_user(guilds_config_data[str(guild.id)]["overview"]["owner-id"])
			await user_dmchannel.send(f'премиум подписка на сервере `{guilds_config_data[str(guild.id)]["overview"]["guild_name"]}` закончилась')
		await ctx.send(f"Успешно.")

		
	
	# запись проверок
	@commands.hybrid_command(
		name = "delete_premium_uuid_history",
		description = "Удалить историю премиум-статусов",
		aliases = ["dlprhis", "pr4"],
		with_app_command = True
	)
	async def delete_premium_uuid_history(self, ctx):
		# если сервер заблокирован то staff игнорируют это ограничение
		if ctx.author.id not in staff_staffList_SpecialPerms() and not guild_bot_output(ctx): return await botFunctions.bot_output_blocked(ctx)
		# команда работает только для staff с специальными правами (список staffList_SpecialPerms)
		if ctx.author.id not in staff_staffList_SpecialPerms(): return await botFunctions.command_for_staff(ctx)

		# open db
		with open("./.db/multiplayer/guilds.json", "r", encoding="utf-8") as read_file: guilds_config_data = json.load(read_file)
		privileges_0 = guilds_config_data[str(ctx.guild.id)]["additional-features"]["privileges"][0]  # path to privileges in server

		if "premium-uuid-history" in privileges_0:
			del privileges_0["premium-uuid-history"]
			del privileges_0["premium-uuid-history-count"]

			# write db
			with open("./.db/multiplayer/guilds.json", "w", encoding="utf-8") as write_file: json.dump(guilds_config_data, write_file, ensure_ascii = False, indent = 4)

			# не будет использоваться т.к. ["premium-uuid"] на этот момент не будет (если сервер уже без премиума)
			# open db, premium info in filedoc
			#with open("./.db/info/premiumHistory.json", "r", encoding="utf-8") as read_file: premium_history_data = json.load(read_file)
			#del premium_history_data[privileges_0["premium-uuid"]]
			# write db, premium info in filedoc
			#with open("./.db/info/premiumHistory.json", "w", encoding="utf-8") as write_file: json.dump(premium_history_data, write_file, ensure_ascii = False, indent = 4)

			await ctx.send("Успешно")
		else: await ctx.send("Истории приобретения премиум-подписки нету")
	
	# запись проверок
	@commands.hybrid_command(
		name = "delete_premium_history_file",
		description = "Удалить архив премиум-статуса с базы данных",
		aliases = ["dlprhf", "pr6"],
		with_app_command = True
	)
	async def delete_premium_history_file(self, ctx, premium_uuid):
		# command work for staff with special permissions
		if ctx.author.id not in staff_staffList_SpecialPerms() and not guild_bot_output(ctx): return await botFunctions.bot_output_blocked(ctx)
		if ctx.author.id not in staff_staffList_SpecialPerms(): return await botFunctions.command_for_staff(ctx)

		if premium_uuid == None: return await ctx.send("Введите `premium-uuid`.")

		# open db, premium info in filedoc
		with open("./.db/info/premiumHistory.json", "r", encoding="utf-8") as read_file: premium_history_data = json.load(read_file)
		if premium_uuid not in premium_history_data: return await ctx.send("`premium-uuid` не найден.")
		del premium_history_data[str(premium_uuid)]
		# write db, premium info in filedoc
		with open("./.db/info/premiumHistory.json", "w", encoding="utf-8") as write_file: json.dump(premium_history_data, write_file, ensure_ascii = False, indent = 4)
		await ctx.send("Успешно")

	# запись проверок
	@commands.hybrid_command(
		name = "check_premium_history_file",
		description = "Проверить наличие и данные премиум-статуса, зарегестрированного в архиве",
		aliases = ["chprhf", "pr7"],
		with_app_command = True
	)
	async def check_premium_history_file(self, ctx, uuid):
		# command work for staff with special permissions
		if ctx.author.id not in staff_staffList_SpecialPerms() and not guild_bot_output(ctx): return await botFunctions.bot_output_blocked(ctx)
		if ctx.author.id not in staff_staffList_SpecialPerms(): return await botFunctions.command_for_staff(ctx)

		if uuid == None: return await ctx.send("Введите `premium-uuid`.")

		# open db, premium info in filedoc
		with open("./.db/info/premiumHistory.json", "r", encoding="utf-8") as read_file: premium_history_data = json.load(read_file)
		if not str(uuid) in premium_history_data: return await ctx.send("Неверный `premium-uuid`.")
		await ctx.send(f'```json\n{json.dumps(premium_history_data[str(uuid)], ensure_ascii = False, indent = 4)}\n```')
	
	
	@app_commands.command(
		name = "help_premium",
		description = "Получить информацию по использованию команд, входящих в линейку Premium-подписки"
	)
	@app_commands.choices(command = [
		app_commands.Choice(name = "get_premium", value = 1),
		app_commands.Choice(name = "delete_premium(NOTSUPPORTED)", value = 2),
		app_commands.Choice(name = "delete_premium_allservers(NOTSUPPORTED)", value = 3),
		app_commands.Choice(name = "delete_premium_uuid_history(NOTSUPPORTED)", value = 4),
		app_commands.Choice(name = "check_premium(NOTSUPPORTED)", value = 5),
		app_commands.Choice(name = "delete_premium_history_file(NOTSUPPORTED)", value = 6),
		app_commands.Choice(name = "check_premium_history_file(NOTSUPPORTED)", value = 7)
	])
	async def help_premium(self, interaction: discord.Interaction, command: app_commands.Choice[int] = None):
		# если сервер заблокирован то staff игнорируют это ограничение
		#if interaction.user.id not in staff_staffList_SpecialPerms() and not guild_bot_output(interaction): return await botFunctions.bot_output_blocked(interaction)
		# команда работает только для staff с специальными правами (список staffList_SpecialPerms)

		if command == None:
			emb = discord.Embed(
				title = "Команды Premium",
				description = ", ".join([
					'`get_premium`',
					'`delete_premium`',
					'`delete_premium_allservers`',
					'`delete_premium_uuid_history`',
					'`check_premium`',
					'`delete_premium_history_file`',
					'`check_premium_history_file`'
				]),
				color = 0x2b2d31
			)
		elif command.name == "get_premium":
			emb = discord.Embed(
				title = "Команда get_premium (rework)",
				description = "\n".join([
					f'**Информация:** Присвоить премиум-статус серверу.',
					'\n```ansi\nget_premium \u001b[0;31m[time*]\u001b[0;0m [server]```',
					f'**Параметры:**',
					'`time*`: Указанное кол-во секунд задаваемого премиума.',
					'`server`: При указании сервера премиум начисляется указанному серверу.'
				]),
				color = 0x2b2d31
			)
			emb.set_footer(text = "* — обязательный параметр")
		else:
			return await interaction.response.send_message("Команда не найдена.", ephemeral = True)
		await interaction.response.send_message(embed = emb, ephemeral = True)
	
		"""

	@app_commands.command(
		name = "check_premium",
		description = "Проверить премиум-статус у сервера (показывает данные с базы данных)"
	)
	@botFunctions.check_command_permissions()
	async def check_premium(self, interaction: discord.Interaction):
		# open db
		with open("./.db/multiplayer/guilds.json", "r", encoding="utf-8") as read_file: guilds_config_data = json.load(read_file)
		privileges_0 = guilds_config_data[str(interaction.guild.id)]["additional-features"]["privileges"][0]  # path to privileges in server

		emb = discord.Embed(
			title = f'Премиум на сервере: {guilds_config_data[str(interaction.guild.id)]["overview"]["guild-name"]}',
			color = 0xFFD700 if guild_premium(interaction) else 0x2b2d31
		)
		emb.add_field(
			name = "Статус",
			value= f'Осталось: `{str(datetime.fromisoformat(guild_premium_time_end(interaction)) - datetime.now())[:-7]}`' if guild_premium(interaction) else "Премиум отсутствует"
		)
		"""
		emb.add_field(
			name = "База данных",
			value = f'```ansi\n\u001b[0;33m{json.dumps(privileges_0, ensure_ascii = False, indent = 4)}\u001b[0m```',
			inline=False
		)
		"""
		await interaction.response.send_message(embed = emb, ephemeral = True)


	# запись проверок
	# проверка окончания премиума
	@tasks.loop(seconds = bot_tasks_loop_premium_check_premiumtime())
	async def premium_check_premiumtime(self):
		with open("./.db/multiplayer/guilds.json", "r", encoding="utf-8") as read_file: guilds_config_data = json.load(read_file)
		for guild in guilds_config_data.keys():
			privileges_0 = guilds_config_data[str(guild)]["additional-features"]["privileges"][0]  # path to privileges in server

			if "premium-time-end" in privileges_0:
				if datetime.fromisoformat(privileges_0["premium-time-end"]) < datetime.now():
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

					user_dmchannel = self.bot.get_user(guilds_config_data[str(guild)]["overview"]["owner-id"])
					await user_dmchannel.send(f'Премиум подписка на сервере `{guilds_config_data[str(guild)]["overview"]["guild-name"]}` закончилась')
	
	# запись проверок
	# обновление окончания времени премиума (на код не влияет, это информационная проверка)
	@tasks.loop(seconds = bot_tasks_loop_premium_change_premiumtimeremaining())
	async def premium_change_premiumtimeremaining(self):
		# open db
		with open("./.db/multiplayer/guilds.json", "r", encoding="utf-8") as read_file: guilds_config_data = json.load(read_file)
		for guild in guilds_config_data.keys():
			privileges_0 = guilds_config_data[str(guild)]["additional-features"]["privileges"][0]  # path to privileges in server

			if "premium-time-remaining" in privileges_0:
				privileges_0["premium-time-remaining"] = f'{str(datetime.fromisoformat(privileges_0["premium-time-end"]) - datetime.now())[:-7]}'

				# write db
				with open("./.db/multiplayer/guilds.json", "w", encoding="utf-8") as write_file: json.dump(guilds_config_data, write_file, ensure_ascii = False, indent = 4)

	# готово
	@commands.Cog.listener()
	async def on_ready(self):
		await self.bot.wait_until_ready()
		self.premium_check_premiumtime.start()
		self.premium_change_premiumtimeremaining.start()


async def setup(bot: commands.Bot):
	await bot.add_cog(Premium(bot))