from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginFacade:
    def __init__(self, driver):
        self.driver = driver

    def login(self, username, password):

        self.driver.find_element(By.ID, "username").send_keys(username)
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.XPATH, "//input[@type='submit' and @value='Log in']").click()

    def is_login_successful(self):
        try:
            # Wait for the "Dashboard" sidebar item to appear (visible only post-login)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//span[text()='Dashboard']"))
            )
            return True
        except (NoSuchElementException, TimeoutException):
            return False
