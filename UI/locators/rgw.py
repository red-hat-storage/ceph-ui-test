from selenium.webdriver.common.by import By

class RGWLocators:
    ADMINISTRATION_MENU = (By.XPATH, "//span[text()='Administration']")
    SERVICES_MENU = (By.XPATH, "//span[text()='Services']")

    RGW_ROW = (By.XPATH, "//tr[td[contains(text(),'rgw.shared')]]")
    RGW_EXPAND_BUTTON = (
        By.XPATH,
        "//tr[td[contains(text(), 'rgw.shared.sec.')]]//button[contains(@aria-label, 'Expand row')]"
    )

    SERVICE_DETAILS_CONTAINER = (By.XPATH, "//cd-service-details")

    DAEMON_TABLE = (
        By.XPATH,
        "//cd-service-details//cd-service-daemon-list[contains(@class, 'cd-service-daemon-list')]"
    )

    DAEMON_ROW = (
        By.XPATH,
        "//cd-service-details//cd-service-daemon-list//table//tbody/tr"
    )

    DAEMON_STATUS_RUNNING = (
    By.XPATH,
    "//cd-service-details//cd-service-daemon-list//table//tbody//tr/td[contains(., 'running')]"
)

