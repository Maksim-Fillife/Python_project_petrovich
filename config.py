import os
import dotenv
dotenv.load_dotenv()

password = os.getenv("PASSWORD")
email = os.getenv("EMAIL")
invalid_password = "<PASSWORD>"
BASE_URL = "https://petrovich.ru/"