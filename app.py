import os
from src.app import create_app

config_name = os.getenv('FLASK_CONFIG') or 'dev'

app = create_app(config_name)