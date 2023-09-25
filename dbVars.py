# вроде ctx работает при interaction, поэтому импорта discord не было
import json
import yaml

class Bot:
	def db_bot_data(self):
		with open("./.db/bot/bot.yml", "r", encoding="utf-8") as read_file: return yaml.safe_load(read_file)
	def get_bot_presence(self): return self.db_bot_data()["presence"]
	def get_bot_tasks_loop_premium_check_premiumtime(self): return self.bot_config_data()["tasks.loop.premium_check_premiumtime"]
	def get_bot_tasks_loop_premium_change_premiumtimeremaining(self): return self.bot_config_data()["tasks.loop.premium_change_premiumtimeremaining"]
bot_presence = Bot().get_bot_presence
bot_tasks_loop_premium_check_premiumtime = Bot().get_bot_tasks_loop_premium_check_premiumtime
bot_tasks_loop_premium_change_premiumtimeremaining = Bot().get_bot_tasks_loop_premium_change_premiumtimeremaining

class Multipresence:
	class Guilds:
		def get_guild_config_yml(self):
			with open("./.db/multipresence/guilds/config.yml", "r", encoding="utf-8") as read_file: return yaml.safe_load(read_file)
		def get_guild_config_yml_prefix(self): return self.get_guild_config_yml()["prefix"]
		def get_guild_config_yml_language(self): return self.get_guild_config_yml()["language"]

		def get_guild_config_json(self):
			with open("./.db/multipresence/guilds/config.json", "r", encoding="utf-8") as read_file: return json.load(read_file)
		def get_guild_config_json_prefix(self, ctx): return self.get_guild_config_json()[str(ctx.guild.id)]["prefix"]
		def get_guild_config_json_language(self, ctx): return self.get_guild_config_json()[str(ctx.guild.id)]["language"]
guild_config_yml_prefix = Multipresence().Guilds().get_guild_config_yml_prefix
guild_config_yml_language = Multipresence().Guilds().get_guild_config_yml_language

guild_config_json_prefix = Multipresence().Guilds().get_guild_config_json_prefix
guild_config_json_language = Multipresence().Guilds().get_guild_config_json_language