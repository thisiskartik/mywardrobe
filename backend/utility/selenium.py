import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyvirtualdisplay import Display
from dotenv import load_dotenv

load_dotenv()


def get_driver():
    options = webdriver.ChromeOptions()
    if os.environ.get('DEBUG_MODE') == 'True':
        options.add_experimental_option("detach", True)
    else:
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        display = Display(visible=False, size=(1280, 720))
        display.start()
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    return driver


def get_element(driver, selector_type, selector, wait_type=EC.visibility_of_element_located, time=2, many=False):
    elem = WebDriverWait(driver, time).until(wait_type((selector_type, selector)))
    if many:
        return driver.find_elements(selector_type, selector)
    else:
        return elem
