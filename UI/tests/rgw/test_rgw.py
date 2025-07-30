import pytest
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators.rgw import RGWLocators


@pytest.mark.rgw
def test_rgw_page_load_and_elements(driver, screenshot):
    try:
        # Step 1: Go to Administration > Services
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(RGWLocators.ADMINISTRATION_MENU)
        ).click()

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(RGWLocators.SERVICES_MENU)
        ).click()

        # Step 2: Find and expand RGW row
        rgw_row = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(RGWLocators.RGW_ROW)
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", rgw_row)

        expand_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(RGWLocators.RGW_EXPAND_BUTTON)
        )
        expand_btn.click()
        time.sleep(1)  # Allow animation

        # Step 3: Check if daemon rows are present
        daemon_rows = WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located(RGWLocators.DAEMON_ROW)
        )
        assert len(daemon_rows) > 0, "❌ No daemon entries found"

        # Step 4: Check for at least one daemon in running state
        running_status = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(RGWLocators.DAEMON_STATUS_RUNNING)
        )
        assert running_status.is_displayed(), "❌ No daemon is in running state"

        print("✅ RGW test passed: Daemons are present and at least one is running.")

    except Exception as e:
        screenshot(driver, "rgw_failure")
        pytest.fail(f"❌ RGW test failed: {e}")
