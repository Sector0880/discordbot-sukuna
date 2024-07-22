import discord
from discord.ext import commands
from discord import app_commands

import yaml
from datetime import datetime
import sys
import json

import dbVars

start_time = datetime.now()

def get_bot_prefix(bot, ctx):
	return dbVars.cspl_get_param(ctx, 'g', 'prefix')

def add_command_usage_counter(interaction, _phase):
	command = interaction.command.name # работает лучше
	with open("./.db/logs/commandsUsageCounter.yml", "r") as read_file: commandsUsageCounter = yaml.safe_load(read_file)
	phase = ''
	match _phase:
		case 1: phase = 'use'
		case 2: phase = 'success'
		case 3: phase = 'lose'
		case 4: phase = 'error'
	commandsUsageCounter["all"][phase] += 1 # все команды
	commandsUsageCounter[command][phase]  += 1 # вызываемая команда
	with open("./.db/logs/commandsUsageCounter.yml", "w") as write_file: yaml.safe_dump(commandsUsageCounter, write_file, sort_keys = False, allow_unicode = True)


#cspl_custom_guilds = lambda ctx: json.load(open("./.db/crossplatform/custom/guilds.json", "r", encoding="utf-8"))

	#if str(ctx.guild.id) in cspl_custom_guilds(ctx).keys() and 'prefix' in cspl_custom_guilds(ctx)[str(ctx.guild.id)]:
		#return json.load(open("./.db/crossplatform/custom/guilds.json", "r", encoding="utf-8"))[str(ctx.guild.id)]['prefix']
	#else:
		#return yaml.safe_load(open('./.db/crossplatform/initial/guilds.yml', 'r', encoding='utf-8'))['prefix']		