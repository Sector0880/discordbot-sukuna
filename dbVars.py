import yaml
import json

bot_presence = lambda: yaml.safe_load(open('./.db/bot/bot.yml', 'r', encoding='utf-8'))['presence']
sf_a = lambda ctx: yaml.safe_load(open('./.db/staff.yml', 'r', encoding='utf-8'))['staffList_Admins']
sf_sp = lambda ctx: yaml.safe_load(open('./.db/staff.yml', 'r', encoding='utf-8'))['staffList_SpecialPerms']

cspl_initial_guilds = lambda ctx: yaml.safe_load(open('./.db/crossplatform/initial/guilds.yml', 'r', encoding='utf-8'))
cspl_initial_users = lambda ctx: yaml.safe_load(open('./.db/crossplatform/initial/users.yml', 'r', encoding='utf-8'))

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