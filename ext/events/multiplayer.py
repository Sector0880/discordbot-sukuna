import discord
from discord.ext import commands, tasks

import json
import asyncio


class MultiplayerEvents(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.Cog.listener()
	async def on_guild_join(self, guild):
		# open db

		
		# write db


		# create role muted
		perms = discord.Permissions(connect = False, send_messages = False)
		role_mute = await guild.create_role(name = "Muted_Sukuna", permissions = perms)

		for category in guild.categories: await category.set_permissions(role_mute, connect = False, send_messages = False)

		for channel in guild.text_channels: await channel.set_permissions(role_mute, send_messages = False)
		for channel in guild.voice_channels: await channel.set_permissions(role_mute, connect = False)

		self.bot.tree.copy_global_to(guild=discord.Object(id=guild.id))
	
	@commands.Cog.listener()
	async def on_guild_remove(self, guild):
		# open db

		# write db
	

	@tasks.loop(minutes = 10)
	async def check_multiplayer_correct(self):
		# open db


		# write db
	
	@commands.Cog.listener()
	async def on_ready(self):
		await self.bot.wait_until_ready()
		self.check_multiplayer_correct.start()


async def setup(bot):
	await bot.add_cog(MultiplayerEvents(bot))