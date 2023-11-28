import yaml
import json
import glob
import clusters

bot_presence = lambda: yaml.safe_load(open('./.db/bot/bot.yml', 'r', encoding='utf-8'))['presence']

# yml initial config
crsp_initial_guilds = lambda: yaml.safe_load(open('./.db/crossparams/initial/guilds.yml', 'r', encoding='utf-8'))
crsp_initial_users = lambda: yaml.safe_load(open('./.db/crossparams/initial/users.yml', 'r', encoding='utf-8'))

def guild_prefix(ctx):
    with open('./.db/crossparams/custom/clusters-guilds.json', 'r', encoding='utf-8') as read_file: clusters_guilds = json.load(read_file)
    
    guild_id = str(ctx.guild.id)

    for key, value in clusters_guilds.items():
        if guild_id in value["guilds"]:
            guild_cluster = key
            with open(f'./.db/crossparams/custom/clusters/{guild_cluster}/guilds.json', 'r', encoding='utf-8') as read_file:cluster_guilds = json.load(read_file)
                
            if guild_id in cluster_guilds: return cluster_guilds[guild_id]["prefix"]

    return yaml.safe_load(open('./.db/crossparams/initial/guilds.yml', 'r', encoding='utf-8'))["prefix"]