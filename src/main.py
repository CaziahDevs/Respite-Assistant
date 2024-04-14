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
username = os.getenv('username')
password = os.getenv('password')
url = os.getenv('url')

driver = webdriver.Chrome()


def login() -> None:
    """
    This function is used to login to the company's website.

    Parameters:
    driver (WebDriver): The WebDriver instance used to interact with the page.

    Returns:
    None

    """
    driver.get(url)
    WebDriverWait(driver, 5)
    # Add code to fill in username and password fields
    username_input = driver.find_element(By.NAME, "lo_uname")
    username_input.send_keys(username)
    password_input = driver.find_element(By.NAME, "lo_pw")
    password_input.send_keys(password, Keys.ENTER)
    WebDriverWait(driver, 5)

def naviagate_to_clock() -> None:
    """
    This function is used to navigate to the clock in/out page.

    Parameters:
    driver (WebDriver): The WebDriver instance used to interact with the page.

    Returns:
    None

    """
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(
            (By.PARTIAL_LINK_TEXT, "Clock In/Out"))
    )
    # Click on the "Clock In" button
    link = driver.find_element(By.PARTIAL_LINK_TEXT, "Clock In/Out")
    link.click()
    time.sleep(5)

def clock_in_out(in_or_out: bool) -> None:
    """
    This function is used to clock in or out of work.

    Parameters:
    in_or_out (bool): A boolean value indicating whether to clock in or out.

    Returns:
    None

    """
    naviagate_to_clock()

    if in_or_out:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.NAME, "Bci"))
        )
        clk_in_btn = driver.find_element(By.NAME, "Bci")
        clk_in_btn.click()
    else:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "Bco"))
        )
        clk_out_btn = driver.find_element(By.NAME, "Bco")
        clk_out_btn.click()
        # driver.send_keys(Keys.ENTER)
        # driver.send_keys(Keys.ENTER)



# Function to check if the current time requires a clock_in or clock_out
def run_bot() -> None:
    """
    This function is used to run the bot. It checks if it is a weekday and the current time is between 6pm and 9pm (or 9:45pm on Fridays). If it is, it attempts to clock in or out of work.

    Parameters:
        None

    Returns:
        None

    """
    current_time = time.localtime()
    #Weekday between 6pm and 9pm
    option1 = current_time.tm_wday < 5 and 18 <= current_time.tm_hour < 21
    #Friday at 9:45pm
    option2 = current_time.tm_wday == 4 and current_time.tm_hour == 21 and current_time.tm_min == 45

    if option1 or option2:
        login()
        clock_in_out(True) if current_time.tm_hour == 18 and current_time.tm_min == 0 else clock_in_out(False)



def main() -> None:
    """
    This function is the main entry point of the code. It is responsible for
    starting the bot and running it in an infinite loop.

    Parameters:
        None

    Returns:
        None

    """
    run_bot()

if __name__ == "__main__":
    main()
