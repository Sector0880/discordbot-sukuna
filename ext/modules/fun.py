import discord
from discord.ext import commands
from discord import app_commands

import nekos
from googletrans import Translator
import requests
from bs4 import BeautifulSoup
import random

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
	
	@app_commands.command(
		name = "battle",
		description="У кого удача сильнее?"
	)
	@app_commands.describe(
		member = "Юзер сервера"
    )
	async def battle(self, interaction: discord.Interaction, member: discord.Member):
		try:
			a = random.randint(1,2)
			lst_win = ['был(а) съедена бомжом.', 'был(а) сбит(а) машиной.', 'суициднулся(ась).', 'самоизолировался(ась) от мелодраммы.', 'забрали в дурку (дом Ромашка).', 'отравили супом из школьной столовой.', 'самоизолировался(ась) от самого(ой) себя.', 'ожирел(а) из-за воздуха.', 'попотел(а) и сбросил(а) 20кг 0_0, но через месяц он(а) набрал(а) ещё 50кг.']
			text_win = random.choice(lst_win)

			lst_def = ['случайно сам(а) себя съел(а), а противник смотрел на это зрелище и ел попкорн.', 'попытался(ась) кинуть вызов, но безуспешно так как сладости у него(её) на первом месте.']
			text_def = random.choice(lst_def)

			if member == interaction.user:
				emb = discord.Embed(description = f'Вы не можете позвать на битву самого себя.')
				emb.set_author(name = interaction.user, icon_url = interaction.user.avatar)
				return await interaction.response.send_message(embed = emb)

			if a == 1:
				emb = discord.Embed(description = f'{member.mention} {text_win}\n\n**Победитель:** <@!{interaction.user.id}>')
				emb.set_footer(text = interaction.user, icon_url = interaction.user.avatar)
				await interaction.response.send_message(embed = emb)
			else:
				emb = discord.Embed(description = f'{interaction.author.mention} {text_def}\n\n**Победитель:** {member.mention}')
				emb.set_footer(text = interaction.user, icon_url = interaction.user.avatar)
				await interaction.response.send_message(embed = emb)
		except Exception as e:
			print(repr(e))

async def setup(bot):
	await bot.add_cog(Fun(bot))