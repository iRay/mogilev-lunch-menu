from PIL import Image
from io import BytesIO
from selenium import webdriver


def init_driver() -> webdriver:
    """
    Selenium driver initialization
    :return:
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.headless = True
    # driver = webdriver.Chrome(options=options)
    driver = webdriver.Chrome("/usr/local/bin/chromedriver", options=options)
    driver.set_window_size(1024, 768)
    return driver
