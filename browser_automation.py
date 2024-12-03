import time
import os
import sys 
import csv

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from dotenv import load_dotenv

load_dotenv('.env')
FIREFOX_PROFILE_PATH = os.getenv('FIREFOX_PROFILE_PATH')

def main():

    if len(sys.argv) < 2:
        print("Usage: python browser_automation.py <path_to_csv>")
        sys.exit(1)

    csv_path = sys.argv[1] 
    driver = get_firefox_with_profile()

    driver.get("https://www.chess.com/login_and_go?returnUrl=https://www.chess.com/")

    input("Press Enter to continue...")

    with open(csv_path, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)

        for row in csv_reader:
            url = row[1]
            driver.get(url)
            time.sleep(5)
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')

            brilliants = soup.find_all(class_='analysis-brilliant')
            brilliant_count = 0
            for brilliant in brilliants:
                brilliant_count += int(brilliant.text) 
            
            if brilliant_count > 0:
                print(f"Found {brilliant_count} brilliant moves on: {url}")
                with open('valid_brilliant_games.csv', 'a') as file:
                    csv_writer = csv.writer(file)
                    csv_writer.writerow(row)
                

def get_firefox_with_profile():
    options = Options()
   
    # Set the profile directory in Firefox options
    options.set_preference('profile', FIREFOX_PROFILE_PATH)
    
    # Prevent Firefox from creating a new profile
    options.set_preference("browser.cache.disk.enable", True)
    options.set_preference("browser.cache.memory.enable", True)
    options.set_preference("browser.cache.offline.enable", True)
    options.set_preference("network.cookie.cookieBehavior", 0)
    
    # Initialize the driver with the specified profile
    driver = webdriver.Firefox(options=options)
    return driver


if __name__ == "__main__":
    main()
