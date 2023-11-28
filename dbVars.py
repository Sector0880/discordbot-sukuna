import yaml
import json
import glob
import clusters

bot_presence = lambda: yaml.safe_load(open('./.db/bot/bot.yml', 'r', encoding='utf-8'))['presence']

mltp_initial_guilds = lambda: yaml.safe_load(open('./.db/crossparams/initial/guilds.yml', 'r', encoding='utf-8'))


def get_guild_prefix(ctx):
	guild_cluster = list(clusters.clusters.keys())[0]
	if guild_cluster == "none":
		guild_prefix = yaml.safe_load(open(f'./.db/crossparams/initial/guilds.yml', 'r', encoding='utf-8'))["prefix"]
	else:
		guild_prefix = json.load(open(f'./.db/crossparams/custom/clusters/{guild_cluster}/guilds.yml', 'r', encoding='utf-8'))[str(ctx.guild.id)]["prefix"]
	return guild_prefix



mltp_initial_users = lambda: yaml.safe_load(open('./.db/crossparams/initial/users.yml', 'r', encoding='utf-8'))