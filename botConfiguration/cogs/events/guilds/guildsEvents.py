import discord
from discord.ext import commands, tasks

import json


class GuildsEvents(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.Cog.listener()
	async def on_guild_join(self, guild):
		with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "r", encoding="utf-8") as read_file: guilds_config_data = json.load(read_file)

		guilds_config_data[str(guild.id)] = {
			"overview": {
				"guild_name": guild.name,
				"owner-nick": guild.owner.name,
				"owner-id": guild.owner.id
			},
			"prefix": "s!",
			"language": "ru",
			"additional-features": {
				"privileges": [
					{
						"premium": False
	  				}
				],
				"show_id": False
			},
			"protection": {
				"gateaway": [
					{
						"bot-output": True
					}
				]
			}
		}

		with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "w", encoding="utf-8") as write_file: json.dump(guilds_config_data, write_file, ensure_ascii = False, indent = 4)


		perms = discord.Permissions(connect = False, send_messages = False)

		role_mute = await guild.create_role(name = "Muted", permissions = perms)


		for category in guild.categories: await category.set_permissions(role_mute, connect = False, send_messages = False)

		for channel in guild.text_channels: await channel.set_permissions(role_mute, send_messages = False)
		for channel in guild.voice_channels: await channel.set_permissions(role_mute, connect = False)


	@tasks.loop(minutes = 1.0)
	async def check_guilds_config(self):
		with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "r", encoding="utf-8") as read_file: guilds_config_data = json.load(read_file)

		for guild in self.bot.guilds:
			if str(guild.id) not in guilds_config_data.keys():
				guilds_config_data[str(guild.id)] = {
					"overview": {
						"guild_name": guild.name,
						"owner-nick": guild.owner.name,
						"owner-id": guild.owner.id
					},
					"prefix": "s!",
					"language": "ru",
					"additional-features": {
						"privileges": [
							{
								"premium": False
							}
						],
						"show_id": False
					},
					"protection": {
						"gateaway": [
							{
								"bot-output": True
							}
						]
					}
				}

			# обновление владельца гильдии
			guilds_config_data[str(guild.id)]["overview"]["owner-nick"] = guild.owner.name
			guilds_config_data[str(guild.id)]["overview"]["owner-id"] = guild.owner.id

		with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "w", encoding="utf-8") as write_file: json.dump(guilds_config_data, write_file, ensure_ascii = False, indent = 4)


	# а нахуя эта функция, если вся информация после ухода бота из гильдии нужна? и я о том же (не удалять)
	#@commands.Cog.listener()
	#async def on_guild_remove(self, guild):
		#with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "r", encoding="utf-8") as read_file: guilds_config_data = json.load(read_file)

		#del guilds_config_data[str(guild.id)]["prefix"]
		#del guilds_config_data[str(guild.id)]["language"]

		#del guilds_config_data[str(guild.id)]["additional-features"]["show_id"]

		#with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "w", encoding="utf-8") as write_file: json.dump(guilds_config_data, write_file, ensure_ascii = False, indent = 4)


	@commands.Cog.listener()
	async def on_ready(self):
		await self.bot.wait_until_ready()
		self.check_guilds_config.start()
		#for seconds in range(60, 0, -1):
			#print(f"Секунд осталось:{seconds}", end = ' \r')
			#time.sleep(1)
			#seconds -= 1


async def setup(bot):
	await bot.add_cog(GuildsEvents(bot))