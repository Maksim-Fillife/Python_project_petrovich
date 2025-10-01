from selenium.webdriver.common.by import By

class MainPageLocators:
    HEADER_SEARCH_INPUT = (By.CSS_SELECTOR, "input.header-search-input")
    SEARCH_RESULT = (By.XPATH, "//h1[contains(@class, 'pt-ta-left') and contains(@class, 'pt-wrap')]")
    SEARCH_BUTTON = (By.XPATH, "//button[contains(text(),'Найти')]")
    LOGIN_BUTTON = (By.XPATH, "//span[text()='Войти']")
    SERVICES_ICON = (By.CSS_SELECTOR, "a[data-test='services-link']")
    FAVORITE_ICON = (By.XPATH, "//a[@data-test='favorite-icon']")
    CART_ICON = (By.CSS_SELECTOR, "a[data-test='cart-link']")
    FOOTER_TITLE = (By.CSS_SELECTOR, "div.footer-grid.footer-links-grid span.footer-title")

class LoginPageLocators:
    EMAIL_INPUT = (By.XPATH, "//input[@data-test='email-login-field']")
    PASSWORD_INPUT = (By.XPATH, "//input[@data-test='password-field']")
    ENTER_BUTTON = (By.XPATH, "//button[.//span[text()='Войти']]")
    PROFILE_BUTTON = (By.XPATH, "//a[@data-test='login-link']")
    PROFILE_POPUP = (By.CSS_SELECTOR, ".profile-popup-block-section")
    LOGOUT_BUTTON = (By.CSS_SELECTOR, "[data-test='logout-link']")
    ERROR_PASSWORD_MESSAGE = (By.XPATH, "//p[@data-test='error-msg' and contains(text(), 'Неверный пароль')]")
    LOGIN_PROMPT = (By.XPATH, "//p[text()='Войдите, чтобы продолжить']")

class DeliveryPageLocators:
    DELIVERY_PAGE_TITLE = (By.CSS_SELECTOR, "h2[data-test='delivery-page-title']")

class ServicesPageLocators:
    DELIVERY_PAGE_BUTTON =(By.CSS_SELECTOR, "a[href='/services/delivery/']")

class CartPageLocators:
    EMPTY_CART_MESSAGE = (By.XPATH, "//span[contains(text(), 'Корзина пуста')]")
    CART_QUANTITY = (By.XPATH, "//span[@class='cart-mini-header-cart']/following-sibling::span")
    DELETE_FROM_CART_BUTTON = (By.CSS_SELECTOR, "[data-test='data-test-deleteCallback']")

class ProductCardLocators:
    PRODUCT_TITLE = (By.CSS_SELECTOR, "span[data-test='product-title']")
    TITLE_IN_CART = (By.CSS_SELECTOR, "h1[data-test='product-title']")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, "button[data-test='add-to-cart-button']")
    ADD_TO_FAVORITE_BUTTON = (By.XPATH, "//button[@data-test='product-add-to-favorite-button']")
    FAVORITE_ADDED_MESSAGE = (By.XPATH, "//p[contains(text(), 'Добавлено в избранное')]")
