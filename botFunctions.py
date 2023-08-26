import discord
from discord.ext import commands, tasks
from discord import app_commands

import yaml
from datetime import datetime
import sys

from botsConfig import *
from dbVars import *
import botsFunctions

# работает
async def command_counter(ctx):
	#command = ctx.invoked_with
	command = ctx.command.name # работает лучше
	with open("./botConfiguration/.db/info/commandsCount.yml", "r") as read_file: commandsInfo = yaml.safe_load(read_file)
	commandsInfo["all"] += 1 # все команды
	commandsInfo[command] += 1 # вызываемая команда
	with open("./botConfiguration/.db/info/commandsCount.yml", "w") as write_file: yaml.safe_dump(commandsInfo, write_file, sort_keys = False, allow_unicode = True)

# работает
async def bot_output_blocked(ctx):
	emb = discord.Embed(
		description = "\n".join([
			error_server_blocked()[guild_language(ctx)]["error"]["description1"].format(emoji_mark_error),
			error_server_blocked()[guild_language(ctx)]["error"]["description2"].format(staff_creator_id())
		]),
		color = color_error,
		timestamp = datetime.now()
	)
	emb.set_image(url = "https://cdn.discordapp.com/attachments/817101575289176064/1137345466875518986/black__200px.gif")
	emb.set_footer(text = ctx.author.name, icon_url = ctx.author.avatar)
	await ctx.send(embed = emb)

async def command_for_staff(interaction: discord.Interaction):
	await interaction.response.send_message(f"{emoji_mark_error} Команда предназначена только для определенных лиц, относящихся к разработке бота.", ephemeral = True)