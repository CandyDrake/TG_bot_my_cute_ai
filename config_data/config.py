from dotenv import load_dotenv
import os
load_dotenv()
AI_TOKEN = os.getenv("AI_TOKEN")
BOT_TOKEN = os.getenv("BOT_TOKEN")
USER_IDS_FILE = os.path.join(os.path.dirname(__file__), '../user_ids.json')