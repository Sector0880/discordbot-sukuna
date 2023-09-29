import discord
from discord.ext import commands

import dbVars

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
	
	@commands.command()
	async def f(self, ctx):
		try:
			await ctx.send(dbVars.guild_prefix(ctx))
		except Exception as e:
			print(e)

async def setup(bot):
	await bot.add_cog(RoleMute(bot))