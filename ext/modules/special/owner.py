import discord
from discord.ext import commands

import asyncio
import re
import os
import json
import yaml

from dbVars import * 
import botDecorators

class Owner(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		
	@commands.command(aliases = ['logs_cuc'])
	@commands.is_owner()
	async def delete_commands_usage_counter(self, ctx):
		try:
			with open("./.db/logs/commandsUsageCounter.yml", "r") as read_file: commandsUsageCounter = yaml.safe_load(read_file)
			commandsUsageCounter["all"]["use"] = 0
			commandsUsageCounter["all"]["success"] = 0
			commandsUsageCounter["all"]["lose"] = 0
			commandsUsageCounter["all"]["error"] = 0

			commandsUsageCounter["repeat"]["use"] = 0
			commandsUsageCounter["repeat"]["success"] = 0
			commandsUsageCounter["repeat"]["lose"] = 0
			commandsUsageCounter["repeat"]["error"] = 0

			commandsUsageCounter["time"]["use"] = 0
			commandsUsageCounter["time"]["success"] = 0
			commandsUsageCounter["time"]["lose"] = 0
			commandsUsageCounter["time"]["error"] = 0
			with open("./.db/logs/commandsUsageCounter.yml", "w") as write_file: yaml.safe_dump(commandsUsageCounter, write_file, sort_keys = False, allow_unicode = True)
			await ctx.send("успешно!")
		except ValueError as e:
			await ctx.send(str(e))
		except Exception as e:
			print(e)
	
	@commands.command(aliases = ['o_gg'])
	@commands.is_owner()
	async def owner_get_guild(self, ctx: discord.Message, guild_id: int = None):
		try:
			if not guild_id: guild_id = ctx.guild.id
			if not isinstance(guild_id, int): return await ctx.send("Введите ID сервера")
			modules_on = []
			modules_off = []
			for module in cspl_get_param_with_merge(ctx, 'g', 'modules', None, None, guild_id):
				if cspl_get_param_with_merge(ctx, 'g', 'status', ['modules', module]):
					modules_on.append(cspl_get_param_with_merge(ctx, 'g', 'name', ['modules', module], None, guild_id))
				else:
					modules_off.append(cspl_get_param_with_merge(ctx, 'g', 'name', ['modules', module], None, guild_id))

			modules_on_str = ', '.join([f'**{module}**' for module in modules_on])
			modules_off_str = ', '.join([f'**{module}**' for module in modules_off])


			get_guild = self.bot.get_guild(guild_id)
			if not get_guild: return await ctx.send("Сервер не найден")
			emb = discord.Embed(
				title=get_guild
			)
			emb.add_field(
				name = "Модули",
				value = "\n".join([
					'<:switch_on:818125506309652490> ' + modules_on_str,
					'<:switch_off:818125535951323177> ' + modules_off_str
				])
			)


			economy_data = cspl_get_param(ctx, "g", "lvls", ["economy"], None, guild_id)
			economy_data.insert(0, cspl_get_param(ctx, "g", "lvlFirst", ["economy"], None, guild_id))
			first_lvl = economy_data[0]['lvl']
			first_lvl_xp = economy_data[0]['xp']
			first_lvl_name = economy_data[0].get('lvlName', False)
			first_lvl_name_text = f' {first_lvl_name}' if first_lvl_name else ''

			last_lvl = economy_data[-1]['lvl']
			last_lvl_xp = economy_data[-1]['xp']
			last_lvl_name = economy_data[-1].get('lvlName', False)
			last_lvl_name_text = f' {last_lvl_name}' if last_lvl_name else ''
			level_range = f'`{first_lvl}{cspl_get_param(ctx, "g", "lvlTxt", ["economy"], None, guild_id)[0]}{first_lvl_name_text} ({first_lvl_xp}{cspl_get_param(ctx, "g", "xpTxt", ["economy"], None, guild_id)[0]})` → `{last_lvl}{cspl_get_param(ctx, "g", "lvlTxt", ["economy"], None, guild_id)[0]}{last_lvl_name_text} ({last_lvl_xp}{cspl_get_param(ctx, "g", "xpTxt", ["economy"], None, guild_id)[0]})`'
			
			emb.add_field(
				name = "Экономика",
				value = '\n'.join([
					f'**Уровни:** {level_range}',
					f'**Награда за сообщение:** `{cspl_get_param(ctx, "g", "xp", ["economy", "msgAward"], None, guild_id)}{cspl_get_param(ctx, "g", "xpTxt", ["economy"], None, guild_id)[0]}, {cspl_get_param(ctx, "g", "coins", ["economy", "msgAward"], None, guild_id)}{cspl_get_param(ctx, "g", "coinsTxt", ["economy"], None, guild_id)[0]} / {cspl_get_param(ctx, "g", "cooldown", ["economy", "msgAward"], None, guild_id)} сек.`',
				]),
				inline=False
			)
			emb.set_thumbnail(url = self.bot.user.avatar)
			emb.set_footer(text = f"/ Панель управления")
			await ctx.send(embed = emb, ephemeral = True)
		except Exception as e:
			await ctx.send(repr(e))


async def setup(bot):
	await bot.add_cog(Owner(bot))