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

mltp_initial_users = lambda: yaml.safe_load(open('./.db/multipresence/initial/users.yml', 'r', encoding='utf-8'))
mltp_custom_users = lambda: [json.load(open(file, 'r', encoding='utf-8')) for file in glob.glob('./.db/multipresence/custom/users/*.json')]