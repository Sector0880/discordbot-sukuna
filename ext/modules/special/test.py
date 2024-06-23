import discord
from discord.ext import commands
from discord import app_commands

import asyncio
import re
import os
import json
import yaml

from dbVars import *
import botDecorators

class Test(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		
	@app_commands.command(
		name = "test",
		description="тестовая команда (только для овнера)"
	)
	async def test(self, interaction: discord.Interaction):
		try:
			if interaction.user.id not in sf_sp(): return await interaction.response.send_message("Нету прав.")

			def find_current_level_xp(xp, interaction):
				economy_levels = cspl_get_param(interaction, 'g', 'lvls', 'economy')
				current_level = cspl_get_param(interaction, 'u', 'lvl', 'economy')
				next_level = current_level + 1

				for i in range(1, len(economy_levels)):
					if xp >= economy_levels[i]["xp"]:
						current_level = economy_levels[i]["lvl"]
						if i + 1 < len(economy_levels):
							next_level = economy_levels[i + 1]["lvl"]
						else:
							next_level = None  # Нет следующего уровня

				current_xp = economy_levels[current_level - 1]["xp"]
				if next_level is not None:
					next_xp = economy_levels[next_level - 1]["xp"]
					percent_to_next_level = int(((xp - current_xp) / (next_xp - current_xp)) * 100)
				else:
					percent_to_next_level = 100  # Достигнут максимальный уровень

				return current_level, next_level, percent_to_next_level
			
			xp = cspl_get_param(interaction, 'u', 'xp', 'economy')
			current_level, next_level, percent_to_next_level = find_current_level_xp(xp, interaction)

			progress_bar_length = 10
			filled_blocks = int(percent_to_next_level / 100 * progress_bar_length)
			empty_blocks = progress_bar_length - filled_blocks

			progress_bar = f"[{'▰' * filled_blocks}{'═' * empty_blocks}]"

			economy_levels = cspl_get_param(interaction, 'g', 'lvls', 'economy')
			current_xp_needed = economy_levels[current_level - 1]["xp"]
			
			if next_level is not None:
				next_xp_needed = economy_levels[next_level - 1]["xp"]
				print(f"**Уровень:** \n`{current_level}ур. ({current_xp_needed}{cspl_get_param(interaction, 'g', 'xpName', 'economy')[0]})` `{progress_bar}{percent_to_next_level:02d}%` `{next_level}ур. ({next_xp_needed}{cspl_get_param(interaction, 'g', 'xpName', 'economy')[0]})`")
			else:
				print(f"**Уровень:** \n`{current_level}ур. ({current_xp_needed}{cspl_get_param(interaction, 'g', 'xpName', 'economy')[0]})` `{progress_bar}{percent_to_next_level:02d}%` `Макс. уровень достигнут`")
		except Exception as e:
			print(repr(e))

	@commands.command()
	@commands.is_owner()
	async def t(self, ctx):
		try:
			em = discord.Embed(
				title="Слеш команды",
				description="Список всех слеш команд бота",
				color=discord.Color.blurple())

			for slash_command in self.bot.tree.walk_commands():
				em.add_field(name=slash_command.name, 
							value=slash_command.description if slash_command.description else slash_command.name, 
							inline=False) 
			#await ctx.send(embed = em)
			await ctx.send(cspl_get_param(ctx, 'u', 'xp', 'economy'))
		except ValueError as e:
			await ctx.send(str(e))
		except Exception as e:
			print(repr(e))

async def setup(bot):
	await bot.add_cog(Test(bot))