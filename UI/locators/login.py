from selenium.webdriver.common.by import By

class Login:
    USERNAME = (By.ID, "username")
    PASSWORD = (By.ID, "password")  
    LOGIN_BUTTON = (By.XPATH, "//input[@type='submit' and @value='Log in']")
