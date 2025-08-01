import logging
import time

from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

logger: logging.Logger = logging.getLogger(__name__)


def make_driver(debug=False):
    options = Options()
    options.page_load_strategy = 'eager'
    # options.add_argument("--disable-images")
    if not debug:
        options.add_argument("--headless")
    return webdriver.Firefox(options=options)


def get_element_by_xpath(
        driver: Firefox,
        xpath: str,
) -> WebElement:
    elem = driver.find_element(by=By.XPATH, value=xpath)
    return elem



def wait_element_by_xpath(
        driver: Firefox,
        xpath: str,
) -> WebElement:
    logger.debug(f'wait_element_by_xpath start {xpath=}')
    for attempt_number in range(1, 6):
        try:
            elem = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            logger.debug(f"it's ALIVE {attempt_number=} {elem.id=} {elem.get_attribute('innerHTML')=}")
            return elem
        except StaleElementReferenceException as e:
            logger.debug(f"it's NOT ALIVE {attempt_number=} {e=}")
            time.sleep(1)
    raise Exception("it's NOT ALIVE")
