import discord
from discord.ext import commands, tasks
from discord import app_commands

import yaml
import json
import re
import asyncio
import uuid
from time import sleep
from datetime import datetime, timedelta

from botConfig import *
from dbVars import *
import botFunctions

class HelpPremium(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
	
	@app_commands.command(
		name = "help_premium",
		description = "Получить информацию по использованию команд, входящих в линейку Premium-подписки"
	)
	@app_commands.choices(command = [
		app_commands.Choice(name = "get_premium", value = 1),
		app_commands.Choice(name = "delete_premium", value = 2)
		#app_commands.Choice(name = "delete_premium_allservers", value = 3),
		#app_commands.Choice(name = "delete_premium_uuid_history", value = 4),
		#app_commands.Choice(name = "check_premium", value = 5),
		#app_commands.Choice(name = "delete_premium_history_file", value = 6),
		#app_commands.Choice(name = "check_premium_history_file", value = 7)
	])
	@botFunctions.check_command_permissions()
	async def help_premium(self, interaction: discord.Interaction, command: app_commands.Choice[int] = None):
		if command == None:
			emb = discord.Embed(
				title = "Команды Premium",
				description = ", ".join([
					'`get_premium`'
					#'`delete_premium`',
					#'`delete_premium_allservers`',
					#'`delete_premium_uuid_history`',
					#'`check_premium`',
					#'`delete_premium_history_file`',
					#'`check_premium_history_file`'
				]),
				color = 0x2b2d31
			)
		elif command.name:
			with open(f"./.db/doc/commands/{command.name}.yml", encoding="utf-8") as read_file: command_path = yaml.safe_load(read_file)
			
			keys = list(command_path["describe"].keys())
			text = ' '.join(keys)
			def add_color_markers(text):
				words = text.split()  # Разделяем текст на отдельные слова
				result = ""
				for word in words:
					if word.endswith("!"):
						# Если слово заканчивается "*", добавляем закрашивающие маркеры
						result += "\u001b[0;31m" + word + "\u001b[0;0m" + " "
					else:
						result += word + " "
				return result.strip()  # Удаляем лишний пробел в конце строки
			formatted_text = add_color_markers(text)
			for key, value in command_path["describe"].items():
				parameters = key + ": " + value
			emb = discord.Embed(
				title = f'Команда {command.name}',
				description = "\n".join([
					f'**Информация:** {command_path["description"]}', # ГОТОВО
					f'\n```ansi\n{command.name} {formatted_text}\n```', # ГОТОВО
					f'**Параметры:**',
					#'`time*`: Указанное кол-во секунд задаваемого премиума.',
					#'`server`: При указании сервера премиум начисляется указанному серверу.'
					#"\n".join([key + ": " + value for key, value in command_path["describe"].items()])
					"\n".join([f"`{key}`: {value}" for key, value in command_path["describe"].items()])
				]),
				color = 0x2b2d31
			)
			emb.set_footer(text = "* — обязательный параметр")
		else:
			return await interaction.response.send_message("Команда не найдена.", ephemeral = True)
		await interaction.response.send_message(embed = emb, ephemeral = True)

async def setup(bot: commands.Bot):
	await bot.add_cog(HelpPremium(bot))