import discord
from discord.ext import commands
from discord import app_commands

from datetime import *
from botFunctions import *

class Fun(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
	
	@commands.hybrid_command(
		name = 'time', 
		description = 'Узнать время.',
		aliases = ['datetime', 'время']
	)
	async def time(self, ctx):
		try:
			add_command_usage_counter(ctx, 1)

			emb = discord.Embed(color=0x2b2d31)
			emb.add_field(name = 'UTC  🌐', value = datetime.utcnow().strftime('**Дата:** %Y.%m.%d\n**Время:** %H:%M:%S'))
			emb.add_field(name = 'МСК  🇷🇺', value = (datetime.utcnow() + timedelta(hours = 3)).strftime('**Дата:** %Y.%m.%d\n**Время:** %H:%M:%S'))
			#emb.set_footer(text = ctx.author, icon_url = ctx.author.avatar.url)

			await ctx.send(embed = emb)
			add_command_usage_counter(ctx, 2)
		except Exception as e:
			await ctx.send(e)
			add_command_usage_counter(ctx, 3)

async def setup(bot):
	await bot.add_cog(Fun(bot))