from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains
from locators.locators import CommonLocators




class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 50)
        self.action = ActionChains(driver)

    def click(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def find_element(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_elements(self, locator):
        #Возвращает список элементов (для карточек товаров)
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def hover(self, locator):
        #Наведение курсора на элемент
        body = self.find_element(CommonLocators.BODY)
        body.click()
        element = self.wait.until(EC.visibility_of_element_located(locator))
        self.action.move_to_element(element).perform()

    def scroll_to_element(self, locator):
        #Прокрутка к элементу
        element = self.wait.until(EC.visibility_of_element_located(locator))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)

    def type_text(self, locator, text):
        #Ввод текста в поле
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        #Возвращает текст видимого элемента
        element = self.wait.until(EC.visibility_of_element_located(locator))
        return element.text.strip()

    def wait_for_text_in_element(self, locator, expected_text):
        #Ждёт, пока в элементе не появится нужный текст
        return self.wait.until(EC.text_to_be_present_in_element(locator, expected_text))

    def is_element_visible(self, locator):
        #Ждет, отображение элемента
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

