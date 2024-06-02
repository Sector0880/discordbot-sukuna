# вроде ctx работает при interaction, поэтому импорта discord не было
import yaml
import json

class Bot:
	def read_bot(self):
		with open("./.db/bot/bot.yml", "r", encoding="utf-8") as read_file: return yaml.safe_load(read_file)
	def get_bot_presence(self): return self.read_bot()["presence"]
bot_presence = Bot().get_bot_presence

class Multipresence:
	class Guilds:
		# config 
		# -----------------------------------------
		# imports 
		def read_guilds_config_yml(self):
			with open("./.db/multipresence/guilds/config.yml", "r", encoding="utf-8") as read_file: return yaml.safe_load(read_file)
		def read_guilds_config_json(self):
			with open("./.db/multipresence/guilds/config.json", "r", encoding="utf-8") as read_file: return json.load(read_file)
		
		# gets 
		def get_guild_prefix(self, ctx): 
			if str(ctx.guild.id) in self.read_guilds_config_json().keys() and "prefix" in self.read_guilds_config_json()[str(ctx.guild.id)]:
				return self.read_guilds_config_json()[str(ctx.guild.id)]["prefix"] 
			else:
				return self.read_guilds_config_yml()["prefix"]
		def get_guild_language(self, ctx):
			if str(ctx.guild.id) in self.read_guilds_config_json().keys() and "language" in self.read_guilds_config_json()[str(ctx.guild.id)]:
				return self.read_guilds_config_json()[str(ctx.guild.id)]["language"] 
			else:
				return self.read_guilds_config_yml()["language"]
		# -----------------------------------------
		
		# modules 
		# -----------------------------------------
		# imports 
		def read_guilds_modules_yml(self):
			with open("./.db/multipresence/guilds/modules.yml", "r", encoding="utf-8") as read_file: return yaml.safe_load(read_file)
		def read_guilds_modules_json(self):
			with open("./.db/multipresence/guilds/modules.json", "r", encoding="utf-8") as read_file: return json.load(read_file)
		
		# gets 
		def get_guild_module_moderation(self, ctx):
			if str(ctx.guild.id) in self.read_guilds_modules_json().keys() and "moderation" in self.read_guilds_modules_json()[str(ctx.guild.id)]:
				return self.read_guilds_modules_json()[str(ctx.guild.id)]["moderation"]
			else:
				return self.read_guilds_modules_yml()["moderation"]
		def get_guild_module_audit(self, ctx):
			if str(ctx.guild.id) in self.read_guilds_modules_json().keys() and "audit" in self.read_guilds_modules_json()[str(ctx.guild.id)]:
				return self.read_guilds_modules_json()[str(ctx.guild.id)]["audit"]
			else:
				return self.read_guilds_modules_yml()["audit"]
		def get_guild_module_fun(self, ctx):
			if str(ctx.guild.id) in self.read_guilds_modules_json().keys() and "fun" in self.read_guilds_modules_json()[str(ctx.guild.id)]:
				return self.read_guilds_modules_json()[str(ctx.guild.id)]["fun"]
			else:
				return self.read_guilds_modules_yml()["fun"]
		def get_guild_module_profile(self, ctx):
			if str(ctx.guild.id) in self.read_guilds_modules_json().keys() and "profile" in self.read_guilds_modules_json()[str(ctx.guild.id)]:
				return self.read_guilds_modules_json()[str(ctx.guild.id)]["profile"]
			else:
				return self.read_guilds_modules_yml()["profile"]
		def get_guild_module_music(self, ctx):
			if str(ctx.guild.id) in self.read_guilds_modules_json().keys() and "music" in self.read_guilds_modules_json()[str(ctx.guild.id)]:
				return self.read_guilds_modules_json()[str(ctx.guild.id)]["music"]
			else:
				return self.read_guilds_modules_yml()["music"]
		# -----------------------------------------

		# portal 
		# -----------------------------------------
		# imports 
		def read_guilds_portal_yml(self):
			with open("./.db/multipresence/guilds/portal.yml", "r", encoding="utf-8") as read_file: return yaml.safe_load(read_file)
		def read_guilds_portal_json(self):
			with open("./.db/multipresence/guilds/portal.json", "r", encoding="utf-8") as read_file: return json.load(read_file)
		
		# gets 
		def get_guild_presence(self, ctx):
			if str(ctx.guild.id) in self.read_guilds_portal_json().keys() and "presence" in self.read_guilds_portal_json()[str(ctx.guild.id)]:
				return self.read_guilds_portal_json()[str(ctx.guild.id)]["presence"]
			else:
				return self.read_guilds_portal_yml()["presence"]
		def get_guild_gateaway_open(self, ctx):
			if str(ctx.guild.id) in self.read_guilds_portal_json().keys() and "open" in self.read_guilds_portal_json()[str(ctx.guild.id)]["gateaway"]:
				return self.read_guilds_portal_json()[str(ctx.guild.id)]["gateaway"]["open"]
			else:
				return self.read_guilds_portal_yml()["gateaway"]["open"]
		# -----------------------------------------

		# premium 
		# -----------------------------------------
		# imports 
		def read_guilds_premium_yml(self):
			with open("./.db/multipresence/guilds/premium.yml", "r", encoding="utf-8") as read_file: return yaml.safe_load(read_file)
		def read_guilds_premium_json(self):
			with open("./.db/multipresence/guilds/premium.json", "r", encoding="utf-8") as read_file: return json.load(read_file)
		
		# gets 
		def get_guild_premium_work(self, ctx):
			if str(ctx.guild.id) in self.read_guilds_premium_json().keys() and "open" in self.read_guilds_premium_json()[str(ctx.guild.id)]["premium"]:
				return self.read_guilds_premium_json()[str(ctx.guild.id)]["premium"]["work"]
			else:
				return self.read_guilds_premium_yml()["premium"]["work"]
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








# старое
def cspl_item_old(ctx, param, item):
	allowed = {
		'guilds': [
			'cluster',
			'gateaway-status',
			'prefix',
			'language',
			'modules', 'moderation', 'profile', 'fun', 'audit', 'music',
			'premium-status'
		],
		'users': [
			'cluster',
			'mute-status'
		]
	}
	path = {
		'guilds': {
			'cluster': ['cluster'],
			'gateaway-status': ['gateaway', 'status'],
			'prefix': ['prefix'],
			'language': ['language'],
			'modules': ['modules'],
			'moderation': ['modules', 'moderation'],
			'profile': ['modules', 'profile'],
			'fun': ['modules', 'fun'],
			'audit': ['modules', 'audit'],
			'music': ['modules', 'music'],
			'premium-status': ['premium', 'status']
		},
		'users': {
			'cluster': ['cluster'],
			'mute-status': ['mute', 'status']
		}
	}

	# ошибки (работают)
	if param not in list(allowed.keys()):
		valid_allowed = "\n".join(list(allowed.keys()))
		raise ValueError(f'Недопустимое значение для аргумента param. Допустимые значения:```\n{valid_allowed}```')
	if item not in allowed[param]:
		valid_item = "\n".join(allowed[param])
		raise ValueError(f'Недопустимое значение для аргумента item. Допустимые значения:```\n{valid_item}```')

	if param == 'guilds': param_id = str(ctx.guild.id)
	else: param_id = str(ctx.author.id)

	with open(f'./.db/crossplatform/custom/clusters-{param}.json', 'r', encoding='utf-8') as read_file:
		clusters_param = json.load(read_file)

	# проблема users в том что если нету id автора команды в clusters-users.json то выводит ошибку 400 Bad Request (error code: 50006): Cannot send an empty message
	for key, value in clusters_param.items():
		if param_id in value[param]:
			guild_cluster = key
			with open(f'./.db/crossplatform/custom/clusters/{guild_cluster}/{param}.json', 'r', encoding='utf-8') as read_file:
				cluster_param = json.load(read_file)

			if param_id in cluster_param:
				result = cluster_param[param_id]
				for p in path[param][item]:
					result = result.get(p)
					if result is None:
						# Если значения в пути отсутствуют, используем данные из yml
						param_yaml = yaml.safe_load(open(f'./.db/crossplatform/initial/{param}.yml', 'r', encoding='utf-8'))
						for p in path[param][item]:
							param_yaml = param_yaml.get(p)
						return param_yaml
				return result
			else:
				param_yaml = yaml.safe_load(open(f'./.db/crossplatform/initial/{param}.yml', 'r', encoding='utf-8'))
				for p in path[param][item]:
					param_yaml = param_yaml.get(p)
				return param_yaml
		else:
			# Если значения в пути отсутствуют, используем данные из yml
			param_yaml = yaml.safe_load(open(f'./.db/crossplatform/initial/{param}.yml', 'r', encoding='utf-8'))
			for p in path[param][item]:
				param_yaml = param_yaml.get(p)
			return param_yaml
	
	print("чтото пошло не так")