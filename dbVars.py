import yaml
import json
import glob

bot_presence = lambda: yaml.safe_load(open('./.db/bot/bot.yml', 'r', encoding='utf-8'))['presence']

mltp_initial_guilds = lambda: yaml.safe_load(open('./.db/multipresence/initial/guilds.yml', 'r', encoding='utf-8'))
mltp_custom_guilds = lambda: [json.load(open(file, 'r', encoding='utf-8')) for file in glob.glob('./.db/multipresence/custom/guilds/*.json')]

def guild_prefix(ctx):
	for custom_guild in mltp_custom_guilds():
		if str(ctx.guild.id) in custom_guild.keys():
			return custom_guild[str(ctx.guild.id)]['prefix']
	return mltp_initial_guilds()['prefix']

MAX_SERVERS_PER_FILE = 10
DIRECTORY = './.db/multipresence/custom/guilds/'

def modify_guild_prefix(guild_id, new_prefix):
	# Проверяем, существуют ли файлы в директории
	if not glob.glob(DIRECTORY + '*.json'):
		# Если файлы не существуют, создаем новый файл
		filename = f'file1.json'
		data = {guild_id: {"prefix": new_prefix}}
		with open(DIRECTORY + filename, 'w', encoding='utf-8') as file:
			json.dump(data, file, ensure_ascii=False, indent=4)
	else:
		# Получаем список файлов в директории
		files = glob.glob(DIRECTORY + '*.json')
		# Перебираем файлы по порядку
		for file_path in files:
			with open(file_path, 'r', encoding='utf-8') as file:
				data = json.load(file)
				# Проверяем, есть ли сервер в текущем файле
				if guild_id in data:
					# Если сервер найден, изменяем его префикс
					if data[guild_id]['prefix'] != new_prefix:
						data[guild_id]['prefix'] = new_prefix
						with open(file_path, 'w', encoding='utf-8') as file:
							json.dump(data, file, ensure_ascii=False, indent=4)
					break
				# Проверяем количество серверов в файле
				elif len(data) < MAX_SERVERS_PER_FILE:
					# Если количество серверов не превышает лимит, добавляем информацию в текущий файл
					if guild_id not in data:
						if len(data) < MAX_SERVERS_PER_FILE:
							data[guild_id] = {"prefix": new_prefix}
							with open(file_path, 'w', encoding='utf-8') as file:
								json.dump(data, file, ensure_ascii=False, indent=4)
						else:
							# Создаем новый файл, если превышен лимит серверов в текущем файле
							file_number = int(file_path.split('.')[0].replace('file', '')) + 1
							filename = f'file{file_number}.json'
							data = {guild_id: {"prefix": new_prefix}}
							with open(DIRECTORY + filename, 'w', encoding='utf-8') as file:
								json.dump(data, file, ensure_ascii=False, indent=4)
					break
			# Если достигнут конец файла и сервер не найден, создаем новый файл
			if file_path == files[-1]:
				file_number = int(file_path.split('.')[0].replace('file', '')) + 1
				filename = f'file{file_number}.json'
				data = {guild_id: {"prefix": new_prefix}}
				with open(DIRECTORY + filename, 'w', encoding='utf-8') as file:
					json.dump(data, file, ensure_ascii=False, indent=4)


mltp_initial_users = lambda: yaml.safe_load(open('./.db/multipresence/initial/users.yml', 'r', encoding='utf-8'))
mltp_custom_users = lambda: [json.load(open(file, 'r', encoding='utf-8')) for file in glob.glob('./.db/multipresence/custom/users/*.json')]