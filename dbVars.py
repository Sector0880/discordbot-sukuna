import json
import yaml
import discord
from discord import app_commands

bot_presence = lambda: yaml.safe_load(open('./.db/bot/bot.yml', 'r', encoding='utf-8'))['presence']
sf_c = lambda: yaml.safe_load(open('./.db/staff.yml', 'r', encoding='utf-8'))['staffList_Creators']
sf_a = lambda: yaml.safe_load(open('./.db/staff.yml', 'r', encoding='utf-8'))['staffList_Admins']
sf_sp = lambda: yaml.safe_load(open('./.db/staff.yml', 'r', encoding='utf-8'))['staffList_SpecialPerms']

cspl_initial_guilds = lambda: yaml.safe_load(open('./.db/crossplatform/initial/guilds.yml', 'r', encoding='utf-8'))
cspl_initial_users = lambda: yaml.safe_load(open('./.db/crossplatform/initial/users.yml', 'r', encoding='utf-8'))

cspl_custom_guilds = lambda interaction: json.load(open("./.db/crossplatform/custom/guilds.json", "r", encoding="utf-8"))
cspl_custom_users = lambda interaction: json.load(open("./.db/crossplatform/custom/users.json", "r", encoding="utf-8"))

# берет объект из базы данных, если в json он существует то он берет именно его из json
def cspl_get_param(interaction, branch, param, path = None, user: discord.Member = None, guild = None):
	if path: path_len = len(path)
	else: path_len = 0

	if guild:
		guild_id = str(guild)
	else: 
		guild_id = str(interaction.guild.id)

	match branch:
		case 'g':
			if path and path_len == 4:
				if guild_id in cspl_custom_guilds(interaction).keys() and path[0] in cspl_custom_guilds(interaction)[guild_id].keys() and path[1] in cspl_custom_guilds(interaction)[guild_id][path[0]].keys() and path[2] in cspl_custom_guilds(interaction)[guild_id][path[0]][path[1]].keys() and path[3] in cspl_custom_guilds(interaction)[guild_id][path[0]][path[1]][path[2]].keys() and param in cspl_custom_guilds(interaction)[guild_id][path[0]][path[1]][path[2]][path[3]].keys():
					return json.load(open("./.db/crossplatform/custom/guilds.json", "r", encoding="utf-8"))[guild_id][path[0]][path[1]][path[2]][path[3]][param]
				else:
					return yaml.safe_load(open('./.db/crossplatform/initial/guilds.yml', 'r', encoding='utf-8'))[path[0]][path[1]][path[2]][path[3]][param]
			if path and path_len == 3:
				if guild_id in cspl_custom_guilds(interaction).keys() and path[0] in cspl_custom_guilds(interaction)[guild_id].keys() and path[1] in cspl_custom_guilds(interaction)[guild_id][path[0]].keys() and path[2] in cspl_custom_guilds(interaction)[guild_id][path[0]][path[1]].keys() and param in cspl_custom_guilds(interaction)[guild_id][path[0]][path[1]][path[2]].keys():
					return json.load(open("./.db/crossplatform/custom/guilds.json", "r", encoding="utf-8"))[guild_id][path[0]][path[1]][path[2]][param]
				else:
					return yaml.safe_load(open('./.db/crossplatform/initial/guilds.yml', 'r', encoding='utf-8'))[path[0]][path[1]][path[2]][param]
			if path and path_len == 2:
				if guild_id in cspl_custom_guilds(interaction).keys() and path[0] in cspl_custom_guilds(interaction)[guild_id].keys() and path[1] in cspl_custom_guilds(interaction)[guild_id][path[0]].keys() and param in cspl_custom_guilds(interaction)[guild_id][path[0]][path[1]].keys():
					return json.load(open("./.db/crossplatform/custom/guilds.json", "r", encoding="utf-8"))[guild_id][path[0]][path[1]][param]
				else:
					return yaml.safe_load(open('./.db/crossplatform/initial/guilds.yml', 'r', encoding='utf-8'))[path[0]][path[1]][param]
			elif path and path_len == 1:
				if guild_id in cspl_custom_guilds(interaction).keys() and path[0] in cspl_custom_guilds(interaction)[guild_id].keys() and param in cspl_custom_guilds(interaction)[guild_id][path[0]].keys():
					return json.load(open("./.db/crossplatform/custom/guilds.json", "r", encoding="utf-8"))[guild_id][path[0]][param]
				else:
					return yaml.safe_load(open('./.db/crossplatform/initial/guilds.yml', 'r', encoding='utf-8'))[path[0]][param]
			else:
				if guild_id in cspl_custom_guilds(interaction).keys() and param in cspl_custom_guilds(interaction)[guild_id].keys():
					return json.load(open("./.db/crossplatform/custom/guilds.json", "r", encoding="utf-8"))[guild_id][param]
				else:
					return yaml.safe_load(open('./.db/crossplatform/initial/guilds.yml', 'r', encoding='utf-8'))[param]
		case 'u':
			if user:
				user_id = str(user.id)

				if path and path_len == 2:
					if user_id in cspl_custom_users(interaction).keys() and guild_id in cspl_custom_users(interaction)[user_id].keys() and path[0] in cspl_custom_users(interaction)[user_id][guild_id].keys() and path[1] in cspl_custom_users(interaction)[user_id][guild_id][path[0]].keys() and param in cspl_custom_users(interaction)[user_id][guild_id][path[0]][path[1]].keys():
						return json.load(open("./.db/crossplatform/custom/users.json", "r", encoding="utf-8"))[user_id][guild_id][path[0]][path[1]][param]
					else:
						return yaml.safe_load(open('./.db/crossplatform/initial/users.yml', 'r', encoding='utf-8'))[path[0]][path[1]][param]
				elif path and path_len == 1:
					if user_id in cspl_custom_users(interaction).keys() and guild_id in cspl_custom_users(interaction)[user_id].keys() and path[0] in cspl_custom_users(interaction)[user_id][guild_id].keys() and param in cspl_custom_users(interaction)[user_id][guild_id][path[0]].keys():
						return json.load(open("./.db/crossplatform/custom/users.json", "r", encoding="utf-8"))[user_id][guild_id][path[0]][param]
					else:
						return yaml.safe_load(open('./.db/crossplatform/initial/users.yml', 'r', encoding='utf-8'))[path[0]][param]
				else:
					if user_id in cspl_custom_users(interaction).keys() and guild_id in cspl_custom_users(interaction)[user_id].keys() and param in cspl_custom_users(interaction)[user_id][guild_id].keys():
						return json.load(open("./.db/crossplatform/custom/users.json", "r", encoding="utf-8"))[user_id][guild_id][param]
					else:
						return yaml.safe_load(open('./.db/crossplatform/initial/users.yml', 'r', encoding='utf-8'))[param]
			else:
				if type(interaction) == discord.Interaction:
					user_id = str(interaction.user.id)

					if path and path_len == 2:
						if user_id in cspl_custom_users(interaction).keys() and guild_id in cspl_custom_users(interaction)[user_id].keys() and path[0] in cspl_custom_users(interaction)[user_id][guild_id].keys() and path[1] in cspl_custom_users(interaction)[user_id][guild_id][path[0]].keys() and param in cspl_custom_users(interaction)[user_id][guild_id][path[0]][path[1]].keys():
							return json.load(open("./.db/crossplatform/custom/users.json", "r", encoding="utf-8"))[user_id][guild_id][path[0]][path[1]][param]
						else:
							return yaml.safe_load(open('./.db/crossplatform/initial/users.yml', 'r', encoding='utf-8'))[path[0]][path[1]][param]
					elif path and path_len == 1:
						if user_id in cspl_custom_users(interaction).keys() and guild_id in cspl_custom_users(interaction)[user_id].keys() and path[0] in cspl_custom_users(interaction)[user_id][guild_id].keys() and param in cspl_custom_users(interaction)[user_id][guild_id][path[0]].keys():
							return json.load(open("./.db/crossplatform/custom/users.json", "r", encoding="utf-8"))[user_id][guild_id][path[0]][param]
						else:
							return yaml.safe_load(open('./.db/crossplatform/initial/users.yml', 'r', encoding='utf-8'))[path[0]][param]
					else:
						if user_id in cspl_custom_users(interaction).keys() and guild_id in cspl_custom_users(interaction)[user_id].keys() and param in cspl_custom_users(interaction)[user_id][guild_id].keys():
							return json.load(open("./.db/crossplatform/custom/users.json", "r", encoding="utf-8"))[user_id][guild_id][param]
						else:
							return yaml.safe_load(open('./.db/crossplatform/initial/users.yml', 'r', encoding='utf-8'))[param]
				elif type(interaction) == discord.Message:
					author_id = str(interaction.author.id)

					if path and path_len == 2:
						if author_id in cspl_custom_users(interaction).keys() and guild_id in cspl_custom_users(interaction)[author_id].keys() and path[0] in cspl_custom_users(interaction)[author_id][guild_id].keys() and path[1] in cspl_custom_users(interaction)[author_id][guild_id][path[0]].keys() and param in cspl_custom_users(interaction)[author_id][guild_id][path[0]][path[1]].keys():
							return json.load(open("./.db/crossplatform/custom/users.json", "r", encoding="utf-8"))[author_id][guild_id][path[0]][path[1]][param]
						else:
							return yaml.safe_load(open('./.db/crossplatform/initial/users.yml', 'r', encoding='utf-8'))[path[0]][path[1]][param]
					elif path and path_len == 1:
						if author_id in cspl_custom_users(interaction).keys() and guild_id in cspl_custom_users(interaction)[author_id].keys() and path[0] in cspl_custom_users(interaction)[author_id][guild_id].keys() and param in cspl_custom_users(interaction)[author_id][guild_id][path[0]].keys():
							return json.load(open("./.db/crossplatform/custom/users.json", "r", encoding="utf-8"))[author_id][guild_id][path[0]][param]
						else:
							return yaml.safe_load(open('./.db/crossplatform/initial/users.yml', 'r', encoding='utf-8'))[path[0]][param]
					else:
						if author_id in cspl_custom_users(interaction).keys() and guild_id in cspl_custom_users(interaction)[author_id].keys() and param in cspl_custom_users(interaction)[author_id][guild_id].keys():
							return json.load(open("./.db/crossplatform/custom/users.json", "r", encoding="utf-8"))[author_id][guild_id][param]
						else:
							return yaml.safe_load(open('./.db/crossplatform/initial/users.yml', 'r', encoding='utf-8'))[param]


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
def cspl_get_param_with_merge(interaction, branch, param, path=None, user: discord.Member = None, guild = None):
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