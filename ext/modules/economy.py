import discord
from discord.ext import commands
from discord import app_commands

import requests
import random
import json
import yaml
import datetime

import botFunctions
import dbVars
import botConfig

class Economy(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot

		self.xp_cooldown = {}

	# награда за сообщение (готово)
	async def msg_award(self, message: discord.Message):
		# проверка на кулдаун сообщения (готово)
		current_time = datetime.datetime.now()
		if message.author.id not in self.xp_cooldown:
			self.xp_cooldown[message.author.id] = {}
		if message.guild.id not in self.xp_cooldown[message.author.id]:
			self.xp_cooldown[message.author.id][message.guild.id] = datetime.datetime.min
		if (current_time - self.xp_cooldown[message.author.id][message.guild.id]).total_seconds() < dbVars.cspl_get_param(message, 'g', 'cooldown', ['economy', 'msgAward']):
			return

		
		custom_users = json.load(open(botConfig.path_db_cspl_custom_users, "r", encoding="utf-8"))

		if str(message.author.id) not in custom_users:
			custom_users[str(message.author.id)] = {}
		if str(message.guild.id) not in custom_users[str(message.author.id)]:
			custom_users[str(message.author.id)][str(message.guild.id)] = {}
		if "economy" not in custom_users[str(message.author.id)][str(message.guild.id)]:
			custom_users[str(message.author.id)][str(message.guild.id)]["economy"] = {}

		xp_add = dbVars.cspl_get_param(message, 'g', 'xp', ['economy', 'msgAward'])
		coins_add = dbVars.cspl_get_param(message, 'g', 'coins', ['economy', 'msgAward'])
		
		if 'xp' not in custom_users[str(message.author.id)][str(message.guild.id)]["economy"]:
			custom_users[str(message.author.id)][str(message.guild.id)]["economy"]['xp'] = xp_add
		else:
			custom_users[str(message.author.id)][str(message.guild.id)]["economy"]['xp'] += xp_add
		
		if 'coins' not in custom_users[str(message.author.id)][str(message.guild.id)]["economy"]:
			custom_users[str(message.author.id)][str(message.guild.id)]["economy"]['coins'] = coins_add
		else:
			custom_users[str(message.author.id)][str(message.guild.id)]["economy"]['coins'] += coins_add

		with open(botConfig.path_db_cspl_custom_users, "w", encoding="utf-8") as write_file: json.dump(custom_users, write_file, ensure_ascii=False, indent=4)

		self.xp_cooldown[message.author.id][message.guild.id] = current_time

	# рассчитывание правильного уровня для пользователя (готово)
	async def check_lvl_validate(self, message: discord.Message):
		custom_users = json.load(open(botConfig.path_db_cspl_custom_users, "r", encoding="utf-8"))

		user_id = str(message.author.id)
		guild_id = str(message.guild.id)

		if user_id not in custom_users:
			custom_users[user_id] = {}
		if guild_id not in custom_users[user_id]:
			custom_users[user_id][guild_id] = {}
		if "economy" not in custom_users[user_id][guild_id]:
			custom_users[user_id][guild_id]["economy"] = {}

		economy_levels = dbVars.cspl_get_param(message, 'g', 'lvls', ['economy'])
		economy_levels.insert(0, dbVars.cspl_get_param(message, 'g', 'lvlFirst', ['economy']))

		def find_current_level_xp(xp):
			current_level = 1  # Начальный уровень 1
			next_level = 2  # Следующий уровень 2

			for i in range(1, len(economy_levels)):
				if xp >= economy_levels[i]["xp"]:
					current_level = economy_levels[i]["lvl"]
					if i + 1 < len(economy_levels):
						next_level = economy_levels[i + 1]["lvl"]
					else:
						next_level = None  # Нет следующего уровня
				else:
					break  # Если текущий xp меньше требуемого, остановить цикл

			current_xp = economy_levels[current_level - 1]["xp"]
			if next_level is not None:
				next_xp = economy_levels[next_level - 1]["xp"]
				percent_to_next_level = int(((xp - current_xp) / (next_xp - current_xp)) * 100)
			else:
				percent_to_next_level = 100  # Достигнут максимальный уровень

			return current_level, next_level, percent_to_next_level

		user_xp = dbVars.cspl_get_param(message, 'u', 'xp', ['economy'])
		current_level, next_level, percent_to_next_level = find_current_level_xp(user_xp)

		if dbVars.cspl_get_param(message, 'u', 'lvl', ['economy']) != current_level:
			custom_users[user_id][guild_id]["economy"]['lvl'] = current_level
		
		if current_level == 1:
			if 'lvl' in custom_users[user_id][guild_id]["economy"]:
				custom_users[user_id][guild_id]["economy"].pop('lvl')

		with open(botConfig.path_db_cspl_custom_users, "w", encoding="utf-8") as write_file: json.dump(custom_users, write_file, ensure_ascii=False, indent=4)
	
	async def lvl_award(self, message: discord.Message):
		custom_users = json.load(open(botConfig.path_db_cspl_custom_users, "r", encoding="utf-8"))

		lvls = dbVars.cspl_get_param(message, 'g', 'lvls', ['economy'])
		lvls.insert(0, dbVars.cspl_get_param(message, 'g', 'lvlFirst', ['economy']))
		member_xp = dbVars.cspl_get_param(message, 'u', 'xp', ['economy'])
		member_lvl = dbVars.cspl_get_param(message, 'u', 'lvl', ['economy'])

		user_id = str(message.author.id)
		guild_id = str(message.guild.id)

		awarded = False
		special_awards_txt = ''
		output_txt = ''

		t1 = []
		t1_solo = []
		t2 = []
		t2_solo = []
		t3 = []
		t3_solo = []
		t4 = []
		t4_solo = []

		for lvl in lvls:
			if member_xp >= lvl['xp'] and member_lvl < lvl['lvl']:
				# проверка наличия валидного уровня
				# добавить этот метод когда будет команда изменения уровней
				#await self.check_lvl_validate(message)

				# создание embed
				emb = discord.Embed()
				

				# Обновление уровня пользователя
				custom_users[user_id][guild_id]["economy"]['lvl'] = lvl['lvl']

				# проверка на наличие наград из уровня
				if 'awards' in lvl and lvl['awards']:
					# Выдача наград
					awards = lvl.get('awards', {})

					# готово
					if 'coins' in awards:
						custom_users[user_id][guild_id]["economy"]['coins'] += awards['coins']

						#awards_txt += f"`{awards['coins']}{dbVars.cspl_get_param(message, 'g', 'coinsTxt', ['economy'])[0]}` "
						#t1.append({'txt': f"`{awards['coins']}{dbVars.cspl_get_param(message, 'g', 'coinsTxt', ['economy'])[0]}` ", 'lvl': lvl['lvl']})
						t1.append(f"`{awards['coins']}{dbVars.cspl_get_param(message, 'g', 'coinsTxt', ['economy'])[0]}` за `{lvl['lvl']}{dbVars.cspl_get_param(message, 'g', 'lvlTxt', ['economy'])[0]}`")
						t1_solo.append(f"`{awards['coins']}{dbVars.cspl_get_param(message, 'g', 'coinsTxt', ['economy'])[0]}`")
					(emb.add_field(
						name = dbVars.cspl_get_param(message, 'g', 'coinsTxt', ['economy'])[1],
						value = '\n'.join(t1 if len(t1) > 1 else t1_solo)
					) if t1 else None)

					# готово
					if 'remove_role' in awards:
						role_id = awards['remove_role']
						role = message.guild.get_role(role_id)
						if role and role in message.author.roles:

							await message.author.remove_roles(role)

							t2.append(f"<@&{role_id}> за `{lvl['lvl']}{dbVars.cspl_get_param(message, 'g', 'lvlTxt', ['economy'])[0]}`")
							t2_solo.append(f"<@&{role_id}>")
					(emb.add_field(
						name = 'Удалена роль',
						value = '\n'.join(t2 if len(t2) > 1 else t2_solo),
						#inline = False
					) if t2 else None)

					# готово
					if 'add_role' in awards:
						role_id = awards['add_role']
						role = message.guild.get_role(role_id)
						if role and role not in message.author.roles:
							await message.author.add_roles(role)

							t3.append(f"<@&{role_id}> за `{lvl['lvl']}{dbVars.cspl_get_param(message, 'g', 'lvlTxt', ['economy'])[0]}`")
							t3_solo.append(f"<@&{role_id}>")
					(emb.add_field(
						name = 'Добавлена роль',
						value = '\n'.join(t3 if len(t3) > 1 else t3_solo),
						#inline = False
					) if t3 else None)
				
					# готово
					if 'add_roles' in awards:
						roles_for_level = []
						for role_mention in awards['add_roles']:
							role_id = role_mention
							role = message.guild.get_role(role_id)
							if role and role not in message.author.roles:
								await message.author.add_roles(role)
								roles_for_level.append(f"<@&{role_id}>")
						
						if roles_for_level:
							t4.append(f"{' '.join(roles_for_level)} за `{lvl['lvl']}{dbVars.cspl_get_param(message, 'g', 'lvlTxt', ['economy'])[0]}`")
							t4_solo.append(' '.join(roles_for_level))

					(emb.add_field(
						name = 'Добавлены роли',
						value = '\n'.join(t4 if len(t4) > 1 else t4_solo),
						#inline = False
					) if t4 else None)
				if 'output' in lvl:
					special_awards_txt += f'{lvl['output']}\n\n'
					
				awarded = True

		if awarded:
			with open(botConfig.path_db_cspl_custom_users, "w", encoding="utf-8") as write_file:
				json.dump(custom_users, write_file, ensure_ascii=False, indent=4)

			if special_awards_txt:
				await message.channel.send(special_awards_txt)
			else:
				economy_levels = dbVars.cspl_get_param(message, 'g', 'lvls', ['economy'])
				economy_levels.insert(0, dbVars.cspl_get_param(message, 'g', 'lvlFirst', ['economy']))

				def find_current_level_xp(xp):
					current_level = 1  # Начальный уровень 1
					next_level = 2  # Следующий уровень 2

					for i in range(1, len(economy_levels)):
						if xp >= economy_levels[i]["xp"]:
							current_level = economy_levels[i]["lvl"]
							if i + 1 < len(economy_levels):
								next_level = economy_levels[i + 1]["lvl"]
							else:
								next_level = None  # Нет следующего уровня
						else:
							break  # Если текущий xp меньше требуемого, остановить цикл

					current_xp = economy_levels[current_level - 1]["xp"]
					if next_level is not None:
						next_xp = economy_levels[next_level - 1]["xp"]
						percent_to_next_level = int(((xp - current_xp) / (next_xp - current_xp)) * 100)
					else:
						percent_to_next_level = 100  # Достигнут максимальный уровень

					return current_level, next_level, percent_to_next_level

				current_level, next_level, percent_to_next_level = find_current_level_xp(dbVars.cspl_get_param(message, 'u', 'xp', ['economy']))

				progress_bar_length = 10
				filled_blocks = int(percent_to_next_level / 100 * progress_bar_length)
				empty_blocks = progress_bar_length - filled_blocks

				progress_bar = f"\n`[{'▰' * filled_blocks}{'═' * empty_blocks}]{percent_to_next_level:02d}%`"
				#progress_bar = ''

				current_xp_needed = economy_levels[current_level - 1]["xp"]
				current_level_name = economy_levels[current_level - 1].get("lvlName", False)
				current_level_name_text = f" {current_level_name}" if current_level_name else ""
				if next_level is not None:
					next_xp_needed = economy_levels[next_level - 1]["xp"]
					next_level_name = economy_levels[next_level - 1].get("lvlName", False)
					next_level_name_text = f" {next_level_name}" if next_level_name else ""
					economy_lvl_txt = f"**{dbVars.cspl_get_param(message, 'g', 'lvlTxt', ['economy'])[1]}:** `{current_level}{dbVars.cspl_get_param(message, 'g', 'lvlTxt', ['economy'])[0]}{current_level_name_text} ({dbVars.cspl_get_param(message, 'u', 'xp', ['economy'])}{dbVars.cspl_get_param(message, 'g', 'xpTxt', ['economy'])[0]})` {progress_bar} \n`{next_xp_needed - dbVars.cspl_get_param(message, 'u', 'xp', ['economy'])}{dbVars.cspl_get_param(message, 'g', 'xpTxt', ['economy'])[0]}` до `{next_level}{dbVars.cspl_get_param(message, 'g', 'lvlTxt', ['economy'])[0]}{next_level_name_text} ({next_xp_needed}{dbVars.cspl_get_param(message, 'g', 'xpTxt', ['economy'])[0]})`"
				else:
					economy_lvl_txt = f"**{dbVars.cspl_get_param(message, 'g', 'lvlTxt', ['economy'])[1]}:** `{current_level}{dbVars.cspl_get_param(message, 'g', 'lvlTxt', ['economy'])[0]}{current_level_name_text} ({dbVars.cspl_get_param(message, 'u', 'xp', ['economy'])}{dbVars.cspl_get_param(message, 'g', 'xpTxt', ['economy'])[0]})` {progress_bar} \n`Макс. {dbVars.cspl_get_param(message, 'g', 'lvlTxt', ['economy'])[1].lower()} достигнут`"
				

				emb.description = f"**Поздравляю!** Вы получили `{dbVars.cspl_get_param(message, 'u', 'lvl', ['economy'])}{dbVars.cspl_get_param(message, 'g', 'lvlTxt', ['economy'])[0]}`\n\nВаша текущая экономика:\n{'\n'.join([
						economy_lvl_txt,
						f"**{dbVars.cspl_get_param(message, 'g', 'coinsTxt', ['economy'])[1]}:** `{dbVars.cspl_get_param(message, 'u', 'coins', ['economy'])}{dbVars.cspl_get_param(message, 'g', 'coinsTxt', ['economy'])[0]}`"
					])}\n\n:tada: Ваши награды:"
				await message.channel.send(content = message.author.mention, embed = emb)

	async def start_economy_system(self, message: discord.Message):
		# выдача наград за сообщение
		await self.msg_award(message)

		# выдача наград за достижение нового уровня
		await self.lvl_award(message)
		
	@commands.Cog.listener()
	async def on_message(self, message: discord.Message):
		try:
			if message.author.bot: return

			if dbVars.cspl_get_param(message, 'g', 'status', ['modules', 'economy']) and dbVars.cspl_get_param(message, 'g', 'status', ['modules', 'economy', 'events', 'lvl_system']):
				await self.start_economy_system(message)
		except Exception as e:
			print(repr(e))
	
	@commands.command()
	@commands.is_owner()
	async def delete_economy_xp(self, ctx, member_id: int, guilds_id: int):
		await ctx.send("скоро...")
		

async def setup(bot):
	await bot.add_cog(Economy(bot))

"""
if dbVars.cspl_get_param(message, 'u', 'xp', 'economy') == 50:
	coins = 200
	await message.channel.send(f"ура! вы достигли 1-ого уровня! Вы получаете {coins} монеток))")
	self.set_econony_coins(message, coins)
elif dbVars.cspl_get_param(message, 'u', 'xp', 'economy') == 100:
	coins = 300
	await message.channel.send(f"ура! вы достигли 2-ого уровня! Вы получаете {coins} монеток))")
	self.set_econony_coins(message, coins)

	def add_econony_lvl_and_coins(self, message: discord.Message, lvl: int, coins: int = None):
		custom_users = json.load(open("./.db/crossplatform/custom/users.json", "r", encoding="utf-8"))
		
		
		if str(message.author.id) not in custom_users:
			custom_users[str(message.author.id)] = {}
		if str(message.guild.id) not in custom_users[str(message.author.id)]:
			custom_users[str(message.author.id)][str(message.guild.id)] = {}
		if "economy" not in custom_users[str(message.author.id)][str(message.guild.id)]:
			custom_users[str(message.author.id)][str(message.guild.id)]["economy"] = {}
		
		custom_users[str(message.author.id)][str(message.guild.id)]["economy"]['lvl'] = lvl
		
		if coins:
			if 'coins' in custom_users[str(message.author.id)][str(message.guild.id)]["economy"]:
				if 'coins' in custom_users[str(message.author.id)][str(message.guild.id)]["economy"] == 0:
					custom_users[str(message.author.id)][str(message.guild.id)]["economy"]['coins'] = coins
					print('типооо')
				custom_users[str(message.author.id)][str(message.guild.id)]["economy"]['coins'] += coins

		with open("./.db/crossplatform/custom/users.json", "w", encoding="utf-8") as write_file: json.dump(custom_users, write_file, ensure_ascii = False, indent = 4)
#u_xp = dbVars.cspl_get_param(message, 'u', 'xp', 'economy')
		#u_lvl = dbVars.cspl_get_param(message, 'u', 'lvl', 'economy')
		#lvls_list = dbVars.cspl_get_param(message, 'g', 'lvls', 'economy')
		#lvls_list.insert(0, cspl_get_param(message, 'g', 'lvlFirst', ['economy']))

		#for level_data in lvls_list:
			#if u_xp >= level_data['xp'] and u_lvl < level_data['lvl']:
				#if level_data['coins']:
					#coins = level_data['coins']
				#lvl = level_data['lvl']
				#self.add_econony_lvl_and_coins(message, lvl, coins if level_data['coins'] else None)
				#await message.channel.send(f"{message.author.mention} ура! вы достигли {lvl}-ого уровня!" + f" Вы получаете {coins} монеток))" if level_data['coins'] else None)

"""


"""
identification_key = f'{message.author.id}&{message.guild.id}'

single_user = dbVars.get_single_user(message.author.id, message.guild.id)

economy = single_user.get('economy', {})

xp_add = dbVars.cspl_get_param(message, 'g', 'xp', ['economy', 'msgAward'])
coins_add = dbVars.cspl_get_param(message, 'g', 'coins', ['economy', 'msgAward'])

if single_user.get('identification', False):
	if identification_key == single_user['identification']:
		# Добавляем XP
		if 'xp' not in economy:
			economy['xp'] = xp_add
		else:
			economy['xp'] += xp_add

		# Добавляем монеты
		if 'coins' not in economy:
			economy['coins'] = coins_add
		else:
			economy['coins'] += coins_add
		
		print('ik')

		# Обновляем данные в базе данных
		dbVars.supabase_update_data(
			'crossplatform_custom_users',
			{'economy': economy},
			[('user_id', message.author.id), ('guild_id', message.guild.id)]
		)
	else:
		# Если пользователя нет в базе данных, создаем новую запись
		economy['xp'] = xp_add
		economy['coins'] = coins_add

		dbVars.supabase_insert_data(
			'crossplatform_custom_users',
			{
				'user_id': message.author.id,
				'guild_id': message.guild.id,
				'identification': identification_key,
				'economy': economy
			}
		)
else:
	dbVars.supabase_insert_data(
		'crossplatform_custom_users',
		{
			'user_id': message.author.id,
			'guild_id': message.guild.id,
			'identification': identification_key
		}
	)
"""