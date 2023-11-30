import yaml
import json
import glob
import clusters

bot_presence = lambda: yaml.safe_load(open('./.db/bot/bot.yml', 'r', encoding='utf-8'))['presence']

# yml initial config
crsp_initial_guilds = lambda: yaml.safe_load(open('./.db/crossparams/initial/guilds.yml', 'r', encoding='utf-8'))
crsp_initial_users = lambda: yaml.safe_load(open('./.db/crossparams/initial/users.yml', 'r', encoding='utf-8'))

def crsp_item(ctx, param, item):
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

	guild_id = str(ctx.guild.id)

	with open(f'./.db/crossparams/custom/clusters-{param}.json', 'r', encoding='utf-8') as read_file:
		clusters_param = json.load(read_file)

	if param == 'guilds':
		for key, value in clusters_param.items():
			if guild_id in value['guilds']:
				guild_cluster = key
				with open(f'./.db/crossparams/custom/clusters/{guild_cluster}/{param}.json', 'r', encoding='utf-8') as read_file:
					cluster_param = json.load(read_file)

				if guild_id in cluster_param:
					result = cluster_param[guild_id]
					for p in path[param][item]:
						result = result.get(p)
						if result is None:
							# Если значения в пути отсутствуют, используем данные из yml
							param_yaml = yaml.safe_load(open(f'./.db/crossparams/initial/{param}.yml', 'r', encoding='utf-8'))
							for p in path[param][item]:
								param_yaml = param_yaml.get(p)
							return param_yaml
					return result

				else:
					param_yaml = yaml.safe_load(open(f'./.db/crossparams/initial/{param}.yml', 'r', encoding='utf-8'))
					for p in path[param][item]:
						param_yaml = param_yaml.get(p)
					return param_yaml
	elif param == 'users':
		raise ValueError('Users скоро будут доступны...')