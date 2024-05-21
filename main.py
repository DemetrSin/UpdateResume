import os
import time

import schedule
from dotenv import find_dotenv, load_dotenv
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

ENV_FILE = find_dotenv()

if ENV_FILE:
    load_dotenv(ENV_FILE)


LOGIN_URL = os.environ.get('LOGIN_URL')
USERNAME = os.environ.get('USERNAME')
PASSWORD = os.environ.get('PASSWORD')
RESUME_URL = os.environ.get('RESUME_URL')


with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install())) as driver:

    try:
        driver.get(LOGIN_URL)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'otp-username'))
        ).send_keys(USERNAME)
        time.sleep(4)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[starts-with(@id, 'santa-input-') and @type='password']"))
        ).send_keys(PASSWORD)
        time.sleep(5)

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Увійти')]"))
        ).click()

        time.sleep(5)
        driver.get(RESUME_URL)

        WebDriverWait(driver, 10).until(
            EC.url_contains('/my/resumes')
        )

        button = WebDriverWait(driver, 0).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[contains(., 'Поднять в поиске') or contains(., 'Підняти в пошуку')]"))
        )
        button.click()

        WebDriverWait(driver, 10).until(
            EC.staleness_of(button)
        )
        time.sleep(5)
    except TimeoutException:
        print('Fine')
