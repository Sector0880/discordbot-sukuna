# вроде ctx работает при interaction, поэтому импорта discord не было
import yaml
import json

# ✓
class Bot:
	def read_bot(self):
		with open("./.db/bot/bot.yml", "r", encoding="utf-8") as read_file: return yaml.safe_load(read_file)
	def get_bot_presence(self): return self.read_bot()["presence"]
bot_presence = Bot().get_bot_presence

class Multipresence:
	class Guilds:
		# config ✓
		# -----------------------------------------
		# imports ✓
		def read_guilds_config_yml(self):
			with open("./.db/multipresence/guilds/config.yml", "r", encoding="utf-8") as read_file: return yaml.safe_load(read_file)
		def read_guilds_config_json(self):
			with open("./.db/multipresence/guilds/config.json", "r", encoding="utf-8") as read_file: return json.load(read_file)
		
		# gets ✓
		def get_guild_prefix(self, ctx): 
			if str(ctx.guild.id) not in self.read_guilds_config_json().keys(): 
				return self.read_guilds_config_yml()["prefix"] 
			else:
				return self.read_guilds_config_json()[str(ctx.guild.id)]["prefix"] 
		def get_guild_language(self, ctx):
			if str(ctx.guild.id) not in self.read_guilds_config_json().keys():
				return self.read_guilds_config_yml()["language"]
			else:
				return self.read_guilds_config_json()[str(ctx.guild.id)]["language"]
		# -----------------------------------------
		
		# modules ✓
		# -----------------------------------------
		# imports ✓
		def read_guilds_modules_yml(self):
			with open("./.db/multipresence/guilds/modules.yml", "r", encoding="utf-8") as read_file: return yaml.safe_load(read_file)
		def read_guilds_modules_json(self):
			with open("./.db/multipresence/guilds/modules.json", "r", encoding="utf-8") as read_file: return json.load(read_file)
		
		# gets ✓
		def get_guild_module_moderation(self, ctx):
			if str(ctx.guild.id) not in self.read_guilds_modules_json().keys():
				return self.read_guilds_modules_yml()["moderation"]
			else:
				return self.read_guilds_modules_json()[str(ctx.guild.id)]["moderation"]
		def get_guild_module_audit(self, ctx):
			if str(ctx.guild.id) not in self.read_guilds_modules_json().keys():
				return self.read_guilds_modules_yml()["audit"]
			else:
				return self.read_guilds_modules_json()[str(ctx.guild.id)]["audit"]
		def get_guild_module_fun(self, ctx):
			if str(ctx.guild.id) not in self.read_guilds_modules_json().keys():
				return self.read_guilds_modules_yml()["fun"]
			else:
				return self.read_guilds_modules_json()[str(ctx.guild.id)]["fun"]
		def get_guild_module_profile(self, ctx):
			if str(ctx.guild.id) not in self.read_guilds_modules_json().keys():
				return self.read_guilds_modules_yml()["profile"]
			else:
				return self.read_guilds_modules_json()[str(ctx.guild.id)]["profile"]
		def get_guild_module_music(self, ctx):
			if str(ctx.guild.id) not in self.read_guilds_modules_json().keys():
				return self.read_guilds_modules_yml()["music"]
			else:
				return self.read_guilds_modules_json()[str(ctx.guild.id)]["music"]
		# -----------------------------------------

		# portal ✓
		# -----------------------------------------
		# imports ✓
		def read_guilds_portal_yml(self):
			with open("./.db/multipresence/guilds/portal.yml", "r", encoding="utf-8") as read_file: return yaml.safe_load(read_file)
		def read_guilds_portal_json(self):
			with open("./.db/multipresence/guilds/portal.json", "r", encoding="utf-8") as read_file: return json.load(read_file)
		
		# gets ✓
		def get_guild_presence(self, ctx):
			if str(ctx.guild.id) not in self.read_guilds_portal_json().keys():
				return self.read_guilds_portal_yml()["presence"]
			else:
				return self.read_guilds_portal_json()[str(ctx.guild.id)]["presence"]
		def get_guild_gateaway_open(self, ctx):
			if str(ctx.guild.id) not in self.read_guilds_portal_json().keys():
				return self.read_guilds_portal_yml()["gateaway"]["open"]
			else:
				return self.read_guilds_portal_json()[str(ctx.guild.id)]["gateaway"]["open"]
		# -----------------------------------------

		# premium ✓
		# -----------------------------------------
		# imports ✓
		def read_guilds_premium_yml(self):
			with open("./.db/multipresence/guilds/premium.yml", "r", encoding="utf-8") as read_file: return yaml.safe_load(read_file)
		def read_guilds_premium_json(self):
			with open("./.db/multipresence/guilds/premium.json", "r", encoding="utf-8") as read_file: return json.load(read_file)
		
		# gets ✓
		def get_guild_premium_work(self, ctx):
			if str(ctx.guild.id) not in self.read_guilds_premium_json().keys():
				return self.read_guilds_premium_yml()["premium"]["work"]
			else:
				return self.read_guilds_premium_json()[str(ctx.guild.id)]["premium"]["work"]
		# -----------------------------------------
guild_prefix = Multipresence().Guilds().get_guild_prefix
guild_language = Multipresence().Guilds().get_guild_language

guild_module_moderation = Multipresence().Guilds().get_guild_module_moderation
guild_module_audit = Multipresence().Guilds().get_guild_module_audit
guild_module_fun = Multipresence().Guilds().get_guild_module_fun
guild_module_profile = Multipresence().Guilds().get_guild_module_profile
guild_module_music = Multipresence().Guilds().get_guild_module_music

guild_presence = Multipresence().Guilds().get_guild_presence
guild_gateaway_open = Multipresence().Guilds().get_guild_gateaway_open

guild_premium_work = Multipresence().Guilds().get_guild_premium_work


class Staff:
	def read_staff(self):
		with open("./.db/staff/staff.yml", "r", encoding="utf-8") as read_file: return yaml.safe_load(read_file)
	def get_staff_creator_name(self): return self.read_staff()["creator"]["name"]
	def get_staff_creator_id1(self): return self.read_staff()["creator"]["id1"]
	def get_staff_creator_id2(self): return self.read_staff()["creator"]["id2"]

	def get_staff_administrators_admin1_name(self): return self.read_staff()["administrators"]["admin1"]["name"]
	def get_staff_administrators_admin1_id(self): return self.read_staff()["administrators"]["admin1"]["id"]

	def get_staff_stafflist_admins(self): return self.read_staff()["staffList_Admins"]
	def get_staff_stafflist_specialperms(self): return self.read_staff()["staffList_SpecialPerms"]
staff_creator_name = Staff().get_staff_creator_name
staff_creator_id1 = Staff().get_staff_creator_id1
staff_creator_id2 = Staff().get_staff_creator_id2

staff_administrators_admin1_name = Staff().get_staff_administrators_admin1_name
staff_administrators_admin1_id = Staff().get_staff_administrators_admin1_id

staff_stafflist_admins = Staff().get_staff_stafflist_admins
staff_stafflist_specialperms = Staff().get_staff_stafflist_specialperms