import discord
from discord.ext import commands, tasks
from discord import app_commands

import json
import asyncio
from dbVars import *

class RoleMute(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.Cog.listener()
	async def on_guild_join(self, guild):
		# create role muted
		perms = discord.Permissions(connect = False, send_messages = False)
		role_mute = await guild.create_role(name = "Muted_Sukuna", permissions = perms)

		for category in guild.categories: await category.set_permissions(role_mute, connect = False, send_messages = False)

		for channel in guild.text_channels: await channel.set_permissions(role_mute, send_messages = False)
		for channel in guild.voice_channels: await channel.set_permissions(role_mute, connect = False)

		self.bot.tree.copy_global_to(guild=discord.Object(id=guild.id))
	
	@app_commands.command()
	async def example(self, interaction: discord.Interaction):
		try:
			await interaction.response.defer(ephemeral = True, thinking = True)
			await interaction.edit_original_response(content = guild_config_json_prefix(interaction))
		except Exception as e:
			print(e)
	
	@commands.command()
	async def files_status(self, ctx):
		await ctx.send("lol")

async def setup(bot):
	await bot.add_cog(RoleMute(bot))