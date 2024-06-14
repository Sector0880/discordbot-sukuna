import discord
from discord.ext import commands
from discord import app_commands

import datetime

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
		name='timeout', 
		description='Временно заблокировать юзеру возможность писать в чат и подключаться в войсы.'
	)
	@app_commands.checks.has_permissions(mute_members=True)
	@app_commands.default_permissions(mute_members = True)
	async def timeout(self, interaction: discord.Interaction, member: discord.Member, seconds: int = 0, minutes: int = 0, hours: int = 0, days: int = 0, reason: str = None):
		try:
			# сделать проверки на 0, на исп команды на людей с такими же правами как и у тебя
			duration = datetime.timedelta(seconds = seconds, minutes = minutes, hours = hours, days = days)
			await member.timeout(duration, reason = reason)

			def choose_correct_word(number, form1, form2, form3):
					if 10 <= number % 100 <= 20:
						return form3
					elif number % 10 == 1:
						return form1
					elif 2 <= number % 10 <= 4:
						return form2
					else:
						return form3

			if duration.days > 0:
				days = duration.days
				time_str = f"{days} {choose_correct_word(days, 'день', 'дня', 'дней')} {duration.seconds // 3600} {choose_correct_word(duration.seconds // 3600, 'час', 'часа', 'часов')} {(duration.seconds % 3600) // 60} {choose_correct_word((duration.seconds % 3600) // 60, 'минута', 'минуты', 'минут')} {duration.seconds % 60} {choose_correct_word(duration.seconds % 60, 'секунда', 'секунды', 'секунд')}"
			elif duration.seconds >= 3600:
				time_str = f"{duration.seconds // 3600} {choose_correct_word(duration.seconds // 3600, 'час', 'часа', 'часов')} {(duration.seconds % 3600) // 60} {choose_correct_word((duration.seconds % 3600) // 60, 'минута', 'минуты', 'минут')} {duration.seconds % 60} {choose_correct_word(duration.seconds % 60, 'секунда', 'секунды', 'секунд')}"
			elif duration.seconds >= 60:
				time_str = f"{(duration.seconds % 3600) // 60} {choose_correct_word((duration.seconds % 3600) // 60, 'минута', 'минуты', 'минут')} {duration.seconds % 60} {choose_correct_word(duration.seconds % 60, 'секунда', 'секунды', 'секунд')}"
			else:
				time_str = f"{duration.seconds} {choose_correct_word(duration.seconds, 'секунда', 'секунды', 'секунд')}"

			await interaction.response.send_message(f'{member.mention} получил тайм-аут на {time_str}.\n{reason if reason else ""}', ephemeral=False)
		except Exception as e:
			await interaction.response.send_message(repr(e))
	
	@app_commands.command(
		name='untimeout',
		description='Вернуть юзеру возможность писать в чат и подключаться в войсы.'
	)
	@app_commands.checks.has_permissions(mute_members=True)
	@app_commands.default_permissions(mute_members = True)
	async def untimeout(self, interaction: discord.Interaction, member: discord.Member):
		try:
			await member.edit(timed_out_until=None, reason=f"Тайм-аут снят модератором {interaction.user}")
			await interaction.response.send_message(f'С {member.mention} был снят тайм-аут', ephemeral=False)
		except Exception as e:
			await interaction.response.send_message(repr(e))
	
	
	@app_commands.command(
		name = 'ban', 
		description = 'Забанить юзера на сервере.'
	)
	@app_commands.checks.has_permissions(ban_members = True)
	@app_commands.default_permissions(ban_members = True)
	async def ban(self, interaction: discord.Interaction):
		await interaction.response.send_message(content = 'Скоро...')


async def setup(bot):
	await bot.add_cog(Moderation(bot))