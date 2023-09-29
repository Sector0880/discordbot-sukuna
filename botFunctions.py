import discord
from discord.ext import commands
from discord import app_commands

import yaml
from datetime import datetime
import sys
import json

def get_prefix(bot, ctx):
	with open("./.db/multipresence/guilds/config.json", "r", encoding="utf-8") as file: db_guild_data = json.load(file)
	if "prefix" in db_guild_data()[str(ctx.guild.id)]:
		with open("./.db/multipresence/guilds/config.json", "r", encoding="utf-8") as file: return json.load(file)[str(ctx.guild.id)]["prefix"]
	else:
		with open("./.db/multipresence/guilds/config.yml", "r", encoding="utf-8") as read_file: return yaml.safe_load(read_file)["prefix"]


# rework
async def command_counter(ctx):
	#command = ctx.invoked_with
	command = ctx.command.name # работает лучше
	with open("./.db/info/commandsCount.yml", "r") as read_file: commandsInfo = yaml.safe_load(read_file)
	commandsInfo["all"] += 1 # все команды
	commandsInfo[command] += 1 # вызываемая команда
	with open("./.db/info/commandsCount.yml", "w") as write_file: yaml.safe_dump(commandsInfo, write_file, sort_keys = False, allow_unicode = True)