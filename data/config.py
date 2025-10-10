import os
import dotenv
dotenv.load_dotenv()

PASSWORD = os.getenv("PASSWORD")
EMAIL = os.getenv("EMAIL")
INVALID_PASSWORD = "<PASSWORD>"
BASE_URL = "https://petrovich.ru/"
COOKIES = os.getenv("COOKIES")