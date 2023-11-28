import yaml
import json
import glob
import clusters

bot_presence = lambda: yaml.safe_load(open('./.db/bot/bot.yml', 'r', encoding='utf-8'))['presence']

# yml initial config
crsp_initial_guilds = lambda: yaml.safe_load(open('./.db/crossparams/initial/guilds.yml', 'r', encoding='utf-8'))
crsp_initial_users = lambda: yaml.safe_load(open('./.db/crossparams/initial/users.yml', 'r', encoding='utf-8'))

# надо поизучать, все работает правильно но путь имба!
def crsp_item(ctx, initial, item): # надо сделать так чтобы не только guild параметры передавал, но и users
    guild_id = str(ctx.guild.id)
    allowed_items = [ # Допустимые значения для аргумента item
        'cluster',
        'gateaway-status',
        'prefix',
        'language',
        'modules', 'moderation', 'profile', 'fun', 'audit', 'music',
        'premium-status'
    ]
    path_items = {
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
    }

    # возможные ошибки
    if item not in allowed_items:
        raise ValueError('Недопустимое значение для аргумента item. Допустимые значения: ```' + "\n".join(allowed_items) + '```')
    
    path = path_items[item]

    with open('./.db/crossparams/custom/clusters-guilds.json', 'r', encoding='utf-8') as read_file:
        clusters_guilds = json.load(read_file)


    for key, value in clusters_guilds.items():
        if guild_id in value['guilds']:
            guild_cluster = key
            with open(f'./.db/crossparams/custom/clusters/{guild_cluster}/guilds.json', 'r', encoding='utf-8') as read_file:
                cluster_guilds = json.load(read_file)

            if guild_id in cluster_guilds:
                result = cluster_guilds[guild_id]
                for p in path:
                    result = result.get(p)
                    if result is None: # надо жеско посидеть и расписать как это говно работает! НО ОНО РАБОТАЕТ ОТЛИЧНЕЙШЕЕЕЕ
                        # Если значения в пути отсутствуют, используем данные из yml
                        guilds_yaml = yaml.safe_load(open('./.db/crossparams/initial/guilds.yml', 'r', encoding='utf-8'))
                        for p in path:
                            guilds_yaml = guilds_yaml.get(p)
                        return guilds_yaml
                return result

            else:
                guilds_yaml = yaml.safe_load(open('./.db/crossparams/initial/guilds.yml', 'r', encoding='utf-8'))
                for p in path:
                    guilds_yaml = guilds_yaml.get(p)
                return guilds_yaml
    # и этот код надо оптимизировать