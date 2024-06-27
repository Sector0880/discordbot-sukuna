import discord
from discord.ext import commands
from discord import app_commands

import yaml
from datetime import datetime
import sys

from botConfig import *
from dbVars import *

def cmd_for_sfsp():
	async def predicate(ctx: discord.Message):
		if ctx.author.id not in sf_sp(): 
			await ctx.send("Нету прав.") # на автора сообщения сообщения
			return False
		else:
			return True
	return commands.check(predicate)

def check_cmd_work():
	async def predicate(interaction: discord.Interaction):
		# Получение всех модулей
		modules = cspl_get_param_with_merge(interaction, 'g', 'modules')
		
		# Поиск модуля, содержащего команду
		found_module = None
		for module_name, module_info in modules.items():
			if 'commands' in module_info and interaction.command.name in module_info['commands']:
				found_module = module_info
				break

		# Если модуль не найден, вернуть False
		if not found_module:
			await interaction.response.send_message(f"{emoji_mark_error} Модуль не найден.", ephemeral=True)
			return False

		# Получение статуса модуля и команды
		module_status = found_module['status']
		command_status = found_module['commands'][interaction.command.name]['status']
		
		# Проверка статуса модуля и команды
		if not module_status and not command_status:
			await interaction.response.send_message(f"{emoji_mark_error} Модуль команды и команда выключены.", ephemeral=True)
			return False
		elif not module_status:
			await interaction.response.send_message(f"{emoji_mark_error} Модуль команды выключен.", ephemeral=True)
			return False
		elif not command_status:
			await interaction.response.send_message(f"{emoji_mark_error} Команда выключена.", ephemeral=True)
			return False
		
		return True

	return app_commands.check(predicate)
			



"""
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
"""