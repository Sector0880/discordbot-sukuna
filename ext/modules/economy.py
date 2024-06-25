import discord
from discord.ext import commands
from discord import app_commands

import nekos
from googletrans import Translator
import requests
from bs4 import BeautifulSoup
import random
import json
import yaml
import datetime

import botFunctions
import dbVars

class Economy(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot

		self.xp_cooldown = {}

	# награда за сообщение (готово)
	async def msg_award(self, message: discord.Message):
		# проверка на кулдаун сообщения (готово)
		current_time = datetime.datetime.now()
		if message.author.id not in self.xp_cooldown:
			self.xp_cooldown[message.author.id] = {}
		if message.guild.id not in self.xp_cooldown[message.author.id]:
			self.xp_cooldown[message.author.id][message.guild.id] = datetime.datetime.min
		if (current_time - self.xp_cooldown[message.author.id][message.guild.id]).total_seconds() < dbVars.cspl_get_param(message, 'g', 'cooldown', 'economy', 'msgAward'):
			return

		custom_users = json.load(open("./.db/crossplatform/custom/users.json", "r", encoding="utf-8"))

		if str(message.author.id) not in custom_users:
			custom_users[str(message.author.id)] = {}
		if str(message.guild.id) not in custom_users[str(message.author.id)]:
			custom_users[str(message.author.id)][str(message.guild.id)] = {}
		if "economy" not in custom_users[str(message.author.id)][str(message.guild.id)]:
			custom_users[str(message.author.id)][str(message.guild.id)]["economy"] = {}

		xp_add = dbVars.cspl_get_param(message, 'g', 'xp', 'economy', 'msgAward')
		coins_add = dbVars.cspl_get_param(message, 'g', 'coins', 'economy', 'msgAward')
		
		if 'xp' not in custom_users[str(message.author.id)][str(message.guild.id)]["economy"]:
			custom_users[str(message.author.id)][str(message.guild.id)]["economy"]['xp'] = xp_add
		else:
			custom_users[str(message.author.id)][str(message.guild.id)]["economy"]['xp'] += xp_add
		
		if 'coins' not in custom_users[str(message.author.id)][str(message.guild.id)]["economy"]:
			custom_users[str(message.author.id)][str(message.guild.id)]["economy"]['coins'] = coins_add
		else:
			custom_users[str(message.author.id)][str(message.guild.id)]["economy"]['coins'] += coins_add

		with open("./.db/crossplatform/custom/users.json", "w", encoding="utf-8") as write_file: json.dump(custom_users, write_file, ensure_ascii=False, indent=4)

		self.xp_cooldown[message.author.id][message.guild.id] = current_time

	# рассчитывание правильного уровня для пользователя (готово)
	async def check_lvl_validate(self, message: discord.Message):
		custom_users = json.load(open("./.db/crossplatform/custom/users.json", "r", encoding="utf-8"))

		user_id = str(message.author.id)
		guild_id = str(message.guild.id)

		if user_id not in custom_users:
			custom_users[user_id] = {}
		if guild_id not in custom_users[user_id]:
			custom_users[user_id][guild_id] = {}
		if "economy" not in custom_users[user_id][guild_id]:
			custom_users[user_id][guild_id]["economy"] = {}

		economy_levels = dbVars.cspl_get_param(message, 'g', 'lvls', 'economy')
		economy_levels.insert(0, {"lvl": 1, "xp": 0})

		def find_current_level_xp(xp):
			current_level = 1  # Начальный уровень 1
			next_level = 2  # Следующий уровень 2

			for i in range(1, len(economy_levels)):
				if xp >= economy_levels[i]["xp"]:
					current_level = economy_levels[i]["lvl"]
					if i + 1 < len(economy_levels):
						next_level = economy_levels[i + 1]["lvl"]
					else:
						next_level = None  # Нет следующего уровня
				else:
					break  # Если текущий xp меньше требуемого, остановить цикл

			current_xp = economy_levels[current_level - 1]["xp"]
			if next_level is not None:
				next_xp = economy_levels[next_level - 1]["xp"]
				percent_to_next_level = int(((xp - current_xp) / (next_xp - current_xp)) * 100)
			else:
				percent_to_next_level = 100  # Достигнут максимальный уровень

			return current_level, next_level, percent_to_next_level

		user_xp = dbVars.cspl_get_param(message, 'u', 'xp', 'economy')
		current_level, next_level, percent_to_next_level = find_current_level_xp(user_xp)

		if dbVars.cspl_get_param(message, 'u', 'lvl', 'economy') != current_level:
			custom_users[user_id][guild_id]["economy"]['lvl'] = current_level
		
		if current_level == 1:
			if 'lvl' in custom_users[user_id][guild_id]["economy"]:
				custom_users[user_id][guild_id]["economy"].pop('lvl')

		with open("./.db/crossplatform/custom/users.json", "w", encoding="utf-8") as write_file: json.dump(custom_users, write_file, ensure_ascii=False, indent=4)
	
	async def lvl_award(self, message: discord.Message):
		custom_users = json.load(open("./.db/crossplatform/custom/users.json", "r", encoding="utf-8"))

		lvls = dbVars.cspl_get_param(message, 'g', 'lvls', 'economy')
		lvls.insert(0, {"lvl": 1, "xp": 0})
		member_xp = dbVars.cspl_get_param(message, 'u', 'xp', 'economy')
		member_lvl = dbVars.cspl_get_param(message, 'u', 'lvl', 'economy')

		user_id = str(message.author.id)
		guild_id = str(message.guild.id)

		awarded = False
		awards_txt = ''

		for lvl in lvls:
			if member_xp >= lvl['xp'] and member_lvl < lvl['lvl']:
				# Обновление уровня пользователя
				custom_users[user_id][guild_id]["economy"]['lvl'] = lvl['lvl']
				if 'awards' in lvl and lvl['awards']:
					# Выдача наград
					awards = lvl.get('awards', {})
					if 'coins' in awards:
						custom_users[user_id][guild_id]["economy"]['coins'] += awards['coins']
						awards_txt += f"`{awards['coins']}{dbVars.cspl_get_param(message, 'g', 'coinsName', 'economy')[0]}` "
					if 'role' in awards:
						role_id = int(awards['role'].strip('<@&>'))
						role = message.guild.get_role(role_id)
						if role:
							await message.author.add_roles(role)
							awards_txt += f'Роль: <@&{role_id}> '
					if 'roles' in awards:
						for role_mention in awards['roles']:
							role_id = int(role_mention.strip('<@&>'))
							role = message.guild.get_role(role_id)
							if role:
								await message.author.add_roles(role)
								awards_txt += f'Роль: <@&{role_id}> '

					awarded = True
			else: # проверка
				# проверка наличия валидного уровня
				await self.check_lvl_validate(message)

		if awarded:
			with open("./.db/crossplatform/custom/users.json", "w", encoding="utf-8") as write_file:
				json.dump(custom_users, write_file, ensure_ascii=False, indent=4)

			await message.channel.send('\n'.join([
				f"{message.author.mention} поздравляю! Вы достигли `{dbVars.cspl_get_param(message, 'u', 'lvl', 'economy')}ур.`",
				f'**Награды:** {awards_txt.strip()}' if awards_txt else ''
			]))

	async def start_economy_system(self, message: discord.Message):
		# выдача наград за сообщение
		await self.msg_award(message)

		# выдача наград за достижение нового уровня
		await self.lvl_award(message)
		
	@commands.Cog.listener()
	async def on_message(self, message: discord.Message):
		try:
			if message.author.bot: return
			await self.start_economy_system(message)
		except Exception as e:
			print(repr(e))
	
	@commands.command()
	@commands.is_owner()
	async def delete_economy_xp(self, ctx, member_id: int, guilds_id: int):
		await ctx.send("скоро...")
		

async def setup(bot):
	await bot.add_cog(Economy(bot))

"""
if dbVars.cspl_get_param(message, 'u', 'xp', 'economy') == 50:
	coins = 200
	await message.channel.send(f"ура! вы достигли 1-ого уровня! Вы получаете {coins} монеток))")
	self.set_econony_coins(message, coins)
elif dbVars.cspl_get_param(message, 'u', 'xp', 'economy') == 100:
	coins = 300
	await message.channel.send(f"ура! вы достигли 2-ого уровня! Вы получаете {coins} монеток))")
	self.set_econony_coins(message, coins)

	def add_econony_lvl_and_coins(self, message: discord.Message, lvl: int, coins: int = None):
		custom_users = json.load(open("./.db/crossplatform/custom/users.json", "r", encoding="utf-8"))
		
		
		if str(message.author.id) not in custom_users:
			custom_users[str(message.author.id)] = {}
		if str(message.guild.id) not in custom_users[str(message.author.id)]:
			custom_users[str(message.author.id)][str(message.guild.id)] = {}
		if "economy" not in custom_users[str(message.author.id)][str(message.guild.id)]:
			custom_users[str(message.author.id)][str(message.guild.id)]["economy"] = {}
		
		custom_users[str(message.author.id)][str(message.guild.id)]["economy"]['lvl'] = lvl
		
		if coins:
			if 'coins' in custom_users[str(message.author.id)][str(message.guild.id)]["economy"]:
				if 'coins' in custom_users[str(message.author.id)][str(message.guild.id)]["economy"] == 0:
					custom_users[str(message.author.id)][str(message.guild.id)]["economy"]['coins'] = coins
					print('типооо')
				custom_users[str(message.author.id)][str(message.guild.id)]["economy"]['coins'] += coins

		with open("./.db/crossplatform/custom/users.json", "w", encoding="utf-8") as write_file: json.dump(custom_users, write_file, ensure_ascii = False, indent = 4)
#u_xp = dbVars.cspl_get_param(message, 'u', 'xp', 'economy')
		#u_lvl = dbVars.cspl_get_param(message, 'u', 'lvl', 'economy')
		#lvls_list = dbVars.cspl_get_param(message, 'g', 'lvls', 'economy')
		#lvls_list.insert(0, {"lvl": 1, "xp": 0})

		#for level_data in lvls_list:
			#if u_xp >= level_data['xp'] and u_lvl < level_data['lvl']:
				#if level_data['coins']:
					#coins = level_data['coins']
				#lvl = level_data['lvl']
				#self.add_econony_lvl_and_coins(message, lvl, coins if level_data['coins'] else None)
				#await message.channel.send(f"{message.author.mention} ура! вы достигли {lvl}-ого уровня!" + f" Вы получаете {coins} монеток))" if level_data['coins'] else None)

"""