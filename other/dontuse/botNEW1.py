import discord
from discord.ext import commands
from discord import app_commands

from datetime import datetime
import json
import os
import asyncio
import yaml
import aiohttp

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
	emoji_db_rework, emoji_db_ok,
	token
)

class Bot(commands.Bot):
	def __init__(self):
		super().__init__(
			command_prefix = "!",
			intents = discord.Intents.all(),
			application_id = 5
		)
		self.initial_extensions = [
			"botConfiguration.cogs.commands.special.newcommands.commandsIntents"
		]

	async def setup_hook(self):
		for ext in self.initial_extensions:
			await self.load_extension(ext)
		await bot.tree.sync(guild = discord.Object(id = 1130857157215146064))
		self.session = aiohttp.ClientSession()
	
	async def close(self):
		await super().close()
		await self.session.close()

	async def on_ready(self):
		print(f"{self.user} connect!")

bot = Bot()

bot.run(token)