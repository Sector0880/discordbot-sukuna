import discord
from discord.ext import commands
from discord import app_commands

import nekos
from googletrans import Translator

from datetime import *
import botFunctions

class Fun(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
	
	@app_commands.command(
		name = 'time', 
		description = 'Узнать время.'
	)
	async def time(self, interaction: discord.Interaction):
		try:
			botFunctions.add_command_usage_counter(interaction, 1)

			emb = discord.Embed(color=0x2b2d31)
			emb.add_field(name = 'UTC  🌐', value = datetime.utcnow().strftime('**Дата:** %Y.%m.%d\n**Время:** %H:%M:%S'))
			emb.add_field(name = 'МСК  🇷🇺', value = (datetime.utcnow() + timedelta(hours = 3)).strftime('**Дата:** %Y.%m.%d\n**Время:** %H:%M:%S'))
			#emb.set_footer(text = ctx.author, icon_url = ctx.author.avatar.url)

			await interaction.response.send_message(embed = emb, ephemeral=False)
			botFunctions.add_command_usage_counter(interaction, 2)
		except Exception as e:
			await interaction.response.send_message(e)
			botFunctions.add_command_usage_counter(interaction, 3)
	
	@app_commands.command(
		name = "fact",
		description="Узнать рандомный факт."
	)
	async def fact(self, interaction: discord.Interaction):
		facts = nekos.fact()

		tra = Translator()

		result = tra.translate(facts, dest = 'ru')

		await interaction.response.send_message(embed = discord.Embed(description = f'{result.text}.', color = 0xffff6c))

async def setup(bot):
	await bot.add_cog(Fun(bot))