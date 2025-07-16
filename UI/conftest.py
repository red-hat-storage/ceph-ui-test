import os
import pytest
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from config.data import TEST_CONFIG

@pytest.fixture(scope="function")
def driver(request):
    browser = os.getenv("browser", "chrome").lower()
    hub_host = os.getenv("hub_host", "localhost")
    dashboard_url = os.getenv("dashboard_url", TEST_CONFIG.url)

    if browser == "chrome":
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("disable-infobars")
        chrome_options.add_argument("enable-automation")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.accept_insecure_certs = True

        wdriver = webdriver.Remote(
            command_executor=f"http://{hub_host}:4444/wd/hub",
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

    wdriver.maximize_window()
    wdriver.set_page_load_timeout(50)
    wdriver.implicitly_wait(10)
    wdriver.set_script_timeout(10)

    wdriver.get(dashboard_url)

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

