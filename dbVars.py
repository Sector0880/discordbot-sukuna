import json
import yaml

bot_presence = lambda: yaml.safe_load(open('./.db/bot/bot.yml', 'r', encoding='utf-8'))['presence']
sf_a = lambda: yaml.safe_load(open('./.db/staff.yml', 'r', encoding='utf-8'))['staffList_Admins']
sf_sp = lambda: yaml.safe_load(open('./.db/staff.yml', 'r', encoding='utf-8'))['staffList_SpecialPerms']

cspl_initial_guilds = lambda: yaml.safe_load(open('./.db/crossplatform/initial/guilds.yml', 'r', encoding='utf-8'))
cspl_initial_users = lambda: yaml.safe_load(open('./.db/crossplatform/initial/users.yml', 'r', encoding='utf-8'))

cspl_custom_guilds = lambda ctx: json.load(open("./.db/crossplatform/custom/guilds.json", "r", encoding="utf-8"))
cspl_custom_users = lambda ctx: json.load(open("./.db/crossplatform/custom/users.json", "r", encoding="utf-8"))

"""
Метод получения параметра из бд
1. Для чего: Можно получить определенный параметр из базы данных кроссплатформера
2. Как работает: cspl_get_param(!ctx, !ветка кроссплатформера, !параметр, дополнительный путь до параметра)
Примеры: 
cspl_get_param(ctx, 'guilds', 'prefix')
cspl_get_param(ctx, 'guilds', 'status', 'premium')
3. Особенности: Идет проверка на наличие кастомного параметра
"""
def cspl_get_param(ctx, _branch, _param, _path1 = None):
	match _branch:
		case 'guilds':
			if str(ctx.guild.id) in cspl_custom_guilds(ctx).keys() and _param in cspl_custom_guilds(ctx)[str(ctx.guild.id)]:
				if _path1: return json.load(open("./.db/crossplatform/custom/guilds.json", "r", encoding="utf-8"))[_path1][_param]
				else: return json.load(open("./.db/crossplatform/custom/guilds.json", "r", encoding="utf-8"))[_param]
			else:
				if _path1: return yaml.safe_load(open('./.db/crossplatform/initial/guilds.yml', 'r', encoding='utf-8'))[_path1][_param]
				else: return yaml.safe_load(open('./.db/crossplatform/initial/guilds.yml', 'r', encoding='utf-8'))[_param]