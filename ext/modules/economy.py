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
	
	async def append_economy_xp_coins(self, message):
		xp_add = dbVars.cspl_get_param(message, 'g', 'xpAdd', 'economy')
		coins_add = dbVars.cspl_get_param(message, 'g', 'coinsAdd', 'economy')
		add_cooldown = dbVars.cspl_get_param(message, 'g', 'addCooldown', 'economy')

		current_time = datetime.datetime.now()

		if message.author.id not in self.xp_cooldown:
			self.xp_cooldown[message.author.id] = {}
		
		if message.guild.id not in self.xp_cooldown[message.author.id]:
			self.xp_cooldown[message.author.id][message.guild.id] = datetime.datetime.min
		
		if (current_time - self.xp_cooldown[message.author.id][message.guild.id]).total_seconds() < add_cooldown:
			return

		custom_users = json.load(open("./.db/crossplatform/custom/users.json", "r", encoding="utf-8"))
		if str(message.author.id) not in custom_users:
			custom_users[str(message.author.id)] = {}
		if str(message.guild.id) not in custom_users[str(message.author.id)]:
			custom_users[str(message.author.id)][str(message.guild.id)] = {}
		if "economy" not in custom_users[str(message.author.id)][str(message.guild.id)]:
			custom_users[str(message.author.id)][str(message.guild.id)]["economy"] = {}
		if 'xp' not in custom_users[str(message.author.id)][str(message.guild.id)]["economy"]:
			custom_users[str(message.author.id)][str(message.guild.id)]["economy"]['xp'] = xp_add
			custom_users[str(message.author.id)][str(message.guild.id)]["economy"]['lvl'] = 1
		else:
			custom_users[str(message.author.id)][str(message.guild.id)]["economy"]['xp'] += xp_add
		
		if 'coins' not in custom_users[str(message.author.id)][str(message.guild.id)]["economy"]:
			custom_users[str(message.author.id)][str(message.guild.id)]["economy"]['coins'] = coins_add
		else:
			custom_users[str(message.author.id)][str(message.guild.id)]["economy"]['coins'] += coins_add

		with open("./.db/crossplatform/custom/users.json", "w", encoding="utf-8") as write_file: json.dump(custom_users, write_file, ensure_ascii=False, indent=4)

		self.xp_cooldown[message.author.id][message.guild.id] = current_time
	
	def add_econony_lvl_and_coins(self, message, lvl: int, coins: int = None):
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


	async def start_economy_count(self, message: discord.Message):
		await self.append_economy_xp_coins(message)
		
		u_xp = dbVars.cspl_get_param(message, 'u', 'xp', 'economy')
		u_lvl = dbVars.cspl_get_param(message, 'u', 'lvl', 'economy')
		lvls_list = dbVars.cspl_get_param(message, 'g', 'lvls', 'economy')

		for level_data in lvls_list:
			if u_xp >= level_data['xp'] and u_lvl < level_data['lvl']:
				if level_data['coins']:
					coins = level_data['coins']
				lvl = level_data['lvl']
				self.add_econony_lvl_and_coins(message, lvl, coins if level_data['coins'] else None)
				await message.channel.send(f"{message.author.mention} ура! вы достигли {lvl}-ого уровня!" + f" Вы получаете {coins} монеток))" if level_data['coins'] else None)

	@commands.Cog.listener()
	async def on_message(self, message: discord.Message):
		try:
			if message.author.bot: return
			await self.start_economy_count(message)
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
"""