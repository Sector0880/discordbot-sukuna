import discord
from discord.ext import commands
from discord import app_commands

import datetime
from botFunctions import *

class Fun(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
	
	@commands.hybrid_command(
		name = 'time', 
		description = 'Узнать время.',
		aliases = ['datetime']
	)
	async def time(self, ctx):
		try:
			add_command_usage_counter(ctx, 1)
			await ctx.send(datetime.now(), ephemeral=True)
			add_command_usage_counter(ctx, 2)
		except Exception as e:
			await ctx.send(e)
			add_command_usage_counter(ctx, 3)

async def setup(bot):
	await bot.add_cog(Fun(bot))