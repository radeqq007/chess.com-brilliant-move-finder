import time
import os
import sys 
import csv

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from dotenv import load_dotenv

load_dotenv('.env')
FIREFOX_PROFILE_PATH = os.getenv('FIREFOX_PROFILE_PATH')

def main():

    if len(sys.argv) < 2:
        print("Usage: python browser_automation.py <path_to_csv>")
        sys.exit(1)

    csv_path = sys.argv[1] 
    driver = get_firefox_with_profile()

    # let the user login 

    driver.get("https://www.chess.com/login_and_go?returnUrl=https://www.chess.com/")

    input("Press Enter to continue...")

    with open(csv_path, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)

        for row in csv_reader:
            url = row[1]
            print(f"Visiting {url}")
            driver.get(url)

            # wait for the page to load
            time.sleep(5)
            # get the page source

            page_source = driver.page_source

            # parse the page source

            soup = BeautifulSoup(page_source, 'html.parser')

            # find elments with class 'analysis-brilliant'
            brilliants = soup.find_all(class_='analysis-brilliant')
            brilliant_count = 0
            for brilliant in brilliants:
                brilliant_count += int(brilliant.text) 
            
            if brilliant_count > 0:
                print(f"Found {brilliant_count} brilliant moves on: {url}")
                with open('valid_brilliant_games.csv', 'a') as file:
                    csv_writer = csv.writer(file)
                    csv_writer.writerow(row)
                



def get_firefox_with_profile(profile_name='default-release'):
    """
    Initialize Firefox WebDriver with an existing profile.
    
    Args:
        profile_name (str): Name of the Firefox profile to use (default is 'default-release')
                          You can find your profile names by visiting 'about:profiles' in Firefox
    
    Returns:
        WebDriver: Selenium WebDriver instance with the specified profile
    """
    options = Options()
   
    profile_dir = FIREFOX_PROFILE_PATH 
    
    # Set the profile directory in Firefox options
    options.set_preference('profile', profile_dir)
    
    # Prevent Firefox from creating a new profile
    options.set_preference("browser.cache.disk.enable", True)
    options.set_preference("browser.cache.memory.enable", True)
    options.set_preference("browser.cache.offline.enable", True)
    options.set_preference("network.cookie.cookieBehavior", 0)
    
    # Initialize the driver with the specified profile
    driver = webdriver.Firefox(options=options)
    return driver

# Example usage
if __name__ == "__main__":
    main()
