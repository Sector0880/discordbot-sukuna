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

		self.xp_add = 5
		self.xp_add_cooldown = 7
		self.xp_cooldown = {}
	
	def create_economy_xp(self, message):
		custom_users = json.load(open("./.db/crossplatform/custom/users.json", "r", encoding="utf-8"))
		if str(message.author.id) not in custom_users:
			custom_users[str(message.author.id)] = {}
		if str(message.guild.id) not in custom_users[str(message.author.id)]:
			custom_users[str(message.author.id)][str(message.guild.id)] = {}
	
		if "economy" not in custom_users[str(message.author.id)][str(message.guild.id)]:
			custom_users[str(message.author.id)][str(message.guild.id)]["economy"] = {}
		custom_users[str(message.author.id)][str(message.guild.id)]["economy"]['xp'] = self.xp_add
		with open("./.db/crossplatform/custom/users.json", "w", encoding="utf-8") as write_file: json.dump(custom_users, write_file, ensure_ascii = False, indent = 4)
	
	async def append_economy_xp(self, message):
		current_time = datetime.datetime.now()

		if message.author.id not in self.xp_cooldown:
			self.xp_cooldown[message.author.id] = {}
		
		if message.guild.id not in self.xp_cooldown[message.author.id]:
			self.xp_cooldown[message.author.id][message.guild.id] = datetime.datetime.min
		
		if (current_time - self.xp_cooldown[message.author.id][message.guild.id]).total_seconds() < self.xp_add_cooldown:
			return

		custom_users = json.load(open("./.db/crossplatform/custom/users.json", "r", encoding="utf-8"))
		custom_users[str(message.author.id)][str(message.guild.id)]["economy"]['xp'] += self.xp_add

		with open("./.db/crossplatform/custom/users.json", "w", encoding="utf-8") as write_file: json.dump(custom_users, write_file, ensure_ascii=False, indent=4)

		self.xp_cooldown[message.author.id][message.guild.id] = current_time
	
	def set_econony_coins(self, message, coins: int):
		custom_users = json.load(open("./.db/crossplatform/custom/users.json", "r", encoding="utf-8"))
		if str(message.author.id) not in custom_users:
			custom_users[str(message.author.id)] = {}
		if str(message.guild.id) not in custom_users[str(message.author.id)]:
			custom_users[str(message.author.id)][str(message.guild.id)] = {}
	
		if "economy" not in custom_users[str(message.author.id)][str(message.guild.id)]:
			custom_users[str(message.author.id)][str(message.guild.id)]["economy"] = {}
		custom_users[str(message.author.id)][str(message.guild.id)]["economy"]['coins'] = coins
		with open("./.db/crossplatform/custom/users.json", "w", encoding="utf-8") as write_file: json.dump(custom_users, write_file, ensure_ascii = False, indent = 4)

	@commands.Cog.listener()
	async def on_message(self, message):
		try:
			if message.author.bot: return
			if dbVars.cspl_get_param(message, 'u', 'xp', 'economy') == 0:
				self.create_economy_xp(message)
			else:
				await self.append_economy_xp(message)
			
			if dbVars.cspl_get_param(message, 'u', 'xp', 'economy') == 50:
				coins = 200
				await message.channel.send(f"ура! вы достигли 1-ого уровня! Вы получаете {coins} монеток))")
				self.set_econony_coins(message, coins)
		except Exception as e:
			print(repr(e))
	
	@commands.command()
	@commands.is_owner()
	async def delete_economy_xp(self, ctx, member_id: int, guilds_id: int):
		await ctx.send("скоро...")
		

async def setup(bot):
	await bot.add_cog(Economy(bot))