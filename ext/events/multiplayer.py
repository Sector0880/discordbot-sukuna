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
		#with open("./.db/multiplayer/economic.json", "r", encoding="utf-8") as read_file: data_economic = json.load(read_file) # not used for guilds
		with open("./.db/multiplayer/gateaway.json", "r", encoding="utf-8") as read_file: data_gateaway = json.load(read_file) # success
		with open("./.db/multiplayer/main.json", "r", encoding="utf-8") as read_file: data_main = json.load(read_file) # success
		#with open("./.db/multiplayer/marriage.json", "r", encoding="utf-8") as read_file: data_marriage = json.load(read_file) # not used for guilds
		with open("./.db/multiplayer/modules.json", "r", encoding="utf-8") as read_file: data_modules = json.load(read_file) # success
		with open("./.db/multiplayer/_serversinfo.json", "r", encoding="utf-8") as read_file: data__serversinfo = json.load(read_file) # success
		with open("./.db/multiplayer/premium.json", "r", encoding="utf-8") as read_file: data_premium = json.load(read_file) # success
		#with open("./.db/multiplayer/profiles.json", "r", encoding="utf-8") as read_file: data_profiles = json.load(read_file) # not used for guilds

		if str(guild.id) not in data_main.keys():
			data_main[str(guild.id)] = {
				"prefix": "s!",
				"language": "ru"
			}
		if str(guild.id) not in data__serversinfo.keys():
			data__serversinfo[str(guild.id)] = {
				"guild-name": guild.name,
				"guild-id": guild.id,
				"owner-name": guild.owner.name,
				"owner-id": guild.owner.id
			}
		if str(guild.id) not in data_modules.keys():
			data_modules[str(guild.id)] = {
				"audit": False,
				"economic": False,
				"fun": False,
				"moderation": False,
				"music": False,
				"profiles": False
			}
		if str(guild.id) not in data_gateaway.keys():
			data_gateaway[str(guild.id)] = {
				"presence": True,
				"gateaway": {
					"?open" : True
					#"!block-uuid": "all servers closed!"
				}
			}
		else:
			data_gateaway[str(guild.id)]["presence"] = True
		if str(guild.id) not in data_premium.keys():
			data_premium[str(guild.id)] = {
				"premium": {
					"?work": False
					#"$p-uuid": "..."
				}
			}
		
		# write db
		#with open("./.db/multiplayer/economic.json", "r", encoding="utf-8") as write_file: json.dump(data_economic, write_file, ensure_ascii = False, indent = 4)
		with open("./.db/multiplayer/gateaway.json", "w", encoding="utf-8") as write_file: json.dump(data_gateaway, write_file, ensure_ascii = False, indent = 4)
		with open("./.db/multiplayer/main.json", "w", encoding="utf-8") as write_file: json.dump(data_main, write_file, ensure_ascii = False, indent = 4)
		#with open("./.db/multiplayer/marriage.json", "r", encoding="utf-8") as write_file: json.dump(data_marriage, write_file, ensure_ascii = False, indent = 4)
		with open("./.db/multiplayer/modules.json", "w", encoding="utf-8") as write_file: json.dump(data_modules, write_file, ensure_ascii = False, indent = 4)
		with open("./.db/multiplayer/_serversinfo.json", "w", encoding="utf-8") as write_file: json.dump(data__serversinfo, write_file, ensure_ascii = False, indent = 4)
		with open("./.db/multiplayer/premium.json", "w", encoding="utf-8") as write_file: json.dump(data_premium, write_file, ensure_ascii = False, indent = 4)
		#with open("./.db/multiplayer/profiles.json", "r", encoding="utf-8") as write_file: json.dump(data_profiles, write_file, ensure_ascii = False, indent = 4)


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
		with open("./.db/multiplayer/gateaway.json", "r", encoding="utf-8") as read_file: data_gateaway = json.load(read_file) # success
		data_gateaway[str(guild.id)]["presence"] = False

		# write db
		with open("./.db/multiplayer/gateaway.json", "w", encoding="utf-8") as write_file: json.dump(data_gateaway, write_file, ensure_ascii = False, indent = 4)
	

	@tasks.loop(minutes = 10)
	async def check_multiplayer_correct(self):
		# open db
		#with open("./.db/multiplayer/economic.json", "r", encoding="utf-8") as read_file: data_economic = json.load(read_file)
		with open("./.db/multiplayer/gateaway.json", "r", encoding="utf-8") as read_file: data_gateaway = json.load(read_file)
		with open("./.db/multiplayer/main.json", "r", encoding="utf-8") as read_file: data_main = json.load(read_file)
		#with open("./.db/multiplayer/marriage.json", "r", encoding="utf-8") as read_file: data_marriage = json.load(read_file)
		with open("./.db/multiplayer/modules.json", "r", encoding="utf-8") as read_file: data_modules = json.load(read_file)
		with open("./.db/multiplayer/_serversinfo.json", "r", encoding="utf-8") as read_file: data__serversinfo = json.load(read_file)
		with open("./.db/multiplayer/premium.json", "r", encoding="utf-8") as read_file: data_premium = json.load(read_file)
		#with open("./.db/multiplayer/profiles.json", "r", encoding="utf-8") as read_file: data_profiles = json.load(read_file)

		for guild in self.bot.guilds:
			if str(guild.id) not in data_main.keys():
				data_main[str(guild.id)] = {
					"prefix": "s!",
					"language": "ru"
				}
			if str(guild.id) not in data__serversinfo.keys():
				data__serversinfo[str(guild.id)] = {
					"guild-name": guild.name,
					"guild-id": guild.id,
					"owner-name": guild.owner.name,
					"owner-id": guild.owner.id
				}
			if str(guild.id) not in data_modules.keys():
				data_modules[str(guild.id)] = {
					"audit": False,
					"economic": False,
					"fun": False,
					"moderation": False,
					"music": False,
					"profiles": False
				}
			if str(guild.id) not in data_gateaway.keys():
				data_gateaway[str(guild.id)] = {
					"presence": True,
					"gateaway": {
						"?open" : True
						#"!block-uuid": "all servers closed!"
					}
				}
			else:
				data_gateaway[str(guild.id)]["presence"] = True
			if str(guild.id) not in data_premium.keys():
				data_premium[str(guild.id)] = {
					"premium": {
						"?work": False
						#"$p-uuid": "..."
					}
				}

			# обновление владельца гильдии
			data__serversinfo[str(guild.id)]["owner-name"] = guild.owner.name
			data__serversinfo[str(guild.id)]["owner-id"] = guild.owner.id

		# write db
		#with open("./.db/multiplayer/economic.json", "r", encoding="utf-8") as write_file: json.dump(data_economic, write_file, ensure_ascii = False, indent = 4)
		with open("./.db/multiplayer/gateaway.json", "w", encoding="utf-8") as write_file: json.dump(data_gateaway, write_file, ensure_ascii = False, indent = 4)
		with open("./.db/multiplayer/main.json", "w", encoding="utf-8") as write_file: json.dump(data_main, write_file, ensure_ascii = False, indent = 4)
		#with open("./.db/multiplayer/marriage.json", "r", encoding="utf-8") as write_file: json.dump(data_marriage, write_file, ensure_ascii = False, indent = 4)
		with open("./.db/multiplayer/modules.json", "w", encoding="utf-8") as write_file: json.dump(data_modules, write_file, ensure_ascii = False, indent = 4)
		with open("./.db/multiplayer/_serversinfo.json", "w", encoding="utf-8") as write_file: json.dump(data__serversinfo, write_file, ensure_ascii = False, indent = 4)
		with open("./.db/multiplayer/premium.json", "w", encoding="utf-8") as write_file: json.dump(data_premium, write_file, ensure_ascii = False, indent = 4)
		#with open("./.db/multiplayer/profiles.json", "r", encoding="utf-8") as write_file: json.dump(data_profiles, write_file, ensure_ascii = False, indent = 4)
	
	@commands.Cog.listener()
	async def on_ready(self):
		await self.bot.wait_until_ready()
		self.check_multiplayer_correct.start()


async def setup(bot):
	await bot.add_cog(MultiplayerEvents(bot))