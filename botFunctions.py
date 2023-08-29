import discord
from discord.ext import commands
from discord import app_commands

import yaml
from datetime import datetime
import sys

from botConfig import *
from dbVars import *

# rework
async def command_counter(ctx):
	#command = ctx.invoked_with
	command = ctx.command.name # работает лучше
	with open("./.db/info/commandsCount.yml", "r") as read_file: commandsInfo = yaml.safe_load(read_file)
	commandsInfo["all"] += 1 # все команды
	commandsInfo[command] += 1 # вызываемая команда
	with open("./.db/info/commandsCount.yml", "w") as write_file: yaml.safe_dump(commandsInfo, write_file, sort_keys = False, allow_unicode = True)

def check_command_permissions():
	async def predicate(interaction: discord.Interaction):
		if interaction.user.id not in staff_staffList_SpecialPerms() and not guild_bot_output(interaction):
			emb = discord.Embed(
			description = "\n".join([
				error_server_blocked()[guild_language(interaction)]["error"]["description1"].format(emoji_mark_error),
				error_server_blocked()[guild_language(interaction)]["error"]["description2"].format(staff_creator_id())
			]),
			color = color_error,
			timestamp = datetime.now()
			)
			emb.set_image(url = "https://cdn.discordapp.com/attachments/817101575289176064/1137345466875518986/black__200px.gif")
			emb.set_footer(text = interaction.user.name, icon_url = interaction.user.avatar)
			await interaction.response.send_message(embed = emb, ephemeral = True)
			return False
		if interaction.user.id not in staff_staffList_SpecialPerms():
			await interaction.response.send_message(f"{emoji_mark_error} Команда предназначена только для определенных лиц, относящихся к разработке бота.", ephemeral = True)
			return False
		return True
	return app_commands.check(predicate)