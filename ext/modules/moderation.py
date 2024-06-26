import discord
from discord.ext import commands
from discord import app_commands
import datetime

class Moderation(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
	
	# Проверка и создание роли "Muted_Sukuna"
	async def ensure_mute_role(self, guild: discord.Guild):
		role_name = "Muted_Sukuna"
		role = discord.utils.get(guild.roles, name=role_name)
		if role is None:
			perms = discord.Permissions(connect=False, send_messages=False)
			role = await guild.create_role(name=role_name, permissions=perms)

			for category in guild.categories:
				await category.set_permissions(role, connect=False, send_messages=False)

			for channel in guild.text_channels:
				await channel.set_permissions(role, send_messages=False)
			for channel in guild.voice_channels:
				await channel.set_permissions(role, connect=False)
		return role
	
	# Событие на присоединение к серверу
	@commands.Cog.listener()
	async def on_guild_join(self, guild: discord.Guild):
		await self.ensure_mute_role(guild)
		self.bot.tree.copy_global_to(guild=discord.Object(id = guild.id))

	# Команда mute
	@app_commands.command(
		name='mute', 
		description='Замутить юзера'
	)
	@app_commands.checks.has_permissions(mute_members=True)
	@app_commands.default_permissions(mute_members=True)
	async def mute(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
		role = await self.ensure_mute_role(interaction.guild)
		if role in member.roles:
			await interaction.response.send_message(f'{member.mention} уже имеет роль {role.name}.', ephemeral=False)
		else:
			await member.add_roles(role, reason=reason)
			await interaction.response.send_message(f'{member.mention} был замучен.\n{reason if reason else ""}', ephemeral=False)
	
	# Команда unmute
	@app_commands.command(
		name='unmute', 
		description='Размьютить юзера'
	)
	@app_commands.checks.has_permissions(mute_members=True)
	@app_commands.default_permissions(mute_members=True)
	async def unmute(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
		role = await self.ensure_mute_role(interaction.guild)
		if role not in member.roles:
			await interaction.response.send_message(f'{member.mention} не имеет роль {role.name}.', ephemeral=False)
		else:
			await member.remove_roles(role, reason=reason)
			await interaction.response.send_message(f'{member.mention} был размучен.\n{reason if reason else ""}', ephemeral=False)


	# Команда timeout
	@app_commands.command(
		name='timeout',
		description='Временная блокировка разрешений писать/подключаться в чат/войс'
	)
	@app_commands.checks.has_permissions(mute_members=True)
	@app_commands.default_permissions(mute_members=True)
	async def timeout(self, interaction: discord.Interaction, member: discord.Member, seconds: int = 0, minutes: int = 0, hours: int = 0, days: int = 0, reason: str = None):
		try:
			# сделать проверки на 0, на исп команды на людей с такими же правами как и у тебя
			duration = datetime.timedelta(seconds=seconds, minutes=minutes, hours=hours, days=days)
			await member.timeout(duration, reason=reason)

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
	
	# Команда untimeout
	@app_commands.command(
		name='untimeout',
		description='Отменить блокировку разрешений писать/подключаться в чат/войс'
	)
	@app_commands.checks.has_permissions(mute_members=True)
	@app_commands.default_permissions(mute_members=True)
	async def untimeout(self, interaction: discord.Interaction, member: discord.Member):
		try:
			if not member.timed_out_until:
				return await interaction.response.send_message(f'<a:mark_error:815121144016404500> {member.name} не находится в тайм-ауте', ephemeral=False)
			
			await member.edit(timed_out_until=None, reason=f"Тайм-аут снят модератором {interaction.user}")
			await interaction.response.send_message(f'С {member.mention} был снят тайм-аут', ephemeral=False)
		except Exception as e:
			await interaction.response.send_message(repr(e))

	# Команда ban
	@app_commands.command(
		name='ban', 
		description='Забанить юзера'
	)
	@app_commands.checks.has_permissions(ban_members=True)
	@app_commands.default_permissions(ban_members=True)
	async def ban(self, interaction: discord.Interaction):
		await interaction.response.send_message(content='Скоро...')


async def setup(bot):
	await bot.add_cog(Moderation(bot))
