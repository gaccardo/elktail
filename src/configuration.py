import sys
import os
import configparser


def get_config():
    config_path = os.path.join(
        os.environ.get("HOME"),
        ".config/elktail/config.ini"
    )

    if not os.path.exists(config_path):
        print("must create a config file first")
        sys.exit(-1)

    config = configparser.ConfigParser()
    config.read(config_path)
    return {
        'host': config['default']['host'],
        'username': config['default']['username'],
        'scheme': config['default']['scheme'],
        'password': config['default']['password'],
        'port': int(config['default']['port'])
    }
