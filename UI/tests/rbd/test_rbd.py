import time
import pytest
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from UI.config.data import TEST_CONFIG
from UI.facade.login import LoginFacade
from UI.locators.rbd import RBDLocators


def _w(driver, t=10):
    return WebDriverWait(driver, t)


@pytest.mark.usefixtures("driver", "screenshot")
def test_rbd_create_image(driver, request, screenshot):
    name = request.config.getoption("--image-name")
    size = request.config.getoption("--image-size")

    try:
        # ── Dashboard & (optional) login ────────────────────────────────────
        driver.get(TEST_CONFIG.url)
        try:
            _w(driver, 5).until(EC.presence_of_element_located((By.ID, "username")))
            LoginFacade(driver).login(TEST_CONFIG.username, TEST_CONFIG.password)
        except TimeoutException:
            pass  # already logged in

        # ── Navigate Block ▸ Images ─────────────────────────────────────────
        driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            _w(driver).until(EC.presence_of_element_located(RBDLocators.BLOCK_DROPDOWN)),
        )
        _w(driver).until(EC.element_to_be_clickable(RBDLocators.BLOCK_DROPDOWN)).click()
        _w(driver).until(EC.element_to_be_clickable(RBDLocators.IMAGES)).click()

        # ── Click “Create” (with JS-fallback) ───────────────────────────────
        create_btn = _w(driver).until(
            EC.element_to_be_clickable(RBDLocators.CREATE_IMAGE_BUTTON)
        )
        try:
            create_btn.click()
        except ElementClickInterceptedException:
            driver.execute_script("arguments[0].click();", create_btn)

        # ── Fill form & submit ──────────────────────────────────────────────
        _w(driver).until(EC.presence_of_element_located(RBDLocators.IMAGE_NAME_INPUT)).send_keys(name)
        _w(driver).until(EC.presence_of_element_located(RBDLocators.IMAGE_SIZE_INPUT)).send_keys(size)
        _w(driver).until(EC.element_to_be_clickable(RBDLocators.CREATE_BUTTON)).click()

    except Exception as e:
        screenshot(driver, "rbd_failure")
        pytest.fail(f"❌ RBD test failed: {e}")
