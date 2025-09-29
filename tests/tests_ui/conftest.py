from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
from pages.product_page import ProductPage
from pages.login_page import LoginPage
from pages.main_page import MainPage
from selenium import webdriver
import pytest




@pytest.fixture(scope='function', autouse=True)
def driver():
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    # options.add_argument('--no-sandbox')
    options.add_argument('--incognito')
    options.add_argument('--window-size=1920,1080')
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()

@pytest.fixture
def main_page(driver):
    return MainPage(driver)

@pytest.fixture
def login_page(driver):
    return LoginPage(driver)

@pytest.fixture
def product_page(driver):
    return ProductPage(driver)