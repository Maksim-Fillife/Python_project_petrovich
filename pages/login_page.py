from data.config import PASSWORD, EMAIL, INVALID_PASSWORD
from locators.locators import LoginPageLocators
from locators.locators import MainPageLocators
from pages.base_page import BasePage
import allure



class LoginPage(BasePage):

    def fill_email(self):
        with allure.step('Fill email'):
            self.type_text(LoginPageLocators.EMAIL_INPUT, EMAIL)

    def fill_password(self):
        with allure.step('Fill password'):
            self.type_text(LoginPageLocators.PASSWORD_INPUT, PASSWORD)

    def fill_invalid_password(self):
        with allure.step('Fill invalid password'):
            self.type_text(LoginPageLocators.PASSWORD_INPUT, INVALID_PASSWORD)

    def submit_authorization(self):
        with allure.step('Submit authorization'):
            self.click(LoginPageLocators.ENTER_BUTTON)

    def check_successful_auth(self):
        with allure.step('Check successful auth'):
            self.hover(LoginPageLocators.PROFILE_BUTTON)
            profile_popup = self.find_element(LoginPageLocators.PROFILE_POPUP)
            assert profile_popup.is_displayed(), "Профиль не отобразился"

    def open_profile_popup(self):
        with allure.step('Open profile popup'):
            self.hover(LoginPageLocators.PROFILE_BUTTON)

    def click_logout(self):
        with allure.step('Click logout'):
            self.click(LoginPageLocators.LOGOUT_BUTTON)

    def check_logout(self):
        with allure.step('Check logout'):
            self.click(MainPageLocators.LOGIN_BUTTON)
            login_prompt = self.get_text(LoginPageLocators.LOGIN_PROMPT)
            assert login_prompt == "Войдите, чтобы продолжить", "Текст не соответствет"

    def check_unsuccessful_auth(self):
        with allure.step('Check unsuccessful auth'):
            error_password_message = self.get_text(LoginPageLocators.ERROR_PASSWORD_MESSAGE)
            assert error_password_message == "Неверный пароль", "Текст не соответствует"
