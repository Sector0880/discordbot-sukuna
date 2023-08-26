import discord
from discord.ext import commands

from datetime import datetime
import json
import os
import asyncio
import yaml

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
	emoji_db_rework, emoji_db_ok
)


# получаем префикс
def get_prefix(bot, ctx):
	with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "r", encoding="utf-8") as file: return json.load(file)[str(ctx.guild.id)]["prefix"]

bot = commands.AutoShardedBot(
	command_prefix = get_prefix,
	case_insensitive = True,
	shard_count = 1,
	intents = discord.Intents.all()
)
bot.remove_command("help")

print("\n".join([
	"███████ ██    ██ ██   ██ ██    ██ ███    ██  █████  ",
	"██      ██    ██ ██  ██  ██    ██ ████   ██ ██   ██ ",
	"███████ ██    ██ █████   ██    ██ ██ ██  ██ ███████ ",
	"     ██ ██    ██ ██  ██  ██    ██ ██  ██ ██ ██   ██ ",
	"███████  ██████  ██   ██  ██████  ██   ████ ██   ██ ",
	f"\x1b[37;43mVERSION\x1b[0m: \x1b[31m{bot_version['number']}\x1b[0m \x1b[0m{bot_version['name']}\x1b[0m"
	 #\x1b[37;43m       \x1b[0m  \x1b[31m                       \x1b[0m \x1b[0m                     \x1b[0m
	"\n"
]))



print("\x1b[1;34mЗагрузка когов\x1b[0m:")
#      \x1b[1;34m            \x1b[0m
async def func_load_cogs():
	#[bot.load_extension(f"cogs.events.guilds.{filename[:-3]}") for filename in os.listdir("./cogs/events/guilds") if filename.endswith(".py")]
	for filename in os.listdir("./botConfiguration/cogs/events/guilds"):
		if filename.endswith(".py"):
			await bot.load_extension(f"botConfiguration.cogs.events.guilds.{filename[:-3]}")
			print(f"\x1b[30;47m{datetime.now()}\x1b[0m Файлы \x1b[1;32m{', '.join([filename])}\x1b[0m в коге \x1b[1;34mcogs/events/guilds\x1b[0m загружены!")
			#       \x1b[30;47m                \x1b[0m       \x1b[1;32m                       \x1b[0m        \x1b[1;34m                  \x1b[0m
	for filename in os.listdir("./botConfiguration/cogs/events/bot"):
		if filename.endswith(".py"):
			await bot.load_extension(f"botConfiguration.cogs.events.bot.{filename[:-3]}")
			print(f"\x1b[30;47m{datetime.now()}\x1b[0m Файлы \x1b[1;32m{', '.join([filename])}\x1b[0m в коге \x1b[1;34mcogs/events/bot\x1b[0m загружены!")
			#       \x1b[30;47m                \x1b[0m       \x1b[1;32m                       \x1b[0m        \x1b[1;34m               \x1b[0m	
	for filename in os.listdir("./botConfiguration/cogs/commands"):
		if filename.endswith(".py"):
			await bot.load_extension(f"botConfiguration.cogs.commands.{filename[:-3]}")
			print(f"\x1b[30;47m{datetime.now()}\x1b[0m Файлы \x1b[1;32m{', '.join([filename])}\x1b[0m в коге \x1b[1;34mcogs/commands\x1b[0m загружены!")
			#       \x1b[30;47m                \x1b[0m       \x1b[1;32m                       \x1b[0m        \x1b[1;34m             \x1b[0m	
	for filename in os.listdir("./botConfiguration/cogs/commands/special/newcommands"):
		if filename.endswith(".py"):
			await bot.load_extension(f"botConfiguration.cogs.commands.special.{filename[:-3]}")
			print(f"\x1b[30;47m{datetime.now()}\x1b[0m Файлы \x1b[1;32m{', '.join([filename])}\x1b[0m в коге \x1b[1;34mcogs/commands/special\x1b[0m загружены!")
			#       \x1b[30;47m                \x1b[0m       \x1b[1;32m                       \x1b[0m        \x1b[1;34m             \x1b[0m	

async def main():
	async with bot:
		await func_load_cogs()
		await bot.start("MTEzMDkwNDE3MDExNTkwNzcxNw.GxNjxy.ZK8TOkncBQGb7bzyIPXEwPB1HuHZ4amhdp7W8E")
asyncio.run(main())