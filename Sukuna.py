import discord
from discord.ext import commands

from datetime import datetime
import json
import os
import asyncio
import yaml

from botConfig import *
from dbVars import *
import botFunctions


def get_prefix(ctx):
	with open("./.db/guildsConfiguration/guildsConfig.json", "r", encoding="utf-8") as file: return json.load(file)[str(ctx.guild.id)]["prefix"]

bot = commands.Bot(
	command_prefix = get_prefix,
	intents = discord.Intents.all()
)
#bot.remove_command("help")


@bot.event
async def on_ready():
	# await bot.change_presence(activity = discord.Game(sukuna["presence"])) включить потом
	synced = await bot.tree.sync()
	print(f"\x1b[43m{datetime.now()}\x1b[0m Успешно обновилось \x1b[35m{len(synced)}\x1b[0m команд!")


@bot.command() 
async def sync_s(ctx):
	synced = await bot.tree.sync()
	await ctx.send(f"Успешно обновилось {len(synced)} команд!")


print("\n".join([
	"███████ ██    ██ ██   ██ ██    ██ ███    ██  █████  ",
	"██      ██    ██ ██  ██  ██    ██ ████   ██ ██   ██ ",
	"███████ ██    ██ █████   ██    ██ ██ ██  ██ ███████ ",
	"     ██ ██    ██ ██  ██  ██    ██ ██  ██ ██ ██   ██ ",
	"███████  ██████  ██   ██  ██████  ██   ████ ██   ██ ",
	f"\x1b[37;43mVERSION\x1b[0m: \x1b[31m{sukuna['version']['number']}\x1b[0m \x1b[0m{sukuna['version']['name']}\x1b[0m"
	"\n"
]))

print("\x1b[1;34mЗагрузка когов\x1b[0m:")
async def func_load_cogs():
	for filename in os.listdir("./botSukunaConfiguration/cogs/events/guilds"):
		if filename.endswith(".py"):
			await bot.load_extension(f"botSukunaConfiguration.cogs.events.guilds.{filename[:-3]}")
			print(f"\x1b[30;47m{datetime.now()}\x1b[0m Файлы \x1b[1;32m{', '.join([filename])}\x1b[0m в коге \x1b[1;34mcogs/events/guilds\x1b[0m загружены!")
			#       \x1b[30;47m                \x1b[0m       \x1b[1;32m                       \x1b[0m        \x1b[1;34m                  \x1b[0m
	for filename in os.listdir("./botSukunaConfiguration/cogs/events/bot"):
		if filename.endswith(".py"):
			await bot.load_extension(f"botSukunaConfiguration.cogs.events.bot.{filename[:-3]}")
			print(f"\x1b[30;47m{datetime.now()}\x1b[0m Файлы \x1b[1;32m{', '.join([filename])}\x1b[0m в коге \x1b[1;34mcogs/events/bot\x1b[0m загружены!")
			#       \x1b[30;47m                \x1b[0m       \x1b[1;32m                       \x1b[0m        \x1b[1;34m               \x1b[0m	
	for filename in os.listdir("./botSukunaConfiguration/cogs/commands"):
		if filename.endswith(".py"):
			await bot.load_extension(f"botSukunaConfiguration.cogs.commands.{filename[:-3]}")
			print(f"\x1b[30;47m{datetime.now()}\x1b[0m Файлы \x1b[1;32m{', '.join([filename])}\x1b[0m в коге \x1b[1;34mcogs/commands\x1b[0m загружены!")
			#       \x1b[30;47m                \x1b[0m       \x1b[1;32m                       \x1b[0m        \x1b[1;34m             \x1b[0m	
	for filename in os.listdir("./botSukunaConfiguration/cogs/commands/special/"):
		if filename.endswith(".py"):
			await bot.load_extension(f"botSukunaConfiguration.cogs.commands.special.{filename[:-3]}")
			print(f"\x1b[30;47m{datetime.now()}\x1b[0m Файлы \x1b[1;32m{', '.join([filename])}\x1b[0m в коге \x1b[1;34mcogs/commands/special\x1b[0m загружены!")
			#       \x1b[30;47m                \x1b[0m       \x1b[1;32m                       \x1b[0m        \x1b[1;34m             \x1b[0m	


@bot.command(aliases = ["rlc"]) 
async def reload_cogs_s(ctx):
	# если сервер заблокирован то staff игнорируют это ограничение
	if ctx.author.id not in staff_staffList_SpecialPerms() and not guild_bot_output(ctx): return
	# команда работает только для staff с специальными правами (список staffList_SpecialPerms)
	if ctx.author.id not in staff_staffList_SpecialPerms(): return

	for filename in os.listdir("./botSukunaConfiguration/cogs/events/guilds"):
		if filename.endswith(".py"):
			await bot.reload_extension(f"botSukunaConfiguration.cogs.events.guilds.{filename[:-3]}")
	for filename in os.listdir("./botSukunaConfiguration/cogs/events/bot"):
		if filename.endswith(".py"):
			await bot.reload_extension(f"botSukunaConfiguration.cogs.events.bot.{filename[:-3]}")
	for filename in os.listdir("./botSukunaConfiguration/cogs/commands"):
		if filename.endswith(".py"):
			await bot.reload_extension(f"botSukunaConfiguration.cogs.commands.{filename[:-3]}")
	for filename in os.listdir("./botSukunaConfiguration/cogs/commands/special/"):
		if filename.endswith(".py"):
			await bot.reload_extension(f"botSukunaConfiguration.cogs.commands.special.{filename[:-3]}")

	await ctx.send(f"Успешно обновлены коги!")


async def get_all_guilds():
	guilds = [guild.id for guild in bot.guilds]
	return guilds
async def main():
	async with bot:
		await func_load_cogs()

		guild_ids = await get_all_guilds()
		for guild_id in guild_ids: bot.tree.copy_global_to(guild=discord.Object(id=guild_id))

		await bot.start(token_sukuna)
asyncio.run(main())