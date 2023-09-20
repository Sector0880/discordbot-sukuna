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


class PremiumEvents(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
	
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
	await bot.add_cog(PremiumEvents(bot))