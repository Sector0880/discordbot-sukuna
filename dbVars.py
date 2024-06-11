import json
import yaml
import discord
from discord import app_commands

bot_presence = lambda: yaml.safe_load(open('./.db/bot/bot.yml', 'r', encoding='utf-8'))['presence']
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
def cspl_get_param(interaction, _branch, _param, _path1 = None, _user: discord.Member = None):
	match _branch:
		case 'g':
			if str(interaction.guild.id) in cspl_custom_guilds(interaction).keys() and (_param in cspl_custom_guilds(interaction)[str(interaction.guild.id)].keys() or _param in cspl_custom_guilds(interaction)[str(interaction.guild.id)][_path1].keys()):
				if _path1: return json.load(open("./.db/crossplatform/custom/guilds.json", "r", encoding="utf-8"))[str(interaction.guild.id)][_path1][_param]
				else: return json.load(open("./.db/crossplatform/custom/guilds.json", "r", encoding="utf-8"))[str(interaction.guild.id)][_param]
			else:
				if _path1: return yaml.safe_load(open('./.db/crossplatform/initial/guilds.yml', 'r', encoding='utf-8'))[_path1][_param]
				else: return yaml.safe_load(open('./.db/crossplatform/initial/guilds.yml', 'r', encoding='utf-8'))[_param]
		case 'u':
			if _user:
				if str(_user.id) in cspl_custom_users(interaction).keys() and str(interaction.guild.id) in cspl_custom_users(interaction)[str(_user.id)].keys() and (_param in cspl_custom_users(interaction)[str(_user.id)][str(interaction.guild.id)].keys() or _param in cspl_custom_users(interaction)[str(_user.id)][str(interaction.guild.id)][_path1].keys()):
					if _path1: return json.load(open("./.db/crossplatform/custom/users.json", "r", encoding="utf-8"))[str(_user.id)][str(interaction.guild.id)][_path1][_param]
					else: return json.load(open("./.db/crossplatform/custom/users.json", "r", encoding="utf-8"))[str(_user.id)][str(interaction.guild.id)][_param]
				else:
					if _path1: return yaml.safe_load(open('./.db/crossplatform/initial/users.yml', 'r', encoding='utf-8'))[_path1][_param]
					else: return yaml.safe_load(open('./.db/crossplatform/initial/users.yml', 'r', encoding='utf-8'))[_param]
			else:
				if str(interaction.user.id) in cspl_custom_users(interaction).keys() and str(interaction.guild.id) in cspl_custom_users(interaction)[str(interaction.user.id)].keys() and (_param in cspl_custom_users(interaction)[str(interaction.user.id)][str(interaction.guild.id)].keys() or _param in cspl_custom_users(interaction)[str(interaction.user.id)][str(interaction.guild.id)][_path1].keys()):
					if _path1: return json.load(open("./.db/crossplatform/custom/users.json", "r", encoding="utf-8"))[str(interaction.user.id)][str(interaction.guild.id)][_path1][_param]
					else: return json.load(open("./.db/crossplatform/custom/users.json", "r", encoding="utf-8"))[str(interaction.user.id)][str(interaction.guild.id)][_param]
				else:
					if _path1: return yaml.safe_load(open('./.db/crossplatform/initial/users.yml', 'r', encoding='utf-8'))[_path1][_param]
					else: return yaml.safe_load(open('./.db/crossplatform/initial/users.yml', 'r', encoding='utf-8'))[_param]