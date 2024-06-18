import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


# Load environment variables from a.env file
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(env_path)
url = os.getenv('url')
driver = webdriver.Chrome()


def clock_in() -> None:
    """
    This function is used to clock in to work.

    Parameters:
    None

    Returns:
    None

    """
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.NAME, "Bci"))
    )
    clk_in_btn = driver.find_element(By.NAME, "Bci")
    clk_in_btn.click()

def clock_out() -> None:
    """
    This function is used to clock out of work.

    Parameters:
    None

    Returns:
    None

    """
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "Bco"))
    )
    clk_out_btn = driver.find_element(By.NAME, "Bco")
    clk_out_btn.click()

def main() -> None:
    """
    This function is the main entry point of the code. It is responsible for
    starting the bot and running it in an infinite loop.

    Parameters:
        None

    Returns:
        None

    """
    current_time = time.localtime()
    clock_in_condition = (current_time.tm_wday < 5) and (current_time.tm_hour == 18) and (current_time.tm_min == 0)
    clock_out_condition = (current_time.tm_wday == 4) and (current_time.tm_hour == 21) and (current_time.tm_min == 0)

    try:
        driver.get(url)
        WebDriverWait(driver, 20)
        print("loading page...", url)
        if clock_in_condition:
            clock_in()
        elif clock_out_condition:
            clock_out()
        else:
            print("No changes made to the timesheet")
        driver.close()
    
    finally:
        driver.quit()

if __name__ == "__main__":
    main()

