import discord
from discord.ext import commands

import asyncio
import re
import os
import json

from dbVars import *

class Test(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		
	@commands.command()
	async def h(self, ctx, param, item):
		try:
			if ctx.author.id not in [980175834373562439, 522136072151367691, 224632121879166976]: return await ctx.send("Нету прав.") # на автора сообщения
			allowed = {
				'guilds': [
					'cluster',
					'gateaway-status',
					'prefix',
					'language',
					'modules', 'moderation', 'profile', 'fun', 'audit', 'music',
					'premium-status'
				],
				'users': [
					'cluster',
					'mute-status'
				]
			}
			if param not in list(allowed.keys()):
				valid_allowed = "\n".join(list(allowed.keys()))
				raise ValueError(f'Недопустимое значение для аргумента param. Допустимые значения:```\n{valid_allowed}```')
			if item not in allowed[param]:
				valid_item = "\n".join(allowed[param])
				raise ValueError(f'Недопустимое значение для аргумента item. Допустимые значения:```\n{valid_item}```')
			
			
			with open(f'./.db/crossparams/initial/{param}.yml', 'r', encoding='utf-8') as read_file:
				initial_param = yaml.safe_load(read_file)
			with open(f'./.db/crossparams/custom/{param}.json', 'r', encoding='utf-8') as read_file:
				custom_param = json.load(read_file)


			if param == 'guilds': param_id = str(ctx.guild.id)
			elif param == 'users': param_id = str(ctx.author.id)

			path = {
				'guilds': {
					'cluster': ['cluster'],
					'gateaway-status': ['gateaway', 'status'],
					'prefix': ['prefix'],
					'language': ['language'],
					'modules': ['modules'],
					'moderation': ['modules', 'moderation'],
					'profile': ['modules', 'profile'],
					'fun': ['modules', 'fun'],
					'audit': ['modules', 'audit'],
					'music': ['modules', 'music'],
					'premium-status': ['premium', 'status']
				},
				'users': {
					'cluster': ['cluster'],
					'mute-status': ['mute', 'status']
				}
			}


			item_path = path[param][item]
			if param_id in list(custom_param.keys()):
				if item in custom_param[param_id].keys():
					await ctx.send(custom_param[param_id][item_path])
				else:
					await ctx.send(initial_param[item_path])
			else:
				await ctx.send(initial_param[item_path])
		except ValueError as e:
			await ctx.send(str(e))
		except Exception as e:
			print(e)

async def setup(bot):
	await bot.add_cog(Test(bot))