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

# инициализация бота
bot = commands.AutoShardedBot(
	shard_count = 1,
	command_prefix = get_bot_prefix,
	intents = discord.Intents.all(),
	help_command=None
)

@bot.event
async def on_ready():
	await bot.change_presence(status = discord.Status.online, activity=discord.Game(bot_presence()))
	synced = await bot.tree.sync()
	print(f'\x1b[43m{datetime.now()}\x1b[0m Добавилась(-ись) \x1b[35m{len(synced)}\x1b[0m команд(-ы)!')

async def get_all_guilds():
	guilds = [guild.id for guild in bot.guilds]
	return guilds

@bot.command()
async def sync(ctx):
	synced = await bot.tree.sync()
	await ctx.send(f"Добавилась(-ись) {len(synced)} команд(-ы)!")

	guild_ids = await get_all_guilds()
	for guild_id in guild_ids: 
		copied = bot.tree.copy_global_to(guild = discord.Object(id = guild_id))
	await ctx.send(f'Copied {len(copied)} global to!')

@bot.command(aliases = ["rle", 'рле']) 
async def reload_exts(ctx):
	try:
		if ctx.author.id not in sf_sp(): return await ctx.send("Нету прав.") # на автора сообщения сообщения
		for filename in os.listdir("./ext"):
			if filename.endswith(".py"):
				await bot.reload_extension(f"ext.{filename[:-3]}")
				print(f'\x1b[30;47m{datetime.now()}\x1b[0m Файл \x1b[1;32m{", ".join([filename])}\x1b[0m перезагружен.')
		for filename in os.listdir("./ext/modules"):
			if filename.endswith(".py"):
				await bot.reload_extension(f"ext.modules.{filename[:-3]}")
				print(f'\x1b[30;47m{datetime.now()}\x1b[0m Файл \x1b[1;32m{", ".join([filename])}\x1b[0m перезагружен.')
		for filename in os.listdir("./ext/modules/special"):
			if filename.endswith(".py"):
				await bot.reload_extension(f"ext.modules.special.{filename[:-3]}")
				print(f'\x1b[30;47m{datetime.now()}\x1b[0m Файл \x1b[1;32m{", ".join([filename])}\x1b[0m перезагружен.')

		await ctx.send(f"Успешно обновлены коги!")
	except Exception as e:
		print(e)

print("\n".join([
	"███████ ██    ██ ██   ██ ██    ██ ███    ██  █████  ",
	"██      ██    ██ ██  ██  ██    ██ ████   ██ ██   ██ ",
	"███████ ██    ██ █████   ██    ██ ██ ██  ██ ███████ ",
	"     ██ ██    ██ ██  ██  ██    ██ ██  ██ ██ ██   ██ ",
	"███████  ██████  ██   ██  ██████  ██   ████ ██   ██ ",
	f'\x1b[37;43mVERSION\x1b[0m: \x1b[31m{botConfig.version["number"]}\x1b[0m \x1b[0m{botConfig.version["name"]}\x1b[0m'
	"\n"
]))

async def func_load_cogs():
	for filename in os.listdir("./ext"):
		if filename.endswith(".py"):
			await bot.load_extension(f"ext.{filename[:-3]}")
			print(f'\x1b[30;47m{datetime.now()}\x1b[0m Файл \x1b[1;32m{", ".join([filename])}\x1b[0m загружен.')
	for filename in os.listdir("./ext/modules"):
		if filename.endswith(".py"):
			await bot.load_extension(f"ext.modules.{filename[:-3]}")
			print(f'\x1b[30;47m{datetime.now()}\x1b[0m Файл \x1b[1;32m{", ".join([filename])}\x1b[0m загружен.')
	for filename in os.listdir("./ext/modules/special"):
		if filename.endswith(".py"):
			await bot.load_extension(f"ext.modules.special.{filename[:-3]}")
			print(f'\x1b[30;47m{datetime.now()}\x1b[0m Файл \x1b[1;32m{", ".join([filename])}\x1b[0m загружен.')

async def main():
	async with bot:
		print("\x1b[1;34mЗагрузка когов\x1b[0m:")
		await func_load_cogs()

		guild_ids = await get_all_guilds()
		for guild_id in guild_ids: bot.tree.copy_global_to(guild = discord.Object(id = guild_id))

		await bot.start(botConfig.token)
asyncio.run(main())