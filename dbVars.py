import yaml
import json
import glob
import clusters

bot_presence = lambda: yaml.safe_load(open('./.db/bot/bot.yml', 'r', encoding='utf-8'))['presence']

# yml initial config
crsp_initial_guilds = lambda: yaml.safe_load(open('./.db/crossparams/initial/guilds.yml', 'r', encoding='utf-8'))
crsp_initial_users = lambda: yaml.safe_load(open('./.db/crossparams/initial/users.yml', 'r', encoding='utf-8'))

# json custom config
#def get_crsp_custom_guilds():
#	with open(f'./.db/crossparams/custom/clusters-guilds.json', 'r', encoding='utf-8') as read_file: clusters_guilds = json.load(read_file)
#	
#
#	guild_cluster = clusters_guilds
#	with open(f'./.db/crossparams/custom/clusters/{guild_cluster}/guilds.json', 'r', encoding='utf-8') as read_file: return json.load(read_file)
#crsp_custom_guilds = get_crsp_custom_guilds

def get_guild_prefix(ctx):
	with open(f'./.db/crossparams/custom/clusters-guilds.json', 'r', encoding='utf-8') as read_file: clusters_guilds = json.load(read_file)
	guild_id = str(ctx.guild.id)

	# Поиск кластера, в котором находится сервер
	for key, value in clusters_guilds.items():
		if guild_id in value["guilds"]:
			guild_cluster = key
			break
		else:
			break # не робит
	#print(f"Сервер {guild_id} находится в кластере {guild_cluster}")

	with open(f'./.db/crossparams/custom/clusters/{guild_cluster}/guilds.json', 'r', encoding='utf-8') as read_file: cluster_guilds = json.load(read_file)

	if "prefix" in cluster_guilds[guild_id]:
		with open(f'./.db/crossparams/custom/clusters/{guild_cluster}/guilds.json', 'r', encoding='utf-8') as read_file: return json.load(read_file)[guild_id]["prefix"]
	else:
		return lambda: yaml.safe_load(open('./.db/crossparams/initial/guilds.yml', 'r', encoding='utf-8'))["prefix"]
guild_prefix = get_guild_prefix