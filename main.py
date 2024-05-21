import logging
import os
import time

import schedule
from dotenv import find_dotenv, load_dotenv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

LOGIN_URL = os.environ.get("LOGIN_URL")
USERNAME1 = os.environ.get("USERNAME1")
USERNAME2 = os.environ.get("USERNAME2")
PASSWORD = os.environ.get("PASSWORD")
RESUME_URL = os.environ.get("RESUME_URL")

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

WAIT_TIME = 10


def setup_driver():
    """Setup and return the Chrome WebDriver."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    return driver


def login(driver, username, password):
    """Log into the website."""
    driver.get(LOGIN_URL)
    WebDriverWait(driver, WAIT_TIME).until(EC.presence_of_element_located((By.ID, "otp-username"))).send_keys(username)
    time.sleep(4)

    WebDriverWait(driver, WAIT_TIME).until(
        EC.presence_of_element_located((By.XPATH, "//input[starts-with(@id, 'santa-input-') and @type='password']"))
    ).send_keys(password)
    time.sleep(4)

    WebDriverWait(driver, WAIT_TIME).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Увійти') or contains(., 'Войти')]"))
    ).click()
    time.sleep(4)


def click_resume_button(driver):
    """Navigate to the resume page and click the button to raise the resume."""
    driver.get(RESUME_URL)
    WebDriverWait(driver, WAIT_TIME).until(EC.url_contains("/my/resumes"))
    time.sleep(4)

    button = WebDriverWait(driver, WAIT_TIME).until(
        EC.presence_of_element_located(
            (By.XPATH, "//button[contains(., 'Поднять в поиске') or contains(., 'Підняти в пошуку')]")
        )
    )
    button.click()
    WebDriverWait(driver, WAIT_TIME).until(EC.staleness_of(button))


def press_button(username, password):
    """Perform the entire login and button click process for a given username."""
    driver = setup_driver()
    try:
        login(driver, username, password)
        click_resume_button(driver)
        logging.info(f"Process completed for {username}.")
    except TimeoutException as e:
        logging.error(f"TimeoutException for {username}: {e}")
    except NoSuchElementException as e:
        logging.error(f"NoSuchElementException for {username}: {e}")
    except Exception as e:
        logging.error(f"Unexpected error for {username}: {e}")
    finally:
        driver.quit()


def main():
    press_button(USERNAME1, PASSWORD)
    press_button(USERNAME2, PASSWORD)


if __name__ == "__main__":
    schedule.every().day.at("08:00").do(main)
    schedule.every().day.at("10:00").do(main)
    schedule.every().day.at("12:00").do(main)
    schedule.every().day.at("14:00").do(main)
    schedule.every().day.at("16:00").do(main)
    schedule.every().day.at("18:00").do(main)

    while True:
        schedule.run_pending()
        time.sleep(1)
