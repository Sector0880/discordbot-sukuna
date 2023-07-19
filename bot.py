import discord
from discord.ext import commands

from datetime import datetime
import json
import os
import asyncio

from botConfig import (version as bot_version)


def get_prefix(bot, ctx):
	with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "r", encoding="utf-8") as file: return json.load(file)[str(ctx.guild.id)]["prefix"]

bot = commands.AutoShardedBot(
	command_prefix=get_prefix,
	case_insensitive=True,
	shard_count=1,
	intents=discord.Intents.all()
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
async def funt_load_cogs():
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


async def main():
	async with bot:
		await funt_load_cogs()
		await bot.start("MTEzMDkwNDE3MDExNTkwNzcxNw.GxNjxy.ZK8TOkncBQGb7bzyIPXEwPB1HuHZ4amhdp7W8E")

asyncio.run(main())