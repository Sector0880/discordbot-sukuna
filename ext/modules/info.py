import discord
from discord.ext import commands
from discord import app_commands

from botConfig import *
from datetime import *

class MyHelp(commands.MinimalHelpCommand):
   	# !help
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            emby = discord.Embed(description=page)
            await destination.send(embed=emby)
       
   # !help <command>
    async def send_command_help(self, command):
        await self.context.send("This is help command")
      
   # !help <group>
    async def send_group_help(self, group):
        await self.context.send("This is help group")
    
   # !help <cog>
    async def send_cog_help(self, cog):
        await self.context.send(f"This is help cog {cog}")

class Info(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self._original_help_command = bot.help_command
		bot.help_command = MyHelp()
		bot.help_command.cog = self
	
	def cog_unload(self):
		self.bot.help_command = self._original_help_command
	
	@commands.hybrid_command(
		name = 'ping',
		description = 'Узнать время отклика бота.',
		aliases = ['пинг']
	)
	async def ping(self, ctx):
		try:
			ping = self.bot.latency
			ping_emoji = '🟩🔳🔳🔳🔳'

			if ping > 0.10000000000000000:
				ping_emoji = '🟧🟩🔳🔳🔳'

			if ping > 0.15000000000000000:
				ping_emoji = '🟥🟧🟩🔳🔳'

			if ping > 0.20000000000000000:
				ping_emoji = '🟥🟥🟧🟩🔳'

			if ping > 0.25000000000000000:
				ping_emoji = '🟥🟥🟥🟧🟩'

			if ping > 0.30000000000000000:
				ping_emoji = '🟥🟥🟥🟥🟧'

			if ping > 0.35000000000000000:
				ping_emoji = '🟥🟥🟥🟥🟥'

			# Переменная с пингом бота до текущего шарда
			shard_ping = f'{ping_emoji} `{round(self.bot.latency * 1000)}ms`'

			message = await ctx.send('Понг! 🏓  🔳🔳🔳🔳🔳 `секунду...`')
			await message.edit(content = f'Понг! 🏓  {shard_ping}')
		except Exception as e:
			await ctx.send(e)
	
	@commands.hybrid_command(
		name = "profile",
		description = 'Показать информацию о юзере.',
		aliases = ['профиль']
	)
	async def profile(self, ctx, user: discord.Member = None):
		try:
			profile = ctx.author if not user else user
			roles = profile.roles
			role_list = ''
			role_list_number = 0

			for role in reversed(roles):
				if role != ctx.guild.default_role:
					role_list += f'<@&{role.id}> '
					role_list_number += 1
				
			if profile.status == discord.Status.online:
				status = '<:online:748149457396433016> В сети'
			elif profile.status == discord.Status.idle:
				status = '<:idle:748149485707984907> Не активен'
			elif profile.status == discord.Status.dnd:
				status = '<a:mark_none:815121643479236618> Не беспокоить'
			else:
				status = '<:offline:748149539915038731> Не в сети'
			
			emb = discord.Embed(colour = color_success)
			emb.set_author(name = f'{profile}', icon_url = profile.avatar)
			emb.set_thumbnail(url = profile.avatar)
			emb.add_field(name = 'В Discord', value = profile.created_at.strftime('**Дата:** %d/%m/%Y\n**Время:** %H:%M:%S'))
			emb.add_field(name = 'На сервере', value = profile.joined_at.strftime('**Дата:** %d/%m/%Y\n**Время:** %H:%M:%S'))
			emb.add_field(name = 'Статус', value = status, inline = False)
			emb.add_field(name = f'Роли [{role_list_number}]', value = 'Отсутствуют' if role_list == '' else role_list, inline = False)
			#emb.set_footer(text = f'ID: {profile.id}')
			emb.timestamp = datetime.utcnow()

			await ctx.send(embed = emb, ephemeral=True)
		except Exception as e:
			await ctx.send(e, ephemeral=True)
	
	@commands.hybrid_command(
		name = "avatar",
		description = 'Получить аватарку юзера.',
		aliases = ['аватарка']
	)
	async def avatar(self, ctx, user: discord.Member = None):
		try:
			user = ctx.author if not user else user

			emb = discord.Embed(colour = color_success)
			emb.set_author(name = user, icon_url = user.avatar)
			emb.set_image(url = user.avatar)

			await ctx.send(embed = emb, ephemeral=True)
		except Exception as e:
			await ctx.send(e, ephemeral=True)

async def setup(bot):
	await bot.add_cog(Info(bot))