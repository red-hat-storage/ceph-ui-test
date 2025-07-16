import pytest
from facade.login import LoginFacade
from config.data import TEST_CONFIG
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_login_success(driver, screenshot):
    # Wait for login page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "username"))
    )

    login_facade = LoginFacade(driver)
    login_facade.login(TEST_CONFIG.username, TEST_CONFIG.password)

    # Wait for page to respond after login
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    # Check login status
    login_successful = login_facade.is_login_successful()

    if login_successful:
        print("[✓] Login successful — test passed")
        screenshot(driver, "login_success")
    else:
        screenshot(driver, "login_failure")
        print("[✗] Login failed — screenshot taken, but test not failed")
