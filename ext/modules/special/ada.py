import discord
from discord.ext import commands

import asyncio
import re
from dbVars import *
from botFunctions import *


class ForADA(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	# готово
	@commands.command(aliases = ["скажи", "с", "s"])
	async def say(self, ctx, channel = None):
		try:
			add_command_usage_counter(ctx, 'use')
			# проверки
			if ctx.author.id not in sf_sp(): return await ctx.send("Нету прав.") # на автора сообщения
			if channel is None: 
				await ctx.message.add_reaction('❌')
				return await ctx.send("Напиши id чата вместе с командой.") # на наличие channel_id
			if not isinstance(channel, int) and not channel.isdigit(): # слава богам всевышним что пока этот try except работает, раньше команда и без него нормально выводила ошибку если написано str но ожидали int, но чтото сломалось и пизда
				return await ctx.send("Я понимаю только id чата, не ссылку или имя, ID!") # на тип channel_id
			else: channel = int(channel)
			channel_id = self.bot.get_channel(channel) # получаем id канала
			if not channel_id: return await ctx.send(f"Чат не найден → <#{channel}>") # если id канала не найден
			await ctx.send(f"Напиши сообщение, я его продублирую. Я буду ожидать твоего сообщения `60 секунд`.\nДля отмены команды напиши текст ОТМЕНА (обязательно большим курсивом).\n\nСервер: `{channel_id.guild.name}`\nЧат: <#{channel}>")
			time_waiting = 60 # время ожидания
			try:
				message = await self.bot.wait_for("message", check = lambda ctx: ctx.author == ctx.author and ctx.channel == ctx.channel, timeout = time_waiting)
				#if message.content == "ОТМЕНА" or "ОТ": return await ctx.send("Команда отменена принужденно.")
				if re.fullmatch("ОТМЕНА", message.content): return await ctx.send("Команда отменена принужденно.")
				message_output = await channel_id.send(message.content)
				await ctx.send(f"Успешно, сообщение: {message_output.jump_url}")
			except asyncio.TimeoutError:
				await ctx.send(f"Время ожидания истекло ({time_waiting} секунд)")
			add_command_usage_counter(ctx, 'success')
		except Exception as e:
			await ctx.send(e)
			add_command_usage_counter(ctx, 'lose')
	
	@commands.Cog.listener()
	async def on_member_join(self, member):
		channel_id = 817101575289176064  # ID канала, в который бот будет отправлять сообщение
		channel = self.bot.get_channel(channel_id)

		if channel:
			await channel.send(f'Пользователь {member.name} присоединился к серверу!')
		else:
			print(f'Канал с ID {channel_id} не найден.')
			
async def setup(bot):
	await bot.add_cog(ForADA(bot))