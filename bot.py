import discord
from discord.ext import commands

from datetime import datetime
import json
import os
import asyncio
import yaml

import botConfig
from dbVars import *
from botFunctions import *


bot = commands.Bot(
	command_prefix = '!',
	intents = discord.Intents.all()
)
bot.remove_command("help")

async def get_all_guilds():
	guilds = [guild.id for guild in bot.guilds]
	return guilds

@bot.event
async def on_ready():
	synced = await bot.tree.sync()
	print(f'\x1b[43m{datetime.now()}\x1b[0m Synced \x1b[35m{len(synced)}\x1b[0m commands!')


@bot.command() 
async def sync(ctx):
	synced = await bot.tree.sync()
	await ctx.send(f"Synced {len(synced)} commands!")

	guild_ids = await get_all_guilds()
	for guild_id in guild_ids: 
		copied = bot.tree.copy_global_to(guild = discord.Object(id = guild_id))
	await ctx.send(f'Copied {len(copied)} global to!')

@bot.command(aliases = ["rlc"]) 
async def reload_exts(ctx):
	if ctx.author.id not in [980175834373562439, 522136072151367691, 224632121879166976]: return await ctx.send("Нету прав.") # на автора сообщения
	for filename in os.listdir("./ext"):
		if filename.endswith(".py"):
			await bot.reload_extension(f"ext.{filename[:-3]}")
	for filename in os.listdir("./ext/modules"):
		if filename.endswith(".py"):
			await bot.reload_extension(f"ext.modules.{filename[:-3]}")

	await ctx.send(f"Успешно обновлены коги!")


print("\n".join([
	"███████ ██    ██ ██   ██ ██    ██ ███    ██  █████  ",
	"██      ██    ██ ██  ██  ██    ██ ████   ██ ██   ██ ",
	"███████ ██    ██ █████   ██    ██ ██ ██  ██ ███████ ",
	"     ██ ██    ██ ██  ██  ██    ██ ██  ██ ██ ██   ██ ",
	"███████  ██████  ██   ██  ██████  ██   ████ ██   ██ ",
	f'\x1b[37;43mVERSION\x1b[0m: \x1b[31m{botConfig.version["number"]}\x1b[0m \x1b[0m{botConfig.version["name"]}\x1b[0m'
	"\n"
]))

print("\x1b[1;34mЗагрузка когов\x1b[0m:")
async def func_load_cogs():
	for filename in os.listdir("./ext"):
		if filename.endswith(".py"):
			await bot.load_extension(f"ext.{filename[:-3]}")
			#print(f'\x1b[30;47m{datetime.now()}\x1b[0m Файл \x1b[1;32m{", ".join([filename])}\x1b[0m в коге \x1b[1;34mevents\x1b[0m загружен!') старая версия вывода
			print(f'\x1b[30;47m{datetime.now()}\x1b[0m Файл \x1b[1;32m{", ".join([filename])}\x1b[0m загружен.')
	for filename in os.listdir("./ext/modules"):
		if filename.endswith(".py"):
			await bot.load_extension(f"ext.modules.{filename[:-3]}")
			#print(f'\x1b[30;47m{datetime.now()}\x1b[0m Файл \x1b[1;32m{", ".join([filename])}\x1b[0m в коге \x1b[1;34mevents\x1b[0m загружен!') старая версия вывода
			print(f'\x1b[30;47m{datetime.now()}\x1b[0m Файл \x1b[1;32m{", ".join([filename])}\x1b[0m загружен.')


async def main():
	async with bot:
		await func_load_cogs()

		guild_ids = await get_all_guilds()
		for guild_id in guild_ids: bot.tree.copy_global_to(guild = discord.Object(id = guild_id))

		await bot.start(botConfig.token)
asyncio.run(main())