import discord
from discord.ext import commands

import asyncio
import re

from botConfig import *
from dbVars import *
import botDecorators

from botDecorators import *

class ForADA(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command(aliases = ["дубляж", "д", "md"])
	async def message_dublite(self, ctx, channel = None):
		# проверки
		#if ctx.author.id not in [staff_creator_id(), staff_ada_id()]: return await ctx.send("Нету прав.") # на автора сообщения
		if ctx.author.id not in [980175834373562439, 522136072151367691, 224632121879166976]: return await ctx.send("Нету прав.") # на автора сообщения
		if channel is None: 
			await ctx.message.add_reaction('❌')
			return await ctx.send("Напиши id чата вместе с командой.") # на наличие channel_id
		if not isinstance(channel, int) and not channel.isdigit(): # слава богам всевышним что пока этот try except работает, раньше команда и без него нормально выводила ошибку если написано str но ожидали int, но чтото сломалось и пизда
			return await ctx.send("Я понимаю только id чата, не ссылку или имя, ID!") # на тип channel_id
		else: channel = int(channel)
		channel_id = self.bot.get_channel(channel) # получаем id канала
		if not channel_id: return await ctx.send(f"Чат не найден → <#{channel}>") # если id канала не найден
		await ctx.send(f"Напиши сообщение, я его продублирую\nСервер: `{channel_id.guild.name}`\nЧат: <#{channel}>\nОжидание: `60 секунд`")
		time_waiting = 60.0 # время ожидания
		try:
			message = await self.bot.wait_for("message", check = lambda ctx: ctx.author == ctx.author and ctx.channel == ctx.channel, timeout = time_waiting)
			#if message.content == "ОТМЕНА" or "ОТ": return await ctx.send("Команда отменена принужденно.")
			if re.fullmatch("ОТМЕНА", message.content): return await ctx.send("Команда отменена принужденно.")
			message_output = await channel_id.send(message.content)
			await ctx.send(f"Успешно, сообщение: {message_output.jump_url}")
		except asyncio.TimeoutError:
			await ctx.send(f"Время ожидания истекло ({time_waiting} секунд)")
			
async def setup(bot):
	await bot.add_cog(ForADA(bot))