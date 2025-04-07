import os

SECRET_KEY = os.environ.get("SECRET_KEY") or "dev_secret_key"
DATABASE = "jallow_world.db"
