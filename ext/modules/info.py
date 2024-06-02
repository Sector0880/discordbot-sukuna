import discord
from discord.ext import commands
from discord import app_commands
import yaml

from botConfig import *
from datetime import *
from dbVars import *
from botFunctions import *

class Info(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
	
	@app_commands.command(
		name = "help",
		description = "Информация по командам"
	)
	@app_commands.choices(command = [
		app_commands.Choice(name = "get_premium", value = 1),
		app_commands.Choice(name = "delete_premium", value = 2),
		app_commands.Choice(name = "time", value = 3),
		#app_commands.Choice(name = "delete_premium_allservers", value = 3),
		#app_commands.Choice(name = "delete_premium_uuid_history", value = 4),
		#app_commands.Choice(name = "check_premium", value = 5),
		#app_commands.Choice(name = "delete_premium_history_file", value = 6),
		#app_commands.Choice(name = "check_premium_history_file", value = 7)
	])
	async def help(self, interaction: discord.Interaction, command: app_commands.Choice[int] = None):
		try:
			if command == None:
				emb = discord.Embed(
					title = f"Команды [{len(self.bot.commands)}|3]",
					description = ", ".join([
						'`get_premium`',
						'`delete_premium`',
						'`time`',
						#'`delete_premium_allservers`',
						#'`delete_premium_uuid_history`',
						#'`check_premium`',
						#'`delete_premium_history_file`',
						#'`check_premium_history_file`'
					]),
					color = 0x2b2d31
				)
			elif command.name:
				self.text_footer = False
				with open(f"./.db/docs/commands/{command.name}.yml", encoding="utf-8") as read_file: cmd = yaml.safe_load(read_file)
				
				if "describe" in cmd:
					keys = list(cmd["describe"].keys())
					text = ' '.join(keys)
					def add_color_markers(text):
						words = text.split()  # Разделяем текст на отдельные слова
						result = ""
						for word in words:
							if word.endswith("!"):
								# Если слово заканчивается "*", добавляем закрашивающие маркеры
								result += "\u001b[0;31m" + word + "\u001b[0;0m" + " "
								self.text_footer = True
							else:
								result += word + " "
						return result.strip()  # Удаляем лишний пробел в конце строки
					formatted_text = add_color_markers(text)
				else:
					formatted_text = ""
				emb = discord.Embed(title = f'Команда: {command.name}', color = 0x2b2d31)
				emb.add_field(
					name = "Информация",
					value = cmd["description"],
					inline=False
				)
				if "prefix" in cmd["type"]:
					pattern_value = f'\n```ansi\n{cspl_get_param(interaction, "guilds", "prefix")}{command.name} {formatted_text}\n```'
				elif "hybrid" in cmd["type"]:
					pattern_value = '\n'.join([
						f'\n```ansi\n/{command.name} {formatted_text}',
						f'{cspl_get_param(interaction, "guilds", "prefix")}{command.name} {formatted_text}\n```'
					])
				else:
					pattern_value = f'\n```ansi\n/{command.name} {formatted_text}\n```'
				emb.add_field(
					name = "Паттерн",
					value = pattern_value,
					inline=False
				)
				if "describe" in cmd: emb.add_field(
					name = "Параметры",
					value = "\n".join([f"`{key}` — {value}" for key, value in cmd["describe"].items()]),
					inline=False
				)
				if self.text_footer: emb.set_footer(text = "! — обязательный параметр")
			else:
				return await interaction.response.send_message("Команда не найдена.", ephemeral = True)
			await interaction.response.send_message(embed = emb, ephemeral = True)
		except Exception as e:
			await interaction.response.send_message(f'||{e}||')
	
	@commands.hybrid_command(
		name = 'ping',
		description = 'Узнать время отклика бота.',
		aliases = ['пинг']
	)
	async def ping(self, ctx):
		try:
			ping = self.bot.latency
			ping_emoji = '🟩🔳🔳🔳🔳'

			if ping > 0.10000000000000000:
				ping_emoji = '🟧🟩🔳🔳🔳'

			if ping > 0.15000000000000000:
				ping_emoji = '🟥🟧🟩🔳🔳'

			if ping > 0.20000000000000000:
				ping_emoji = '🟥🟥🟧🟩🔳'

			if ping > 0.25000000000000000:
				ping_emoji = '🟥🟥🟥🟧🟩'

			if ping > 0.30000000000000000:
				ping_emoji = '🟥🟥🟥🟥🟧'

			if ping > 0.35000000000000000:
				ping_emoji = '🟥🟥🟥🟥🟥'

			# Переменная с пингом бота до текущего шарда
			shard_ping = f'{ping_emoji} `{round(self.bot.latency * 1000)}ms`'

			message = await ctx.send('Отбиваю...  🔳🔳🔳🔳🔳 `секунду...`')
			await message.edit(content = f'Понг! 🏓  {shard_ping}')
		except Exception as e:
			await ctx.send(e)
	
	@commands.hybrid_command(
		name = "profile",
		description = 'Показать информацию о юзере.',
		aliases = ['профиль']
	)
	async def profile(self, ctx, user: discord.Member = None):
		try:
			profile = ctx.author if not user else user
			roles = profile.roles
			role_list = ''
			role_list_number = 0

			for role in reversed(roles):
				if role != ctx.guild.default_role:
					role_list += f'<@&{role.id}> '
					role_list_number += 1
				
			if profile.status == discord.Status.online:
				status = '<:online:748149457396433016> В сети'
			elif profile.status == discord.Status.idle:
				status = '<:idle:748149485707984907> Не активен'
			elif profile.status == discord.Status.dnd:
				status = '<a:mark_none:815121643479236618> Не беспокоить'
			else:
				status = '<:offline:748149539915038731> Не в сети'
			
			emb = discord.Embed(colour = color_success)
			emb.set_author(name = f'{profile}', icon_url = profile.avatar)
			emb.set_thumbnail(url = profile.avatar)
			emb.add_field(name = 'В Discord', value = profile.created_at.strftime('**Дата:** %d/%m/%Y\n**Время:** %H:%M:%S'))
			emb.add_field(name = 'На сервере', value = profile.joined_at.strftime('**Дата:** %d/%m/%Y\n**Время:** %H:%M:%S'))
			emb.add_field(name = 'Статус', value = status, inline = False)
			emb.add_field(name = f'Роли [{role_list_number}]', value = 'Отсутствуют' if role_list == '' else role_list, inline = False)
			#emb.set_footer(text = f'ID: {profile.id}')
			emb.timestamp = datetime.utcnow()

			await ctx.send(embed = emb, ephemeral=True)
		except Exception as e:
			await ctx.send(e, ephemeral=True)
	
	@commands.hybrid_command(
		name = "avatar",
		description = 'Получить аватарку юзера.',
		aliases = ['аватарка']
	)
	async def avatar(self, ctx, user: discord.Member = None):
		try:
			user = ctx.author if not user else user

			emb = discord.Embed(colour = color_success)
			emb.set_author(name = user, icon_url = user.avatar)
			emb.set_image(url = user.avatar)

			await ctx.send(embed = emb, ephemeral=True)
		except Exception as e:
			await ctx.send(e, ephemeral=True)

async def setup(bot):
	await bot.add_cog(Info(bot))