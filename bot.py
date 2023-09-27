import discord
from discord.ext import commands

from datetime import datetime
import json
import os
import asyncio
import yaml

from botConfig import *
from dbVars import *
import botDecorators



bot = commands.Bot(
	command_prefix = botDecorators.get_prefix,
	intents = discord.Intents.all()
)
#bot.remove_command("help")

@bot.event
async def on_ready():
	synced = await bot.tree.sync()
	print(f'\x1b[43m{datetime.now()}\x1b[0m Synced \x1b[35m{len(synced)}\x1b[0m commands!')


@bot.command() 
async def sync(ctx):
	synced = await bot.tree.sync()
	await ctx.send(f"Synced {len(synced)} commands!")

@bot.command(aliases = ["rlc"]) 
async def reload_exts(ctx):
	# если сервер заблокирован то staff игнорируют это ограничение
	#if ctx.author.id not in staff_staffList_SpecialPerms() and not guild_bot_output(ctx): return
	# команда работает только для staff с специальными правами (список staffList_SpecialPerms)
	#if ctx.author.id not in staff_staffList_SpecialPerms(): return

	for filename in os.listdir("./ext/events"):
		if filename.endswith(".py"):
			await bot.reload_extension(f"ext.events.{filename[:-3]}")
	for filename in os.listdir("./ext/commands/main"):
		if filename.endswith(".py"):
			await bot.reload_extension(f"ext.commands.main.{filename[:-3]}")

	await ctx.send(f"Успешно обновлены коги!")


print("\n".join([
	"███████ ██    ██ ██   ██ ██    ██ ███    ██  █████  ",
	"██      ██    ██ ██  ██  ██    ██ ████   ██ ██   ██ ",
	"███████ ██    ██ █████   ██    ██ ██ ██  ██ ███████ ",
	"     ██ ██    ██ ██  ██  ██    ██ ██  ██ ██ ██   ██ ",
	"███████  ██████  ██   ██  ██████  ██   ████ ██   ██ ",
	f'\x1b[37;43mVERSION\x1b[0m: \x1b[31m{version["number"]}\x1b[0m \x1b[0m{version["name"]}\x1b[0m'
	"\n"
]))

print("\x1b[1;34mЗагрузка когов\x1b[0m:")
async def func_load_cogs():
	for filename in os.listdir("./ext/events"):
		if filename.endswith(".py"):
			await bot.load_extension(f"ext.events.{filename[:-3]}")
			print(f'\x1b[30;47m{datetime.now()}\x1b[0m Файлы \x1b[1;32m{", ".join([filename])}\x1b[0m в коге \x1b[1;34mevents\x1b[0m загружены!')
	#for filename in os.listdir("./ext/commands/main"):
		#if filename.endswith(".py"):
			#await bot.load_extension(f"ext.commands.main.{filename[:-3]}")
			#print(f'\x1b[30;47m{datetime.now()}\x1b[0m Файлы \x1b[1;32m{", ".join([filename])}\x1b[0m в коге \x1b[1;34mcommands/main\x1b[0m загружены!')

async def get_all_guilds():
	guilds = [guild.id for guild in bot.guilds]
	return guilds
async def main():
	async with bot:
		await func_load_cogs()

		guild_ids = await get_all_guilds()
		for guild_id in guild_ids: bot.tree.copy_global_to(guild = discord.Object(id = guild_id))

		await bot.start(token)
asyncio.run(main())