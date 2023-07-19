# ГОТОВ
import discord
from discord.ext import commands, tasks

import json


class GuildsEvents(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.Cog.listener()
	async def on_guild_join(self, guild):
		with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "r") as read_file: guilds_config_data = json.load(read_file)

		guilds_config_data[str(guild.id)] = {
			"overview": {
				"guild_name": guild.name,
				"owner": guild.owner.id
			},

			"prefix": "/",
			"language": "ru",

			"additional-features": [
				{"privileges": [
					{"premium": False}
				]},
				{"modes": [
					{"tester": False}
				]},
				{"show_id": False}
			],

			"protection": [
				{"gateaway": {"bot_output": True}}
			]
		}

		with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "w") as write_file: json.dump(guilds_config_data, write_file, ensure_ascii = False, indent = 4)


		perms = discord.Permissions(connect = False, send_messages = False)

		role_mute = await guild.create_role(name = "Muted", permissions = perms)


		for category in guild.categories: await category.set_permissions(role_mute, connect = False, send_messages = False)

		for channel in guild.text_channels: await channel.set_permissions(role_mute, send_messages = False)
		for channel in guild.voice_channels: await channel.set_permissions(role_mute, connect = False)


	@tasks.loop(minutes = 30.0)
	async def check_guilds_config(self):
		with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "r") as read_file: guilds_config_data = json.load(read_file)

		for guild in self.bot.guilds:
			if str(guild.id) not in guilds_config_data.keys():
				guilds_config_data[str(guild.id)] = {
					"overview": {
						"guild_name": guild.name,
						"owner": guild.owner.id
					},

					"prefix": "/",
					"language": "ru",

					"additional-features": [
						{"privileges": [
							{"premium": False}
						]},
						{"modes": [
							{"tester": False}
						]},
						{"show_id": False}
					],

					"protection": [
						{"gateaway": {"bot_output": True}}
					]
				}


			#if not "overview" in guilds_config_data[str(guild.id)].keys(): guilds_config_data[str(guild.id)]["overview"] = {}
			#guilds_config_data[str(guild.id)]["overview"]["name"] = guild.name
			#guilds_config_data[str(guild.id)]["overview"]["owner"] = guild.owner.id
			#
			#
			#if not "prefix" in guilds_config_data[str(guild.id)].keys(): guilds_config_data[str(guild.id)]["prefix"] = "j!"
			#if not "language" in guilds_config_data[str(guild.id)].keys(): guilds_config_data[str(guild.id)]["language"] = "ru"
			#
			#
			#if not "additional-features" in guilds_config_data[str(guild.id)].keys(): guilds_config_data[str(guild.id)]["additional-features"] = {}
			#if not "privileges" in guilds_config_data[str(guild.id)]["additional-features"].keys(): guilds_config_data[str(guild.id)]["additional-features"]["privileges"] = {}
			#if not "premium" in guilds_config_data[str(guild.id)]["additional-features"]["privileges"].keys(): guilds_config_data[str(guild.id)]["additional-features"]["privileges"]["premium"] = False
			#
			#if not "modes" in guilds_config_data[str(guild.id)]["additional-features"].keys(): guilds_config_data[str(guild.id)]["additional-features"]["modes"] = {}
			#if not "tester" in guilds_config_data[str(guild.id)]["additional-features"]["modes"].keys(): guilds_config_data[str(guild.id)]["additional-features"]["modes"]["tester"] = False
			#
			#if not "show-id" in guilds_config_data[str(guild.id)]["additional-features"].keys(): guilds_config_data[str(guild.id)]["additional-features"]["show-id"] = False
			#
			#if not "gateaway" in guilds_config_data[str(guild.id)].keys(): guilds_config_data[str(guild.id)]["gateaway"] = True

		with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "w") as write_file: json.dump(guilds_config_data, write_file, ensure_ascii = False, indent = 4)


	@commands.Cog.listener()
	async def on_guild_remove(self, guild):
		with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "r") as read_file: guilds_config_data = json.load(read_file)

		#guilds_config_data[str(guild.id)].pop("prefix")
		del guilds_config_data[str(guild.id)]["prefix"]
		#guilds_config_data[str(guild.id)].pop("language")
		del guilds_config_data[str(guild.id)]["language"]

		#guilds_config_data[str(guild.id)]["additional-features"][1]["modes"].remove("tester")
		del guilds_config_data[str(guild.id)]["additional-features"][1]["modes"][0]["tester"]
		#guilds_config_data[str(guild.id)]["additional-features"].remove("modes")
		del guilds_config_data[str(guild.id)]["additional-features"][1]["modes"]

		#guilds_config_data[str(guild.id)]["additional-features"].remove("show_id")
		del guilds_config_data[str(guild.id)]["additional-features"][2]["show_id"]

		del guilds_config_data[str(guild.id)]["additional-features"][2]
		del guilds_config_data[str(guild.id)]["additional-features"][1]

		with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "w") as write_file: json.dump(guilds_config_data, write_file, ensure_ascii = False, indent = 4)


	@commands.Cog.listener()
	async def on_ready(self):
		await self.bot.wait_until_ready()
		self.check_guilds_config.start()


async def setup(bot):
	await bot.add_cog(GuildsEvents(bot))