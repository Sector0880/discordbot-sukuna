import discord
from discord.ext import commands
from discord import app_commands

import yaml
from datetime import datetime
import sys
import json

def bot_prefix(bot, ctx):
	cspl_custom_guilds = lambda ctx: json.load(open("./.db/crossplatform/custom/guilds.json", "r", encoding="utf-8"))

	if str(ctx.guild.id) in cspl_custom_guilds(ctx).keys() and 'prefix' in cspl_custom_guilds(ctx)[str(ctx.guild.id)]:
		return json.load(open("./.db/crossplatform/custom/guilds.json", "r", encoding="utf-8"))['prefix']
	else:
		return yaml.safe_load(open('./.db/crossplatform/initial/guilds.yml', 'r', encoding='utf-8'))['prefix']


def bot_prefix_old(bot, ctx):
	with open('./.db/crossparams/custom/clusters-guilds.json', 'r', encoding='utf-8') as read_file: clusters_guilds = json.load(read_file)
	
	guild_id = str(ctx.guild.id)

	for key, value in clusters_guilds.items():
		if guild_id in value["guilds"]:
			guild_cluster = key
			with open(f'./.db/crossparams/custom/clusters/{guild_cluster}/guilds.json', 'r', encoding='utf-8') as read_file:cluster_guilds = json.load(read_file)
				
			if guild_id in cluster_guilds: return cluster_guilds[guild_id]["prefix"]

	return yaml.safe_load(open('./.db/crossparams/initial/guilds.yml', 'r', encoding='utf-8'))["prefix"]
				





# rework
async def command_counter(ctx):
	#command = ctx.invoked_with
	command = ctx.command.name # работает лучше
	with open("./.db/info/commandsCount.yml", "r") as read_file: commandsInfo = yaml.safe_load(read_file)
	commandsInfo["all"] += 1 # все команды
	commandsInfo[command] += 1 # вызываемая команда
	with open("./.db/info/commandsCount.yml", "w") as write_file: yaml.safe_dump(commandsInfo, write_file, sort_keys = False, allow_unicode = True)