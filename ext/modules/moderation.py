import discord
from discord.ext import commands
from discord import app_commands

class Moderation(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
	
	# mute container
	# — — — — — — — — — — — — — — — — — — — — — — — — — 
	# сделать аналогичное событие на уход из сервера
	@commands.Cog.listener()
	async def on_guild_join(self, guild):
		# create role muted
		perms = discord.Permissions(connect = False, send_messages = False)
		role_mute = await guild.create_role(name = "Muted_Sukuna", permissions = perms)

		for category in guild.categories: await category.set_permissions(role_mute, connect = False, send_messages = False)

		for channel in guild.text_channels: await channel.set_permissions(role_mute, send_messages = False)
		for channel in guild.voice_channels: await channel.set_permissions(role_mute, connect = False)

		self.bot.tree.copy_global_to(guild = discord.Object(id = guild.id))
	
	@app_commands.command(
		name = 'mute', 
		description = 'Заблокировать юзеру возможность писать в чат.'
	)
	async def mute(self, interaction: discord.Interaction):
		await interaction.response.send_message(content = 'Скоро...')
	
	@app_commands.command(
		name = 'ban', 
		description = 'Забанить юзера на сервере.'
	)
	async def ban(self, interaction: discord.Interaction):
		await interaction.response.send_message(content = 'Скоро...')

async def setup(bot):
	await bot.add_cog(Moderation(bot))