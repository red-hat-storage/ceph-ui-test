from selenium.webdriver.common.by import By


class RBDLocators:
    BLOCK_DROPDOWN = (By.XPATH, "//span[normalize-space(.)='Block']")
    IMAGES         = (By.XPATH, "//span[normalize-space(.)='Images']")

    # Click the button, not its inner <span>
    CREATE_IMAGE_BUTTON = (
        By.XPATH,
        "//button[@data-testid='primary-action' and contains(@aria-label,'Create')]",
    )

    IMAGE_NAME_INPUT = (By.XPATH, "//input[@id='name'  and @placeholder='Name...']")
    IMAGE_SIZE_INPUT = (By.XPATH, "//input[@id='size'  and @placeholder='e.g., 10GiB']")
    CREATE_BUTTON    = (By.XPATH, "//button[@type='submit' and contains(@aria-label,'Create Image')]")

