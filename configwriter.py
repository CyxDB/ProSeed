from configparser import ConfigParser

def init_configs():
    config = ConfigParser()
    config['DEFAULT'] = {
        'api_key': '',
        'startggapi_url': 'https://api.start.gg/gql/alpha',
        'output_dir': './',
        'user_slug': '',
        'owner_id': ''
    }

    config['StartggAPI'] = {
        'api_key': '',
        'startggapi_url': 'https://api.start.gg/gql/alpha',
        'Authorization': 'Bearer ',
        'Content-Type': 'application/json'
    }

    config['BAN20'] = {
        'api_key' : '9d5bfb54910992d8e3795039f1669237',
        'owner_id' : 1525697,
        'event_id' : 817470,
        'cheat_df_filepath' : 'cheat_df.csv',
        'file_loc' : './',
    }

    with open('./settings.ini', 'w') as f:
        config.write(f)
        
init_configs