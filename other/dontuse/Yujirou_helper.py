import discord
from discord.ext import commands

from datetime import datetime
import json
import os
import asyncio
import yaml

from botsConfig import *
from dbVars import *
import botsFunctions


# получаем префикс
def get_prefix(ctx):
	with open("./.db/multiplayer/guilds.json", "r", encoding="utf-8") as file: return json.load(file)[str(ctx.guild.id)]["prefix"]

bot = commands.Bot(
	command_prefix = get_prefix,
	intents = discord.Intents.all()
)
#bot.remove_command("help")


@bot.event
async def on_ready():
	await bot.change_presence(activity = discord.Game(yujirou["presence"]))
	synced = await bot.tree.sync()
	print(f"\x1b[43m{datetime.now()}\x1b[0m Успешно обновилось \x1b[35m{len(synced)}\x1b[0m команд!")

@bot.command() 
async def sync_y(ctx):
	synced = await bot.tree.sync()
	await ctx.send(f"Успешно обновилось {len(synced)} команд!")
@bot.command(aliases = ["rlc_y"]) 
async def reload_cogs_y(ctx):
	# если сервер заблокирован то staff игнорируют это ограничение
	if ctx.author.id not in staff_staffList_SpecialPerms() and not guild_bot_output(ctx): return
	# команда работает только для staff с специальными правами (список staffList_SpecialPerms)
	if ctx.author.id not in staff_staffList_SpecialPerms(): return

	for filename in os.listdir("./cogsYujirou/commands"):
		if filename.endswith(".py"):
			await bot.load_extension(f"cogsYujirou.commands.{filename[:-3]}")
			print(f"\x1b[30;47m{datetime.now()}\x1b[0m Файлы \x1b[1;32m{', '.join([filename])}\x1b[0m в коге \x1b[1;34mcommands\x1b[0m загружены!")

	await ctx.send(f"Успешно обновлены коги!")


print("\n".join([
	" ____  ____            _   _                             ",
	"|_  _||_  _|          (_) (_)                           ",
	"  \ \  / /__   _      __  __   _ .--.   .--.   __   _   ",
	"   \ \/ /[  | | |    [  |[  | [ `/'`\]/ .'`\ \[  | | |  ",
	"   _|  |_ | \_/ |, _  | | | |  | |    | \__. | | \_/ |, ",
	"  |______|'.__.'_/[ \_| |[___][___]    '.__.'  '.__.'_/ ",
	"                   \____/                               ",
	f"\x1b[37;43mVERSION\x1b[0m: \x1b[31m{yujirou['version']['number']}\x1b[0m \x1b[0m{yujirou['version']['name']}\x1b[0m"
	"\n"
]))

print("\x1b[1;34mЗагрузка когов\x1b[0m:")
async def func_load_cogs():
	for filename in os.listdir("./cogsYujirou/commands"):
		if filename.endswith(".py"):
			await bot.load_extension(f"cogsYujirou.commands.{filename[:-3]}")
			print(f"\x1b[30;47m{datetime.now()}\x1b[0m Файлы \x1b[1;32m{', '.join([filename])}\x1b[0m в коге \x1b[1;34mcommands\x1b[0m загружены!")

async def main():
	async with bot:
		await func_load_cogs()
		bot.tree.copy_global_to(guild = discord.Object(id = main_server))
		await bot.start(token_yujirou)
asyncio.run(main())