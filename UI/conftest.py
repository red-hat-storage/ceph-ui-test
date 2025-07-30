import os
import pytest
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from UI.config.data import TEST_CONFIG
from UI.facade.login import LoginFacade

@pytest.fixture(scope="function")
def driver(request):
    browser = os.getenv("browser", "chrome").lower()
    hub_host = os.getenv("hub_host", "localhost")
    dashboard_url = os.getenv("dashboard_url", TEST_CONFIG.url)

    # Setup browser options
    if browser == "chrome":
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("disable-infobars")
        chrome_options.add_argument("enable-automation")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.accept_insecure_certs = True


        try:
            wdriver = webdriver.Remote(
                command_executor=f"http://{hub_host}:4444/wd/hub",
                options=chrome_options
            )
        except Exception:
            print(f"[⚠️] Failed to connect to {hub_host}, retrying with host.docker.internal...")
            wdriver = webdriver.Remote(
                command_executor="http://host.docker.internal:4444/wd/hub",
                options=chrome_options
            )

    elif browser == "firefox":
        firefox_options = FirefoxOptions()
        firefox_options.add_argument("--headless")
        firefox_options.add_argument("--no-sandbox")
        firefox_options.accept_insecure_certs = True

        wdriver = webdriver.Remote(
            command_executor=f"http://{hub_host}:4444/wd/hub",
            options=firefox_options
        )

    else:
        raise ValueError(f"Unsupported browser: {browser}")

    # Browser configuration
    wdriver.maximize_window()
    wdriver.set_page_load_timeout(50)
    wdriver.implicitly_wait(10)
    wdriver.set_script_timeout(10)

    # Visit Ceph dashboard and perform login
    wdriver.get(dashboard_url)

    login_facade = LoginFacade(wdriver)
    login_facade.login(TEST_CONFIG.username, TEST_CONFIG.password)

    # Login verification using the "Administration" menu label
    try:
        WebDriverWait(wdriver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//span[text()='Administration']"))
        )
    except Exception:
        os.makedirs("screenshots", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"screenshots/login_failed_{timestamp}.png"
        wdriver.save_screenshot(screenshot_path)
        print(f"[❌] Login failed. Screenshot saved to {screenshot_path}")
        wdriver.quit()
        raise Exception("Login failed.")

    yield wdriver
    wdriver.quit()

@pytest.fixture
def screenshot():
    def take_screenshot(driver, name=None):
        os.makedirs("screenshots", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name or 'screenshot'}_{timestamp}.png"
        path = os.path.join("screenshots", filename)
        try:
            driver.save_screenshot(path)
            print(f"[📸] Screenshot saved at: {path}")
        except Exception as e:
            print(f"[❌] Failed to capture screenshot: {e}")
        return path
    return take_screenshot

