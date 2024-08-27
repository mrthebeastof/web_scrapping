from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from openpyxl import Workbook
import time
import random


chrome_options = Options()
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")


chrome_driver_path = 'C:/WebDrivers/chromedriver.exe'  


service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)


def scrape_data(url):
    try:
        driver.get(url)
        
        # Example 
        title = driver.title
        first_heading = driver.find_element(By.TAG_NAME, 'h1').text if driver.find_elements(By.TAG_NAME, 'h1') else 'No H1 Heading'
        description = driver.find_element(By.NAME, 'description').get_attribute('content') if driver.find_elements(By.NAME, 'description') else 'No Description'
        image_src = driver.find_element(By.TAG_NAME, 'img').get_attribute('src') if driver.find_elements(By.TAG_NAME, 'img') else 'No Image'

        return [url, title, first_heading, description, image_src]
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return [url, 'Error', 'Error', 'Error', 'Error']

# List of URLs
urls = [
    'https://example.com',
    'https://anotherexample.com',
    
]

# Create a new Excel workbook 
wb = Workbook()
ws = wb.active
ws.title = "Scraped Data"

# Write the headers
ws.append(['URL', 'Title', 'H1 Heading', 'Description', 'Image URL'])

# Execution limiter settings
MAX_SCRAPES_PER_HOUR = 10
scrapes_count = 0
start_time = time.time()

for url in urls:
    if scrapes_count >= MAX_SCRAPES_PER_HOUR:
        elapsed_time = time.time() - start_time
        if elapsed_time < 3600:  # 3600 seconds = 1 hour
            time_to_wait = 3600 - elapsed_time
            print(f"Reached limit. Waiting for {time_to_wait/60:.2f} minutes.")
            time.sleep(time_to_wait)
        scrapes_count = 0
        start_time = time.time()

    data = scrape_data(url)
    ws.append(data)
    time.sleep(random.uniform(1, 5))
    scrapes_count += 1


wb.save('scraped_data_selenium.xlsx')
driver.quit()

print("Scraping completed. Data saved to 'scraped_data_selenium.xlsx'.")
