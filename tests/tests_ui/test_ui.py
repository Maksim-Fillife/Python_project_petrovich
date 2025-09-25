from selenium.common import StaleElementReferenceException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from data.config import *
import random


def test_login(driver):
    wait = WebDriverWait(driver, 10)
    driver.get(BASE_URL)

    login_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Войти']"))
    )
    login_button.click()

    fill_email = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//input[@data-test='email-login-field']"))
    )
    fill_email.send_keys(email)

    fill_password = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//input[@data-test='password-field']"))
    )
    fill_password.send_keys(password)

    click_enter_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Войти']]"))
    )
    click_enter_button.click()

    open_profile = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[@data-test='login-link']"))
    )
    open_profile.click()

    check_authorization = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//h3[contains(text(),'Личные данные')]"))
    )
    assert check_authorization.text == "Личные данные", "Заголовок страницы не соответствует"

def test_login_with_invalid_password(driver):
    wait = WebDriverWait(driver, 10)
    driver.get(BASE_URL)

    login_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Войти']"))
    )
    login_button.click()

    fill_email = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//input[@data-test='email-login-field']"))
    )
    fill_email.send_keys(email)

    fill_password = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//input[@data-test='password-field']"))
    )
    fill_password.send_keys(invalid_password)

    click_enter_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Войти']]"))
    )
    click_enter_button.click()

    error_password_message = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//p[@data-test='error-msg' and contains(text(), 'Неверный пароль')]"))
    )
    assert error_password_message.text == "Неверный пароль", "Текст не соответствует"

def test_logout(driver):
    action = ActionChains(driver)
    wait = WebDriverWait(driver, 10)
    driver.get(BASE_URL)

    login_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Войти']"))
    )
    login_button.click()

    fill_email = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//input[@data-test='email-login-field']"))
    )
    fill_email.send_keys(email)

    fill_password = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//input[@data-test='password-field']"))
    )
    fill_password.send_keys(password)

    click_enter_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Войти']]"))
    )
    click_enter_button.click()

    open_profile = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[@data-test='login-link']"))
    )
    open_profile.click()
    driver.find_element(By.TAG_NAME, "body").click()

    profile_trigger = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='login-link']"))
    )
    action.move_to_element(profile_trigger).perform()

    logout_button = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='logout-link']"))
    )
    logout_button.click()

    login_prompt = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//p[text()='Войдите, чтобы продолжить']"))
    )
    assert login_prompt.text == "Войдите, чтобы продолжить", "Текст не соответствет"


def test_search_product_by_keyword(driver):
    wait = WebDriverWait(driver, 10)
    driver.get(BASE_URL)

    search_input = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input.header-search-input"))
    )
    keyword = "перфоратор"
    search_input.send_keys(keyword)

    search_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Найти')]"))
    )
    search_button.click()

    result_header = wait.until(
        EC.presence_of_element_located((By.XPATH, "//h1[contains(@class, 'pt-ta-left') and contains(@class, 'pt-wrap')]"))
    )
    header_text = result_header.text
    assert keyword.lower() in header_text.lower(), f"Текст заголовка не соответствует {keyword}"


def test_open_delivery_page(driver):
    wait = WebDriverWait(driver, 10)
    driver.get(BASE_URL)

    services_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-test='services-link']"))
    )
    services_button.click()

    delivery_services = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/services/delivery/']"))
    )
    delivery_services.click()

    check_delivery_title = wait.until(
        EC.text_to_be_present_in_element((By.CSS_SELECTOR, "h2[data-test='delivery-page-title']"), "Доставка и подъем")
    )
    assert check_delivery_title is True, "Ожидался текст 'Доставка и подъем'"


def test_open_product_card(driver):
    wait = WebDriverWait(driver, 10)
    driver.get(BASE_URL)

    search_input = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input.header-search-input"))
    )
    keyword = "краска"
    search_input.send_keys(keyword)
    search_input.send_keys(Keys.ENTER)

    cards = wait.until(
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "span[data-test='product-title']"))
    )
    assert len(cards) > 0

    select_product = random.choice(cards)
    product_name = select_product.text
    print(product_name)
    select_product.click()

    product_title_in_card = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "h1[data-test='product-title']"))
    )
    product_title_text = product_title_in_card.text
    assert product_name.lower() in product_title_text.lower()

def test_add_product_to_cart(driver):
    wait = WebDriverWait(driver, 10)
    driver.get(BASE_URL)

    search_input = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input.header-search-input"))
    )
    keyword = "розетка"
    search_input.send_keys(keyword)
    search_input.send_keys(Keys.ENTER)

    cards = wait.until(
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "span[data-test='product-title']"))
    )
    assert len(cards) > 0

    select_product = random.choice(cards)
    product_name = select_product.text
    print(product_name)
    select_product.click()

    check_product_title = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "h1[data-test='product-title']"))
    )
    product_title_text = check_product_title.text
    assert product_name.lower() in product_title_text.lower()

    max_retries = 3
    for i in range(max_retries):
        try:
            add_to_cart = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-test='add-to-cart-button']"))
            )
            add_to_cart.click()
            break
        except StaleElementReferenceException:
            if i == max_retries - 1:
                raise
            continue

    check_adding = wait.until(
        EC.text_to_be_present_in_element((By.CSS_SELECTOR, "button[data-test='add-to-cart-button']"), "В корзине")
    )
    assert check_adding is True

    open_cart = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-test='cart-link']"))
    )
    open_cart.click()

    check_product_title_in_cart = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "span[data-test='product-title']"))
    )
    product_title_in_cart = check_product_title_in_cart.text
    assert product_name.lower() in product_title_in_cart.lower(), f"Ошибка, в корзине ожидался товар \"{product_name}\""


def test_delete_product_from_cart(driver):
    action = ActionChains(driver)
    wait = WebDriverWait(driver, 10)
    driver.get(BASE_URL)

    search_input = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input.header-search-input"))
    )
    keyword = "крепеж"
    search_input.send_keys(keyword)
    search_input.send_keys(Keys.ENTER)

    cards = wait.until(
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "span[data-test='product-title']"))
    )
    assert len(cards) > 0

    select_product = random.choice(cards)
    product_name = select_product.text
    print(product_name)
    select_product.click()

    check_product_title = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "h1[data-test='product-title']"))
    )
    product_title_text = check_product_title.text
    assert product_name.lower() in product_title_text.lower()

    max_retries = 3
    for i in range(max_retries):
        try:
            add_to_cart = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-test='add-to-cart-button']"))
            )
            add_to_cart.click()
            break
        except StaleElementReferenceException:
            if i == max_retries - 1:
                raise
            continue

    check_adding = wait.until(
        EC.text_to_be_present_in_element((By.CSS_SELECTOR, "button[data-test='add-to-cart-button']"), "В корзине")
    )
    assert check_adding is True

    cart_popup = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "a[data-test='cart-link']"))
    )
    action.move_to_element(cart_popup).perform()

    delete_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test='data-test-deleteCallback']"))
    )
    delete_button.click()
    action.move_to_element(cart_popup).perform()

    quantity_product = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//span[@class='cart-mini-header-cart']/following-sibling::span"))
    )
    quantity_text = quantity_product.text
    assert quantity_text.startswith("0")



def test_add_product_to_favorites(driver):
    wait = WebDriverWait(driver, 10)
    driver.get(BASE_URL)

    search_input = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input.header-search-input"))
    )
    keyword = "ламинат"
    search_input.send_keys(keyword)
    search_input.send_keys(Keys.ENTER)

    cards = wait.until(
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "span[data-test='product-title']"))
    )
    assert len(cards) > 0

    select_product = random.choice(cards)
    product_name = select_product.text
    print(product_name)
    select_product.click()

    product_title_in_card = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "h1[data-test='product-title']"))
    )
    product_title_text = product_title_in_card.text
    assert product_name.lower() in product_title_text.lower()

    add_to_favorite_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[@data-test='product-add-to-favorite-button']"))
    )
    add_to_favorite_button.click()

    check_adding_to_favorites = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//p[contains(text(), 'Добавлено в избранное')]"))
    )
    assert check_adding_to_favorites.is_displayed()
    assert check_adding_to_favorites.text == "Добавлено в избранное"


def test_open_favorites_page_and_verify_item(driver):
    wait = WebDriverWait(driver, 10)
    driver.get(BASE_URL)

    search_input = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input.header-search-input"))
    )
    keyword = "водоснабжение"
    search_input.send_keys(keyword)
    search_input.send_keys(Keys.ENTER)

    cards = wait.until(
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "span[data-test='product-title']"))
    )
    assert len(cards) > 0

    select_product = random.choice(cards)
    product_name = select_product.text
    print(product_name)
    select_product.click()

    add_to_favorite_button = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//button[@data-test='product-add-to-favorite-button' and .='В избранное']"))
    )
    add_to_favorite_button.click()

    open_favorite_page = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[@data-test='favorite-icon']"))
    )
    open_favorite_page.click()

    product_title_in_favorite = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "span[data-test='product-title']"))
    )
    product_title_text = product_title_in_favorite.text
    assert product_name.lower() == product_title_text.lower(), f"Ошибка, в корзине ожидался товар \"{product_name}\""


def test_footer_contains_company_info(driver):
    wait = WebDriverWait(driver, 10)
    driver.get(BASE_URL)

    expected = {"О компании", "Покупателям", "Сервисы", "Лояльность", "Контакты", "Обратная связь"}

    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.footer-grid.footer-links-grid span.footer-title")))

    check_footer = driver.find_elements(By.CSS_SELECTOR, "div.footer-grid.footer-links-grid span.footer-title")

    actual_footer_data = {el.text for el in check_footer}

    assert expected == actual_footer_data






































