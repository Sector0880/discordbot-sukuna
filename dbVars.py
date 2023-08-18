import json
import yaml


class Bot:
	def bot_config_data(self):
		with open("./botConfiguration/.db/bot/botConfiguration/botConfig.yml", "r", encoding="utf-8") as read_file: return yaml.safe_load(read_file)
	
	def get_bot_activity(self): return self.bot_config_data()["presence"]["activity"]
	def get_bot_message_output_delete_after(self): return self.bot_config_data()["message-output"]["delete_after"]

bot_activity = Bot().get_bot_activity
bot_delete_after = Bot().get_bot_message_output_delete_after


class Guild:
	def guilds_config_data(self):
		with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "r", encoding="utf-8") as read_file: return json.load(read_file)

	def get_guild_name(self, ctx): return self.guilds_config_data()[str(ctx.guild.id)]["overview"]["guild_name"]
	def get_owner_id(self, ctx): return self.guilds_config_data()[str(ctx.guild.id)]["overview"]["owner-id"]

	def get_guild_prefix(self, ctx): return self.guilds_config_data()[str(ctx.guild.id)]["prefix"]
	def get_guild_language(self, ctx): return self.guilds_config_data()[str(ctx.guild.id)]["language"]
	
	def get_guild_premium(self, ctx): return self.guilds_config_data()[str(ctx.guild.id)]["additional-features"]["privileges"][0]["premium"]
	def get_guild_premium_uuid(self, ctx): return self.guilds_config_data()[str(ctx.guild.id)]["additional-features"]["privileges"][0]["premium-uuid"]
	def get_guild_premium_time_start(self, ctx): return self.guilds_config_data()[str(ctx.guild.id)]["additional-features"]["privileges"][0]["premium-time-start"]
	def get_guild_premium_time_set(self, ctx): return self.guilds_config_data()[str(ctx.guild.id)]["additional-features"]["privileges"][0]["premium-time-set"]
	def get_guild_premium_time_extra(self, ctx): return self.guilds_config_data()[str(ctx.guild.id)]["additional-features"]["privileges"][0]["premium-time-extra"]
	def get_guild_premium_time_extra_history(self, ctx): return self.guilds_config_data()[str(ctx.guild.id)]["additional-features"]["privileges"][0]["premium-time-extra-history"]
	def get_guild_premium_time_extra_count(self, ctx): return self.guilds_config_data()[str(ctx.guild.id)]["additional-features"]["privileges"][0]["premium-time-extra-count"]
	def get_guild_premium_time_end(self, ctx): return self.guilds_config_data()[str(ctx.guild.id)]["additional-features"]["privileges"][0]["premium-time-end"]
	def get_guild_premium_time_remaining(self, ctx): return self.guilds_config_data()[str(ctx.guild.id)]["additional-features"]["privileges"][0]["premium-time-remaining"]
	
	def get_guild_show_id(self, ctx): return self.guilds_config_data()[str(ctx.guild.id)]["additional-features"]["show_id"]

	def get_guild_bot_output(self, ctx): return self.guilds_config_data()[str(ctx.guild.id)]["protection"]["gateaway"]["bot_output"]

guild_owner_id = Guild().get_owner_id

guild_name = Guild().get_guild_name
guild_prefix = Guild().get_guild_prefix
guild_language = Guild().get_guild_language

guild_premium = Guild().get_guild_premium
guild_premium_uuid = Guild().get_guild_premium_uuid
guild_premium_time_start = Guild().get_guild_premium_time_start
guild_premium_time_set = Guild().get_guild_premium_time_set
guild_premium_time_extra = Guild().get_guild_premium_time_extra
guild_premium_time_extra_history = Guild().get_guild_premium_time_extra_history
guild_premium_time_extra_count = Guild().get_guild_premium_time_extra_count
guild_premium_time_end = Guild().get_guild_premium_time_end
guild_premium_time_remaining = Guild().get_guild_premium_time_remaining

guild_show_id = Guild().get_guild_show_id

guild_bot_output = Guild().get_guild_bot_output


class Staff:
	def staff_config_data(self):
		with open("./botConfiguration/.db/staff/list/staff.yml", "r", encoding="utf-8") as read_file: return yaml.safe_load(read_file)

	def get_staff_creator_id(self): return self.staff_config_data()["creator"]["id"]
	def get_staff_ada_id(self): return self.staff_config_data()["administrators"]["admin1"]["id"]
	def get_staff_staffList_SpecialPerms(self): return self.staff_config_data()["staffList_SpecialPerms"]

staff_creator_id = Staff().get_staff_creator_id
staff_ada_id = Staff().get_staff_ada_id
staff_staffList_SpecialPerms = Staff().get_staff_staffList_SpecialPerms


class Doc:
	class Errors:
		class Terminal:
			def get_error_terminal_command_error(self):
				with open("./botConfiguration/.db/doc/errors/terminal/terminalCommandError.yml", encoding="utf-8") as read_file: return yaml.safe_load(read_file)
			def get_error_terminal_traceback_error(self):
				with open("./botConfiguration/.db/doc/errors/terminal/terminalTracebackError.yml", encoding="utf-8") as read_file: return yaml.safe_load(read_file)

		def get_error_command_not_found(self):
			with open("./botConfiguration/.db/doc/errors/commandNotFound.yml", encoding="utf-8") as read_file: return yaml.safe_load(read_file)
		def get_error_server_blocked(self):
			with open("./botConfiguration/.db/doc/errors/serverBlocked.yml", encoding="utf-8") as read_file: return yaml.safe_load(read_file)
		def get_error_invalid_language(self):
			with open("./botConfiguration/.db/doc/errors/invalidLanguage.yml", encoding="utf-8") as read_file: return yaml.safe_load(read_file)

error_terminal_command_error = Doc().Errors().Terminal().get_error_terminal_command_error
error_terminal_traceback_error = Doc().Errors().Terminal().get_error_terminal_traceback_error

error_command_not_found = Doc().Errors().get_error_command_not_found
error_server_blocked = Doc().Errors().get_error_server_blocked
error_invalid_language = Doc().Errors().get_error_invalid_language


files_status_txt = open("./botConfiguration/.db/files_status.txt", encoding="utf-8")