import json
import yaml
import discord

bot_presence = lambda: yaml.safe_load(open('./.db/bot/bot.yml', 'r', encoding='utf-8'))['presence']

sf_c = lambda: yaml.safe_load(open('./.db/staff.yml', 'r', encoding='utf-8'))['staffList_Creators']
sf_a = lambda: yaml.safe_load(open('./.db/staff.yml', 'r', encoding='utf-8'))['staffList_Admins']
sf_sp = lambda: yaml.safe_load(open('./.db/staff.yml', 'r', encoding='utf-8'))['staffList_SpecialPerms']

cspl_initial_guilds = lambda: yaml.safe_load(open('./.db/crossplatform/initial/guilds.yml', 'r', encoding='utf-8'))
cspl_initial_users = lambda: yaml.safe_load(open('./.db/crossplatform/initial/users.yml', 'r', encoding='utf-8'))

cspl_custom_guilds = lambda interaction: json.load(open("./.db/crossplatform/custom/guilds.json", "r", encoding="utf-8"))
cspl_custom_users = lambda interaction: json.load(open("./.db/crossplatform/custom/users.json", "r", encoding="utf-8"))

# берет объект из базы данных, если в json он существует то он берет именно его из json
def cspl_get_param(interaction, branch: str, param: str, path: list = None, user: discord.Member = None, guild = None):
	try:
		if path: path_len = len(path)
		else: path_len = 0

		if guild:
			guild_id = guild
		else: 
			guild_id = interaction.guild.id
		
		match branch:
			case 'g':
				if path and path_len == 4:
					if (
						guild_id in cspl_custom_guilds(interaction)
						and path[0] in cspl_custom_guilds(interaction)[guild_id]
						and path[1] in cspl_custom_guilds(interaction)[guild_id][path[0]]
						and path[2] in cspl_custom_guilds(interaction)[guild_id][path[0]][path[1]]
						and path[3] in cspl_custom_guilds(interaction)[guild_id][path[0]][path[1]][path[2]]
						and param in cspl_custom_guilds(interaction)[guild_id][path[0]][path[1]][path[2]][path[3]]
					):
						return cspl_custom_guilds(interaction)[guild_id][path[0]][path[1]][path[2]][path[3]][param]
					else:
						return cspl_initial_guilds()[path[0]][path[1]][path[2]][path[3]][param]
				if path and path_len == 3:
					if (
						guild_id in cspl_custom_guilds(interaction)
						and path[0] in cspl_custom_guilds(interaction)[guild_id]
						and path[1] in cspl_custom_guilds(interaction)[guild_id][path[0]]
						and path[2] in cspl_custom_guilds(interaction)[guild_id][path[0]][path[1]]
						and param in cspl_custom_guilds(interaction)[guild_id][path[0]][path[1]][path[2]]
					):
						return cspl_custom_guilds(interaction)[guild_id][path[0]][path[1]][path[2]][param]
					else:
						return cspl_initial_guilds()[path[0]][path[1]][path[2]][param]
				if path and path_len == 2:
					if (
						guild_id in cspl_custom_guilds(interaction)
						and path[0] in cspl_custom_guilds(interaction)[guild_id]
						and path[1] in cspl_custom_guilds(interaction)[guild_id][path[0]]
						and param in cspl_custom_guilds(interaction)[guild_id][path[0]][path[1]]
					):
						return cspl_custom_guilds(interaction)[guild_id][path[0]][path[1]][param]
					else:
						return cspl_initial_guilds()[path[0]][path[1]][param]
				elif path and path_len == 1:
					if (
						guild_id in cspl_custom_guilds(interaction)
						and path[0] in cspl_custom_guilds(interaction)[guild_id]
						and param in cspl_custom_guilds(interaction)[guild_id][path[0]]
					):
						return cspl_custom_guilds(interaction)[guild_id][path[0]][param]
					else:
						return cspl_initial_guilds()[path[0]][param]
				else:
					if (
						guild_id in cspl_custom_guilds(interaction)
						and param in cspl_custom_guilds(interaction)[guild_id]
					):
						return cspl_custom_guilds(interaction)[guild_id][param]
					else:
						return cspl_initial_guilds()[param]
			case 'u':
				if user:
					user_id = user.id
				else:
					if type(interaction) == discord.Interaction:
						user_id = interaction.user.id
					else:
						user_id = interaction.author.id
				
				if path and path_len == 2:
					if (
						user_id in cspl_custom_users(interaction)
						and guild_id in cspl_custom_users(interaction)[user_id]
						and path[0] in cspl_custom_users(interaction)[user_id][guild_id]
						and path[1] in cspl_custom_users(interaction)[user_id][guild_id][path[0]]
						and param in cspl_custom_users(interaction)[user_id][guild_id][path[0]][path[1]]
					):
						return cspl_custom_users(interaction)[user_id][guild_id][path[0]][path[1]][param]
					else:
						return cspl_initial_users()[path[0]][path[1]][param]
				elif path and path_len == 1:
					if (
						user_id in cspl_custom_users(interaction)
						and guild_id in cspl_custom_users(interaction)[user_id]
						and path[0] in cspl_custom_users(interaction)[user_id][guild_id]
						and param in cspl_custom_users(interaction)[user_id][guild_id][path[0]]
					):
						return cspl_custom_users(interaction)[user_id][guild_id][path[0]][param]
					else:
						return cspl_initial_users()[path[0]][param]
				else:
					if (
						user_id in cspl_custom_users(interaction)
						and guild_id in cspl_custom_users(interaction)[user_id]
						and param in cspl_custom_users(interaction)[user_id][guild_id]
					):
						return cspl_custom_users(interaction)[user_id][guild_id][param]
					else:
						return cspl_initial_users()[param]
	except Exception as e:
		print(f'Ошибка cspl_get_param: {repr(e)}')

def merge_data(default_data, custom_data):
	if isinstance(default_data, dict) and isinstance(custom_data, dict):
		merged = default_data.copy()
		for key, value in custom_data.items():
			if key in default_data:
				merged[key] = merge_data(default_data[key], value)
			else:
				merged[key] = value
		return merged
	elif isinstance(default_data, list) and isinstance(custom_data, list):
		# Assuming lists are merged by adding custom_data items to the default_data list
		merged = default_data.copy()
		for item in custom_data:
			if item not in merged:
				merged.append(item)
		return merged
	return custom_data

# берет объект из базы данных, но складывает json и yaml, таким образом yaml и json сливаются вместе, и измененные параметры
# в json заменяются в выдаваемом объекте
def cspl_get_param_with_merge(interaction: discord.Interaction, branch, param, path=None, user: discord.Member = None, guild = None):
	if path:
		path_len = len(path)
	else:
		path_len = 0

	match branch:
		case 'g':
			initial_data = cspl_initial_guilds()
			custom_data = cspl_custom_guilds(interaction).get(str(interaction.guild.id if not guild else guild), {})
			merged_data = merge_data(initial_data, custom_data)

			if path_len == 2:
				return merged_data[path[0]][path[1]].get(param)
			elif path_len == 1:
				return merged_data[path[0]].get(param)
			else:
				return merged_data.get(param)

		case 'u':
			initial_data = cspl_initial_users()
			custom_data = cspl_custom_users(interaction).get(str(user.id), {}).get(str(interaction.guild.id if not guild else guild), {})
			merged_data = merge_data(initial_data, custom_data)

			if path_len == 2:
				return merged_data[path[0]][path[1]].get(param)
			elif path_len == 1:
				return merged_data[path[0]].get(param)
			else:
				return merged_data.get(param)


"""
from supabase import create_client, Client

supabase_url = 'https://arsyftsiyroyjcaohmqn.supabase.co'
supabase_api = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFyc3lmdHNpeXJveWpjYW9obXFuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjEyOTg3MjcsImV4cCI6MjAzNjg3NDcyN30.hDJM2M76MrefU0Lc1vAphSa5uVMcPVylw1phEiqsPO4'
supabase: Client = create_client(supabase_url, supabase_api)

def supabase_get_data(table_name: str, select: str, eq: list = None):
	response = supabase.table(table_name).select(select)
	
	if eq:
		for column, value in eq:
			response = response.eq(column, value)
	
	try:
		response = response.execute()
		return response.data
	except Exception as e:
		print(repr(e))
def supabase_insert_data(table_name: str, insert: dict):
	response = supabase.table(table_name).insert(insert)
	try:
		response = response.execute()
		return response.data
	except Exception as e:
		print(repr(e))
def supabase_update_data(table_name: str, update: dict, eq: list = None):
	response = supabase.table(table_name).update(update)

	if eq:
		for column, value in eq:
			response = response.eq(column, value)
	
	try:
		response = response.execute()
		return response.data
	except Exception as e:
		print(repr(e))


bot_presence = lambda: supabase_get_data('bot', 'presence')[0]['presence']

# переделать на supabase_get_data
sf_c = lambda: yaml.safe_load(open('./.db/staff.yml', 'r', encoding='utf-8'))['staffList_Creators']
sf_a = lambda: yaml.safe_load(open('./.db/staff.yml', 'r', encoding='utf-8'))['staffList_Admins']
sf_sp = lambda: yaml.safe_load(open('./.db/staff.yml', 'r', encoding='utf-8'))['staffList_SpecialPerms']

cspl_initial_guilds = lambda: supabase_get_data('crossplatform_initial_guilds', '*')[0]
cspl_initial_users = lambda: supabase_get_data('crossplatform_initial_users', '*')[0]

cspl_custom_guilds = lambda interaction: supabase_get_data('crossplatform_custom_guilds', '*')
cspl_custom_users = lambda interaction: supabase_get_data('crossplatform_custom_users', '*')

def get_single_user(user_id, guild_id):
	single_user = supabase_get_data('crossplatform_custom_users', '*', [('user_id', user_id), ('guild_id', guild_id)])
	if single_user: return single_user[0]
	else: return dict(single_user)
		
def get_single_guild(guild_id):
	single_guild = supabase_get_data('crossplatform_custom_guilds', '*', [('guild_id', guild_id)])
	if single_guild: return single_guild[0]
	else: return dict(single_guild)

	single_user = supabase_get_data('crossplatform_custom_users', '*', [('user_id', user_id), ('guild_id', guild_id)])
	if single_user: single_user = single_user[0]
	else: single_user = {}

	single_guild = supabase_get_data('crossplatform_custom_guilds', '*', [('guild_id', guild_id)])
	if single_guild: single_guild = single_guild[0]
	else: single_guild = {}

	single_user = get_single_user(user_id, guild_id)

	single_guild = get_single_guild(guild_id)
"""

"""
					if (single_guild 
					and path[0] in single_guild
					and path[1] in single_guild[path[0]]
					and path[2] in single_guild[path[0]][path[1]]
					and path[3] in single_guild[path[0]][path[1]][path[2]]
					and param in single_guild[path[0]][path[1]][path[2]][path[3]]
					):
						return single_guild[path[0]][path[1]][path[2]][path[3]][param]
					else:
						return supabase_get_data('crossplatform_initial_guilds', '*')[0][path[0]][path[1]][path[2]][path[3]][param]
					"""

"""
					if (single_user
					and path[0] in single_user
					and path[1] in single_user[path[0]]
					and param in single_user[path[0]][path[1]]
					):
						return single_user[path[0]][path[1]][param]
					else:
						return supabase_get_data('crossplatform_initial_users', '*')[0][path[0]][path[1]][param]
					"""



"""
	if path:
		path_len = len(path)
	else:
		path_len = 0
	
	if guild:
		guild_id = str(guild)
	else: 
		guild_id = str(interaction.guild.id)
	
	if user:
		user_id = user.id
	else:
		if isinstance(interaction, discord.Interaction):
			user_id = interaction.user.id
		else:
			user_id = interaction.author.id

	match branch:
		case 'g':
			initial_data = cspl_initial_guilds()
			custom_data = single_guild.get('guild_id', {})
			merged_data = merge_data(initial_data, custom_data)

			if path_len == 2:
				return merged_data[path[0]][path[1]].get(param)
			elif path_len == 1:
				return merged_data[path[0]].get(param)
			else:
				return merged_data.get(param)

		case 'u':
			initial_data = cspl_initial_users()
			custom_data = single_user.get('user_id', {})
			merged_data = merge_data(initial_data, custom_data)

			if path_len == 2:
				return merged_data[path[0]][path[1]].get(param)
			elif path_len == 1:
				return merged_data[path[0]].get(param)
			else:
				return merged_data.get(param)
	"""