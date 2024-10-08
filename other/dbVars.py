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

"""
* обновить
Метод получения параметра из бд
1. Для чего: Можно получить определенный параметр из базы данных кроссплатформера
2. Как работает: cspl_get_param(!interaction, !ветка кроссплатформера, !параметр, дополнительный путь до параметра)
Примеры: 
cspl_get_param(interaction, 'guilds', 'prefix')
cspl_get_param(interaction, 'guilds', 'status', 'premium')
3. Особенности: Идет проверка на наличие кастомного параметра
"""
def cspl_get_param(interaction, branch, param, path = None, user: discord.Member = None):
	if path: path_len = len(path)
	match branch:
		case 'g':
			if path and path_len == 2:
				if str(interaction.guild.id) in cspl_custom_guilds(interaction).keys() and path[0] in cspl_custom_guilds(interaction)[str(interaction.guild.id)].keys() and path[1] in cspl_custom_guilds(interaction)[str(interaction.guild.id)][path[0]].keys() and param in cspl_custom_guilds(interaction)[str(interaction.guild.id)][path[0]][path[1]].keys():
					return json.load(open("./.db/crossplatform/custom/guilds.json", "r", encoding="utf-8"))[str(interaction.guild.id)][path[0]][path[1]][param]
				else:
					return yaml.safe_load(open('./.db/crossplatform/initial/guilds.yml', 'r', encoding='utf-8'))[path[0]][path[1]][param]
			elif path and path_len == 1:
				if str(interaction.guild.id) in cspl_custom_guilds(interaction).keys() and path[0] in cspl_custom_guilds(interaction)[str(interaction.guild.id)].keys() and param in cspl_custom_guilds(interaction)[str(interaction.guild.id)][path[0]].keys():
					return json.load(open("./.db/crossplatform/custom/guilds.json", "r", encoding="utf-8"))[str(interaction.guild.id)][path[0]][param]
				else:
					return yaml.safe_load(open('./.db/crossplatform/initial/guilds.yml', 'r', encoding='utf-8'))[path[0]][param]
			else:
				if str(interaction.guild.id) in cspl_custom_guilds(interaction).keys() and param in cspl_custom_guilds(interaction)[str(interaction.guild.id)].keys():
					return json.load(open("./.db/crossplatform/custom/guilds.json", "r", encoding="utf-8"))[str(interaction.guild.id)][param]
				else:
					return yaml.safe_load(open('./.db/crossplatform/initial/guilds.yml', 'r', encoding='utf-8'))[param]
		case 'u':
			if user:
				if path and path_len == 2:
					if str(user.id) in cspl_custom_users(interaction).keys() and str(interaction.guild.id) in cspl_custom_users(interaction)[str(user.id)].keys() and path[0] in cspl_custom_users(interaction)[str(user.id)][str(interaction.guild.id)].keys() and path[1] in cspl_custom_users(interaction)[str(user.id)][str(interaction.guild.id)][path[0]].keys() and param in cspl_custom_users(interaction)[str(user.id)][str(interaction.guild.id)][path[0]][path[1]].keys():
						return json.load(open("./.db/crossplatform/custom/users.json", "r", encoding="utf-8"))[str(user.id)][str(interaction.guild.id)][path[0]][path[1]][param]
					else:
						return yaml.safe_load(open('./.db/crossplatform/initial/users.yml', 'r', encoding='utf-8'))[path[0]][path[1]][param]
				elif path and path_len == 1:
					if str(user.id) in cspl_custom_users(interaction).keys() and str(interaction.guild.id) in cspl_custom_users(interaction)[str(user.id)].keys() and path[0] in cspl_custom_users(interaction)[str(user.id)][str(interaction.guild.id)].keys() and param in cspl_custom_users(interaction)[str(user.id)][str(interaction.guild.id)][path[0]].keys():
						return json.load(open("./.db/crossplatform/custom/users.json", "r", encoding="utf-8"))[str(user.id)][str(interaction.guild.id)][path[0]][param]
					else:
						return yaml.safe_load(open('./.db/crossplatform/initial/users.yml', 'r', encoding='utf-8'))[path[0]][param]
				else:
					if str(user.id) in cspl_custom_users(interaction).keys() and str(interaction.guild.id) in cspl_custom_users(interaction)[str(user.id)].keys() and param in cspl_custom_users(interaction)[str(user.id)][str(interaction.guild.id)].keys():
						return json.load(open("./.db/crossplatform/custom/users.json", "r", encoding="utf-8"))[str(user.id)][str(interaction.guild.id)][param]
					else:
						return yaml.safe_load(open('./.db/crossplatform/initial/users.yml', 'r', encoding='utf-8'))[param]
			else:
				if type(interaction) == discord.Interaction:
					if path and path_len == 2:
						if str(interaction.user.id) in cspl_custom_users(interaction).keys() and str(interaction.guild.id) in cspl_custom_users(interaction)[str(interaction.user.id)].keys() and path[0] in cspl_custom_users(interaction)[str(interaction.user.id)][str(interaction.guild.id)].keys() and path[1] in cspl_custom_users(interaction)[str(interaction.user.id)][str(interaction.guild.id)][path[0]].keys() and param in cspl_custom_users(interaction)[str(interaction.user.id)][str(interaction.guild.id)][path[0]][path[1]].keys():
							return json.load(open("./.db/crossplatform/custom/users.json", "r", encoding="utf-8"))[str(interaction.user.id)][str(interaction.guild.id)][path[0]][path[1]][param]
						else:
							return yaml.safe_load(open('./.db/crossplatform/initial/users.yml', 'r', encoding='utf-8'))[path[0]][path[1]][param]
					elif path and path_len == 1:
						if str(interaction.user.id) in cspl_custom_users(interaction).keys() and str(interaction.guild.id) in cspl_custom_users(interaction)[str(interaction.user.id)].keys() and path[0] in cspl_custom_users(interaction)[str(interaction.user.id)][str(interaction.guild.id)].keys() and param in cspl_custom_users(interaction)[str(interaction.user.id)][str(interaction.guild.id)][path[0]].keys():
							return json.load(open("./.db/crossplatform/custom/users.json", "r", encoding="utf-8"))[str(interaction.user.id)][str(interaction.guild.id)][path[0]][param]
						else:
							return yaml.safe_load(open('./.db/crossplatform/initial/users.yml', 'r', encoding='utf-8'))[path[0]][param]
					else:
						if str(interaction.user.id) in cspl_custom_users(interaction).keys() and str(interaction.guild.id) in cspl_custom_users(interaction)[str(interaction.user.id)].keys() and param in cspl_custom_users(interaction)[str(interaction.user.id)][str(interaction.guild.id)].keys():
							return json.load(open("./.db/crossplatform/custom/users.json", "r", encoding="utf-8"))[str(interaction.user.id)][str(interaction.guild.id)][param]
						else:
							return yaml.safe_load(open('./.db/crossplatform/initial/users.yml', 'r', encoding='utf-8'))[param]
				elif type(interaction) == discord.Message:
					if path and path_len == 2:
						if str(interaction.author.id) in cspl_custom_users(interaction).keys() and str(interaction.guild.id) in cspl_custom_users(interaction)[str(interaction.author.id)].keys() and path[0] in cspl_custom_users(interaction)[str(interaction.author.id)][str(interaction.guild.id)].keys() and path[1] in cspl_custom_users(interaction)[str(interaction.author.id)][str(interaction.guild.id)][path[0]].keys() and param in cspl_custom_users(interaction)[str(interaction.author.id)][str(interaction.guild.id)][path[0]][path[1]].keys():
							return json.load(open("./.db/crossplatform/custom/users.json", "r", encoding="utf-8"))[str(interaction.author.id)][str(interaction.guild.id)][path[0]][path[1]][param]
						else:
							return yaml.safe_load(open('./.db/crossplatform/initial/users.yml', 'r', encoding='utf-8'))[path[0]][path[1]][param]
					elif path and path_len == 1:
						if str(interaction.author.id) in cspl_custom_users(interaction).keys() and str(interaction.guild.id) in cspl_custom_users(interaction)[str(interaction.author.id)].keys() and path[0] in cspl_custom_users(interaction)[str(interaction.author.id)][str(interaction.guild.id)].keys() and param in cspl_custom_users(interaction)[str(interaction.author.id)][str(interaction.guild.id)][path[0]].keys():
							return json.load(open("./.db/crossplatform/custom/users.json", "r", encoding="utf-8"))[str(interaction.author.id)][str(interaction.guild.id)][path[0]][param]
						else:
							return yaml.safe_load(open('./.db/crossplatform/initial/users.yml', 'r', encoding='utf-8'))[path[0]][param]
					else:
						if str(interaction.author.id) in cspl_custom_users(interaction).keys() and str(interaction.guild.id) in cspl_custom_users(interaction)[str(interaction.author.id)].keys() and param in cspl_custom_users(interaction)[str(interaction.author.id)][str(interaction.guild.id)].keys():
							return json.load(open("./.db/crossplatform/custom/users.json", "r", encoding="utf-8"))[str(interaction.author.id)][str(interaction.guild.id)][param]
						else:
							return yaml.safe_load(open('./.db/crossplatform/initial/users.yml', 'r', encoding='utf-8'))[param]