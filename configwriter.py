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

    with open('./settings.ini', 'w') as f:
        config.write(f)
        
init_configs