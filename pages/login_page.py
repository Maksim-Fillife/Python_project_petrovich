from data.config import PASSWORD, EMAIL, INVALID_PASSWORD
from locators.locators import LoginPageLocators
from locators.locators import MainPageLocators
from pages.base_page import BasePage
import allure



class LoginPage(BasePage):

    def fill_email(self):
        with allure.step('Ввести email'):
            self.type_text(LoginPageLocators.EMAIL_INPUT, EMAIL)

    def fill_password(self):
        with allure.step('Ввести пароль'):
            self.type_text(LoginPageLocators.PASSWORD_INPUT, PASSWORD)

    def fill_invalid_password(self):
        with allure.step('Ввести неправильный пароль'):
            self.type_text(LoginPageLocators.PASSWORD_INPUT, INVALID_PASSWORD)

    def submit_authorization(self):
        with allure.step('Нажать кнопку "Войти"'):
            self.click(LoginPageLocators.ENTER_BUTTON)

    def is_profile_popup_displayed(self):
        with allure.step('Проверить успешность авторизации'):
            self.hover(LoginPageLocators.PROFILE_BUTTON)
            profile_popup = self.find_element(LoginPageLocators.PROFILE_POPUP)
            return profile_popup.is_displayed()

    def open_profile_popup(self):
        with allure.step('Открыть попап профиля'):
            self.hover(LoginPageLocators.PROFILE_BUTTON)
            self.find_element(MainPageLocators.LOGIN_BUTTON)

    def click_logout(self):
        with allure.step('Нажать кнопку "Выход"'):
            self.click(LoginPageLocators.LOGOUT_BUTTON)

    def get_login_prompt_text(self):
        with allure.step('Проверить успешный выход из профиля'):
            self.click(MainPageLocators.LOGIN_BUTTON)
            return self.get_text(LoginPageLocators.LOGIN_PROMPT)

    def get_error_password_message(self):
        with allure.step('Получить сообщение об ошибке "Неверный пароль"'):
            return self.get_text(LoginPageLocators.ERROR_PASSWORD_MESSAGE)
