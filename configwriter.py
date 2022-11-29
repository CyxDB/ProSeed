from configparser import ConfigParser

def init_configs():
    config = ConfigParser()
    config['DEFAULT'] = {
        'api_key': '',
        'output_dir': './',
        'user_slug': '',
        'owner_id': ''
    }

    config['User'] = {
        'api_key': '',
    }

    with open('./settings.ini', 'w') as f:
        config.write(f)