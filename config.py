import os
from typing import List

API_ID = os.environ.get("API_ID", "37476811")
API_HASH = os.environ.get("API_HASH", "7aa60670b871050820086c6267371ee6")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8903849115:AAGDXLU5J2KjUb0Z1J6bhCk2ulytajNXmlQ")
# PICS removed — now using Wallhaven API (see TechifyBots/commands.py)
ADMIN = int(os.environ.get("ADMIN", "8730393744"))
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1003955674028"))
DB_URI = os.environ.get("DB_URI", "mongodb+srv://Anujedit:Anujedit@cluster0.7cs2nhd.mongodb.net/?appName=Cluster0")
DB_NAME = os.environ.get("DB_NAME", "Anujedit")
IS_FSUB = os.environ.get("IS_FSUB", "False").lower() == "true"  # Set "True" For Enable Force Subscribe
AUTH_CHANNELS = list(map(int, os.environ.get("AUTH_CHANNELS", "").split())) # Add Multiple channel ids
AUTH_REQ_CHANNELS = list(map(int, os.environ.get("AUTH_REQ_CHANNELS", "").split())) # Add Multiple channel ids
FSUB_EXPIRE = int(os.environ.get("FSUB_EXPIRE", 2))  # minutes, 0 = no expiry
