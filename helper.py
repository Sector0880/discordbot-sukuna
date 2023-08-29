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


bot = commands.Bot(
	command_prefix = "!",
	intents = discord.Intents.all()
)

@bot.command() 
async def sync(ctx):
	synced_all = await bot.tree.sync()
	await ctx.send(f"Успешно обновилось {len(synced_all)} команд!")

@bot.command(aliases = ["rlc"]) 
async def reload_exts(ctx):
	# если сервер заблокирован то staff игнорируют это ограничение
	if ctx.author.id not in staff_staffList_SpecialPerms() and not guild_bot_output(ctx): return
	# команда работает только для staff с специальными правами (список staffList_SpecialPerms)
	if ctx.author.id not in staff_staffList_SpecialPerms(): return

	for filename in os.listdir("./ext/commands/for_helper"):
		if filename.endswith(".py"):
			await bot.reload_extension(f"ext.commands.for_helper.{filename[:-3]}")

	await ctx.send(f"Успешно обновлены коги!")

@bot.event
async def on_ready():
	await bot.change_presence(activity = discord.Game("Независимый отец Sukuna :3"))
	synced = await bot.tree.sync()
	print(f'\x1b[43m{datetime.now()}\x1b[0m Успешно обновилось \x1b[35m{len(synced)}\x1b[0m команд!')

print("\x1b[1;34mЗагрузка когов\x1b[0m:")
async def func_load_exts():
	for filename in os.listdir("./ext/commands/for_helper"):
		if filename.endswith(".py"):
			await bot.load_extension(f"ext.commands.for_helper.{filename[:-3]}")
			print(f'\x1b[30;47m{datetime.now()}\x1b[0m Файлы \x1b[1;32m{", ".join([filename])}\x1b[0m в коге \x1b[1;34mcommands/for_helper\x1b[0m загружены!')

async def main():
	async with bot:
		await func_load_exts()

		bot.tree.copy_global_to(guild = discord.Object(id = main_server))

		await bot.start("MTE0NDY4NzI3MzI4MDAyNDU4Ng.GSGSIN.ON70UoFs1lmEMYC7z6joSrv-BdBRsu0thK0MNg")
asyncio.run(main())