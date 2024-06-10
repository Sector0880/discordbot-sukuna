import discord
from discord.ext import commands

import asyncio
import re
from dbVars import *
from botFunctions import *


class Settings(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	def set_profile_param(self, ctx, param: str, content):
		custom_users = json.load(open("./.db/crossplatform/custom/users.json", "r", encoding="utf-8"))
		if str(ctx.author.id) not in custom_users:
			custom_users[str(ctx.author.id)] = {}
		if str(ctx.guild.id) not in custom_users[str(ctx.author.id)]:
			custom_users[str(ctx.author.id)][str(ctx.guild.id)] = {}
		if "profile" not in custom_users[str(ctx.author.id)][str(ctx.guild.id)]:
			custom_users[str(ctx.author.id)][str(ctx.guild.id)]["profile"] = {}
		custom_users[str(ctx.author.id)][str(ctx.guild.id)]["profile"][param] = str(content)
		with open("./.db/crossplatform/custom/users.json", "w", encoding="utf-8") as write_file: json.dump(custom_users, write_file, ensure_ascii = False, indent = 4)
	
	async def del_profile_param(self, ctx, param: str):
		custom_users = json.load(open("./.db/crossplatform/custom/users.json", "r", encoding="utf-8"))
		if str(ctx.author.id) not in custom_users:
			custom_users[str(ctx.author.id)] = {}
		if str(ctx.guild.id) not in custom_users[str(ctx.author.id)]:
			custom_users[str(ctx.author.id)][str(ctx.guild.id)] = {}
		if "profile" not in custom_users[str(ctx.author.id)][str(ctx.guild.id)]:
			custom_users[str(ctx.author.id)][str(ctx.guild.id)]["profile"] = {}
		if str(param) not in custom_users[str(ctx.author.id)][str(ctx.guild.id)]["profile"]:
			return await ctx.send(f"В Вашем профиле не указан {param}.")
		
		# Удалить параметр из профиля
		custom_users[str(ctx.author.id)][str(ctx.guild.id)]["profile"].pop(str(param))
		
		# Проверка и удаление profile, если он стал пустым
		if not custom_users[str(ctx.author.id)][str(ctx.guild.id)]["profile"]:
			del custom_users[str(ctx.author.id)][str(ctx.guild.id)]["profile"]
		
		# Проверка и удаление str(ctx.guild.id), если profile стал пустым
		if not custom_users[str(ctx.author.id)][str(ctx.guild.id)]:
			del custom_users[str(ctx.author.id)][str(ctx.guild.id)]
		
		# Проверка и удаление str(ctx.author.id), если str(ctx.guild.id) стал пустым
		if not custom_users[str(ctx.author.id)]:
			del custom_users[str(ctx.author.id)]
		
		with open("./.db/crossplatform/custom/users.json", "w", encoding="utf-8") as write_file: json.dump(custom_users, write_file, ensure_ascii=False, indent=4)
	

	@commands.hybrid_command(
		name = "set_profile_about",
		description = 'Добавить биографию для своего профиля на сервере.',
		aliases = ['spab']
	)
	async def set_profile_about(self, ctx, *, _content: str = commands.parameter(description="Ваша биография.", displayed_name = "Биография")):
		try:
			self.set_profile_param(ctx, "about", _content)
			await ctx.send(f"```json\n{cspl_custom_users(ctx)[str(ctx.author.id)][str(ctx.guild.id)]["profile"]}\n```", ephemeral = True)
		except Exception as e:
			print(repr(e))
	
	@commands.hybrid_command(
		name = "set_profile_age",
		description = 'Добавить возраст для своего профиля на сервере.',
		aliases = ['spag']
	)
	async def set_profile_age(self, ctx, _content):
		try:
			self.set_profile_param(ctx, "age", _content)
			await ctx.send(f"```json\n{cspl_custom_users(ctx)[str(ctx.author.id)][str(ctx.guild.id)]["profile"]}\n```", ephemeral = True)
		except Exception as e:
			print(repr(e))
	
	@commands.hybrid_command(
		name = "set_profile_city",
		description = 'Добавить город для своего профиля на сервере.',
		aliases = ['spci']
	)
	async def set_profile_city(self, ctx, *, _content):
		try:
			self.set_profile_param(ctx, "city", _content)
			await ctx.send(f"```json\n{cspl_custom_users(ctx)[str(ctx.author.id)][str(ctx.guild.id)]["profile"]}\n```", ephemeral = True)
		except Exception as e:
			print(repr(e))
	
	@commands.hybrid_command(
		name = "del_profile_about",
		description = 'Удалить биографию из своего профиля на сервере.',
		aliases = ['dpab']
	)
	async def del_profile_about(self, ctx):
		try:
			await self.del_profile_param(ctx, "about")
			await ctx.send("Успешно удалена биография.")
		except Exception as e:
			print(repr(e))
	
	@commands.hybrid_command(
		name = "del_profile_age",
		description = 'Удалить свой возраст из своего профиля на сервере.',
		aliases = ['dpag']
	)
	async def del_profile_age(self, ctx):
		try:
			await self.del_profile_param(ctx, "age")
			await ctx.send("Успешно удален возраст.")
		except Exception as e:
			print(repr(e))
	
	@commands.hybrid_command(
		name = "del_profile_city",
		description = 'Удалить город из своего профиля на сервере.',
		aliases = ['dpci']
	)
	async def del_profile_city(self, ctx):
		try:
			await self.del_profile_param(ctx, "city")
			await ctx.send("Успешно удален город.")
		except Exception as e:
			print(repr(e))

			
async def setup(bot):
	await bot.add_cog(Settings(bot))