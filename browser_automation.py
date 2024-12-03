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
    driver = None
    
    try:
        driver = get_firefox_with_profile()
        
        # Test if we're already logged in
        driver.get("https://www.chess.com/home")
        time.sleep(3) 
        
        if "login" in driver.current_url.lower():
            print("Login required!")
            input("Press Enter once you're logged in...")
        
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
                
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if driver:
            driver.quit()


def get_firefox_with_profile():
    options = Options()
    
    # Set the profile directory
    options.add_argument('-profile')
    options.add_argument(FIREFOX_PROFILE_PATH)
    
    # Disable automation flags
    options.set_preference('dom.webdriver.enabled', False)
    options.set_preference('useAutomationExtension', False)
    
    # options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0")
    options.set_preference("privacy.resistFingerprinting", False)
    options.set_preference("webdriver.load.strategy", "normal")
    
    service = Service(log_path=os.path.devnull)

    driver = webdriver.Firefox(
        options=options,
        service=service
    )
    
    return driver

if __name__ == "__main__":
    main()