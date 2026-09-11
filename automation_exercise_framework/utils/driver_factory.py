from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from config import config


def get_driver():
    if config.BROWSER == "firefox":
        options = FirefoxOptions()
        if config.HEADLESS:
            options.add_argument("--headless")
        driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()), options=options
        )
    else:
        options = ChromeOptions()
        if config.HEADLESS:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()), options=options
        )

    driver.implicitly_wait(config.IMPLICIT_WAIT)
    return driver
