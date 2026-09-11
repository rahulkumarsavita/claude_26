from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from config import config


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, config.EXPLICIT_WAIT_TIMEOUT)

    def open(self, url):
        self.driver.get(url)

    def find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_all(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def click(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def type_text(self, locator, text, clear_first=True):
        element = self.find(locator)
        if clear_first:
            element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        return self.find(locator).text.strip()

    def is_displayed(self, locator, timeout=None):
        wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        try:
            return wait.until(EC.visibility_of_element_located(locator)).is_displayed()
        except Exception:
            return False

    def wait_until_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_until_invisible(self, locator):
        return self.wait.until(EC.invisibility_of_element_located(locator))

    def hover(self, element_or_locator):
        element = (
            element_or_locator
            if hasattr(element_or_locator, "click")
            else self.find(element_or_locator)
        )
        ActionChains(self.driver).move_to_element(element).perform()
