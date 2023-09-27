import discord
from discord.ext import commands
from discord import app_commands

import yaml
from datetime import datetime
import sys

from botConfig import *
from dbVars import *

def check_command_permissions():
	async def predicate(interaction: discord.Interaction):
		if interaction.user.id not in staff_staffList_SpecialPerms() and not guild_bot_output(interaction):
			# переделать
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
		return True
	return app_commands.check(predicate)

def command_for_staff():
	async def predicate(interaction: discord.Interaction):
		if interaction.user.id not in staff_staffList_SpecialPerms():
			await interaction.response.send_message(f"{emoji_mark_error} Команда предназначена только для определенных лиц, относящихся к разработке бота.", ephemeral = True)
			return False
		return True
	return app_commands.check(predicate)