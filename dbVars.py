import json
import yaml


class Bot:
	def bot_config_data(self):
		with open("./botConfiguration/.db/bot/botConfiguration/botConfig.yml", "r", encoding="utf-8") as read_file: return yaml.safe_load(read_file)
	
	def get_bot_presence(self): return self.bot_config_data()["presence"]["title"]


	def bot_switches_data(self):
		with open("./botConfiguration/.db/bot/botConfiguration/botSwitches.yml", "r", encoding="utf-8") as read_file: return yaml.safe_load(read_file)
	
	def get_bot_switches_testers_work_commands_mention(self): return self.bot_switches_data()["work_commands"]["mention"]
	def get_bot_switches_testers_work_commands_db_info(self): return self.bot_switches_data()["work_commands"]["db_info"]
	def get_bot_switches_testers_work_commands_update_check(self): return self.bot_switches_data()["work_commands"]["update_check"]

	def get_bot_switches_output_correct(self): return self.bot_switches_data()["special-functions"]["commands"]["output"]["correct"]
	def get_bot_switches_output_partial_sleep(self): return self.bot_switches_data()["special-functions"]["commands"]["output"]["partial-sleep"]
	def get_bot_switches_output_emoji(self): return self.bot_switches_data()["special-functions"]["commands"]["output"]["emoji"]

	def get_bot_switches_message_output_delete_after(self): return self.bot_switches_data()["special-functions"]["message-output"]["delete_after"]

	def get_bot_switches_updates_mention_embs_stopwatch(self): return self.bot_switches_data()["updates"]["mention"]["embs"]["stopwatch"]
	def get_bot_switches_updates_mention_embs_check(self): return self.bot_switches_data()["updates"]["mention"]["embs"]["check"]

bot_presence = Bot().get_bot_presence

bot_switches_testers_work_commands_mention = Bot().get_bot_switches_testers_work_commands_mention
bot_switches_testers_work_commands_db_info = Bot().get_bot_switches_testers_work_commands_db_info
bot_switches_testers_work_commands_update_check = Bot().get_bot_switches_testers_work_commands_update_check

bot_switches_output_correct = Bot().get_bot_switches_output_correct
bot_switches_output_partial_sleep = Bot().get_bot_switches_output_partial_sleep
bot_switches_output_emoji = Bot().get_bot_switches_output_emoji

bot_switches_message_output_delete_after = Bot().get_bot_switches_message_output_delete_after

bot_switches_updates_mention_embs_stopwatch = Bot().get_bot_switches_updates_mention_embs_stopwatch
bot_switches_updates_mention_embs_check = Bot().get_bot_switches_updates_mention_embs_check


class Guild:
	def guilds_config_data(self):
		with open("./botConfiguration/.db/guildsConfiguration/guildsConfig.json", "r", encoding="utf-8") as read_file: return json.load(read_file)

	def get_guild_name(self, ctx): return self.guilds_config_data()[str(ctx.guild.id)]["overview"]["guild_name"]
	def get_guild_prefix(self, ctx): return self.guilds_config_data()[str(ctx.guild.id)]["prefix"]
	def get_guild_language(self, ctx): return self.guilds_config_data()[str(ctx.guild.id)]["language"]
	
	def get_guild_premium(self, ctx): return self.guilds_config_data()[str(ctx.guild.id)]["additional-features"][0]["privileges"][0]["premium"]
	def get_guild_show_id(self, ctx): return self.guilds_config_data()[str(ctx.guild.id)]["additional-features"][2]["show_id"]
	def get_guild_tester(self, ctx): return self.guilds_config_data()[str(ctx.guild.id)]["additional-features"][1]["modes"][0]["tester"]

	def get_guild_bot_output(self, ctx): return self.guilds_config_data()[str(ctx.guild.id)]["protection"][0]["gateaway"]["bot_output"]

guild_name = Guild().get_guild_name
guild_prefix = Guild().get_guild_prefix
guild_language = Guild().get_guild_language

guild_premium = Guild().get_guild_premium
guild_show_id = Guild().get_guild_show_id
guild_tester = Guild().get_guild_tester

guild_bot_output = Guild().get_guild_bot_output


class Staff:
	def staff_config_data(self):
		with open("./botConfiguration/.db/staff/list/staffList.yml", "r", encoding="utf-8") as read_file: return yaml.safe_load(read_file)

	def get_staff_owner_id(self): return self.staff_config_data()["owner"]["id"]

	def get_staff_testers_main_testers(self): return self.staff_config_data()["testers"]["main-testers"]["testers-list"]

	def get_staff_testers_divided_testers_for_commands_mention(self): return self.staff_config_data()["testers"]["divided-testers"]["for_commands"]["mention"]["testers-list"]

	def get_staff_testers_divided_testers_for_commands_db_info(self): return self.staff_config_data()["testers"]["divided-testers"]["for_commands"]["db_info"]["testers-list"]
	def get_staff_testers_divided_testers_for_commands_update_check(self): return self.staff_config_data()["testers"]["divided-testers"]["for_commands"]["update_check"]["testers-list"]

staff_owner_id = Staff().get_staff_owner_id

staff_testers_main_testers = Staff().get_staff_testers_main_testers

staff_testers_divided_testers_for_commands_mention = Staff().get_staff_testers_divided_testers_for_commands_mention
staff_testers_divided_testers_for_commands_db_info = Staff().get_staff_testers_divided_testers_for_commands_db_info
staff_testers_divided_testers_for_commands_update_check = Staff().get_staff_testers_divided_testers_for_commands_update_check


class Doc:
	class Errors:
		class CommandBlocked:
			def get_error_command_offed(self):
				with open("./botConfiguration/.db/doc/errors/commandBlocked/commandOffed.yml", encoding="utf-8") as read_file: return yaml.safe_load(read_file)
			def get_error_command_testing(self):
				with open("./botConfiguration/.db/doc/errors/commandBlocked/commandTesting.yml", encoding="utf-8") as read_file: return yaml.safe_load(read_file)
		
		class Terminal:
			def get_error_terminal_command_error(self):
				with open("./botConfiguration/.db/doc/errors/terminal/terminalCommandError.yml", encoding="utf-8") as read_file: return yaml.safe_load(read_file)
			def get_error_terminal_traceback_error(self):
				with open("./botConfiguration/.db/doc/errors/terminal/terminalTracebackError.yml", encoding="utf-8") as read_file: return yaml.safe_load(read_file)

		def get_error_switch_false_command_offed(self):
			with open("./botConfiguration/.db/doc/errors/commandBlocked/commandOffed.yml", encoding="utf-8") as read_file: return yaml.safe_load(read_file)

		def get_error_switch_false_command_testing(self):
			with open("./botConfiguration/.db/doc/errors/commandBlocked/commandTesting.yml", encoding="utf-8") as read_file: return yaml.safe_load(read_file)

		def get_error_command_not_found(self):
			with open("./botConfiguration/.db/doc/errors/commandNotFound.yml", encoding="utf-8") as read_file: return yaml.safe_load(read_file)
		def get_error_server_blocked(self):
			with open("./botConfiguration/.db/doc/errors/serverBlocked.yml", encoding="utf-8") as read_file: return yaml.safe_load(read_file)
		def get_error_invalid_language(self):
			with open("./botConfiguration/.db/doc/errors/invalidLanguage.yml", encoding="utf-8") as read_file: return yaml.safe_load(read_file)

error_command_offed = Doc().Errors().CommandBlocked().get_error_command_offed
error_command_testing = Doc().Errors().CommandBlocked().get_error_command_testing

error_terminal_command_error = Doc().Errors().Terminal().get_error_terminal_command_error
error_terminal_traceback_error = Doc().Errors().Terminal().get_error_terminal_traceback_error

error_switch_false_command_offed = Doc().Errors().get_error_switch_false_command_offed

error_switch_false_command_testing = Doc().Errors().get_error_switch_false_command_testing

error_command_not_found = Doc().Errors().get_error_command_not_found
error_server_blocked = Doc().Errors().get_error_server_blocked
error_invalid_language = Doc().Errors().get_error_invalid_language