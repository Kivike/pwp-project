import os
from src.app import create_app

config_mode = os.getenv('FLASK_ENV') or 'development'

app = create_app(config_mode)
if __name__ == "__main__":
    app.run(host='0.0.0.0')