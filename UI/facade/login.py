from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from locators.login import Login

class LoginFacade:
    def __init__(self, driver):
        self.driver = driver

    def login(self, username, password):
        self.driver.find_element(*Login.USERNAME).send_keys(username)
        self.driver.find_element(*Login.PASSWORD).send_keys(password)
        self.driver.find_element(*Login.LOGIN_BUTTON).click()

    def is_login_successful(self):
        try:
            # This button is visible in screenshot after login
            self.driver.find_element(By.XPATH, "//button[contains(text(), 'Expand Cluster')]")
            return True
        except NoSuchElementException:
            return False
