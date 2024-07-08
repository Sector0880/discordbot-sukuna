import discord
from discord.ext import commands
from discord import app_commands, interactions

import asyncio
import re
from dbVars import *
from botFunctions import *

class RepeatCancel(discord.ui.View):
	def __init__(self):
		super().__init__(timeout=None)
		self.cancelled = False
	
	@discord.ui.button(label="Отменить", style=discord.ButtonStyle.gray)
	async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
		if interaction.user.id not in sf_sp(): return await interaction.response.send_message("Нету прав.", ephemeral = False) # на автора сообщения

		self.cancelled = True
		await interaction.response.send_message('Команда отменена.', ephemeral = False)
		#interaction.message.view.stop() должно скрывать кнопку после нажатия но не скрывает
		self.stop()

class DialogCancel(discord.ui.View):
	def __init__(self):
		super().__init__(timeout=None)
		self.cancelled = False
	
	@discord.ui.button(label="Остановить", style=discord.ButtonStyle.gray)
	async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
		if interaction.user.id not in sf_sp(): return await interaction.response.send_message("Нету прав.", ephemeral = False) # на автора сообщения

		self.cancelled = True
		await interaction.response.send_message('Диалог прекращен.', ephemeral=False)
		#interaction.message.view.stop() должно скрывать кнопку после нажатия но не скрывает
		self.stop()

class ForADA(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command(aliases = ["повтори", "п", "rp"])
	async def repeat(self, ctx: discord.Message, channel = None):
		try:
			# проверки
			if ctx.author.id not in sf_sp(): return
			if channel is None: 
				await ctx.message.add_reaction('❌')
				return await ctx.send("❌ Напиши id чата вместе с командой.\n```!rp [id чата]```") # на наличие channel_id
			if not isinstance(channel, int) and not channel.isdigit(): # слава богам всевышним что пока этот try except работает, раньше команда и без него нормально выводила ошибку если написано str но ожидали int, но чтото сломалось и пизда
				return await ctx.send("Я понимаю только id чата, не ссылку или имя, ID!") # на тип channel_id
			else: channel = int(channel)
			channel_id = self.bot.get_channel(channel) # получаем id канала
			if not channel_id: return await ctx.send(f"Чат не найден → <#{channel}>") # если id канала не найден

			repeat_view = RepeatCancel()
			await ctx.send(f"Напиши сообщение, я его повторю. Я буду ожидать твоего сообщения `60 секунд`.\nСервер: `{channel_id.guild.name}`\nЧат: <#{channel}>", view = repeat_view)

			time_waiting = 60 # время ожидания
			try:
				message = await self.bot.wait_for("message", check = lambda message: message.author == ctx.author and message.channel == ctx.channel, timeout = time_waiting)
				#if message.content == "ОТМЕНА" or "ОТ": return await ctx.send("Команда отменена принужденно.")
				#if re.fullmatch("ОТМЕНА", message.content): return await ctx.send("Команда отменена принужденно.")
				if repeat_view.cancelled: 
					repeat_view.cancelled = False
					return
				else: 
					message_output = await channel_id.send(message.content)
					await ctx.send(f"Успешно, сообщение: {message_output.jump_url}")
			except asyncio.TimeoutError:
				await ctx.send(f"Время ожидания истекло ({time_waiting} секунд)")
		except Exception as e:
			await ctx.send(e)
	
	@commands.command(aliases = ['dg', 'диалог'])
	async def dialog(self, ctx: discord.Message, channel = None):
		try:
			# проверки
			if ctx.author.id not in sf_sp(): return await ctx.send("Нету прав.") # на автора сообщения
			if channel is None: 
				#await ctx.message.add_reaction('❌')
				return await ctx.send("❌ Напиши id чата вместе с командой.\n```!rp [id чата]```") # на наличие channel_id
			if not isinstance(channel, int) and not channel.isdigit(): # слава богам всевышним что пока этот try except работает, раньше команда и без него нормально выводила ошибку если написано str но ожидали int, но чтото сломалось и пизда
				return await ctx.send("Я понимаю только id чата, не ссылку или имя, ID!") # на тип channel_id
			else: channel = int(channel)
			channel_id = self.bot.get_channel(channel) # получаем id канала
			if not channel_id: return await ctx.send(f"Чат не найден → <#{channel}>") # если id канала не найден


			dialog_view = DialogCancel()
			await ctx.send(f"Диалог запущен. Теперь каждое твое сообщение в этом чате отправляется от моего лица.\nСервер: `{channel_id.guild.name}`\nЧат: <#{channel}>", view = dialog_view)
			while True:
				message = await self.bot.wait_for("message", check = lambda message: message.author == ctx.author and message.channel == ctx.channel)
				if dialog_view.cancelled: 
					dialog_view.cancelled = False
					return
				else: 
					message_output = await channel_id.send(message.content)
					await ctx.send(f"Успешно, сообщение: {message_output.jump_url}", view = dialog_view)
		except Exception as e:
			await ctx.send(e)

	@commands.Cog.listener()
	async def on_member_join(self, member: discord.Member):
		channel_id = 1051768599930482728  # ID канала, в который бот будет отправлять сообщение
		channel = self.bot.get_channel(channel_id)

		if channel:
			await channel.send(f'Пользователь {member.name} присоединился к серверу!')
		else:
			print(f'Канал с ID {channel_id} не найден.')
			
async def setup(bot):
	await bot.add_cog(ForADA(bot))


"""
# Define a simple Button View class
# пример
class Confirm(discord.ui.View):
	def __init__(self):
		super().__init__()

	# When the button is pressed, set the inner value to `True` and
	# stop the View from listening to more input.
	# We also send the user an ephemeral message that we're confirming their choice.
	@discord.ui.button(label='Confirm', style=discord.ButtonStyle.green)
	async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
		await interaction.response.send_message('Confirming', ephemeral=True)
		self.stop()

	# This one is similar to the confirmation button except sets the inner value to `False`
	@discord.ui.button(label='Cancel', style=discord.ButtonStyle.grey)
	async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
		await interaction.response.send_message('Cancelling', ephemeral=True)
		self.stop()
"""