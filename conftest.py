from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import pytest




@pytest.fixture(scope='function', autouse=True)
def driver():
    # options = Options()
    # options.add_argument('--headless=new')
    # options.add_argument("--no-sandbox")
    # options.add_argument("--window-size=1920,1080")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    yield driver