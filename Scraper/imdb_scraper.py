from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import random

import time

def get_imdb_rating(title, release_year):
    chrome_options = Options()
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    driver = webdriver.Chrome(options=chrome_options)
    url = f'https://www.imdb.com/find/?q={title,release_year}&ref_=nv_sr_sm'
    driver.get(url)
    time.sleep(random.uniform(2, 5))  # Wait for the page to load
    
    try:
        title_button = driver.find_element(By.LINK_TEXT, title)
        print('titlE', title_button.text)
        year = driver.find_element(By.XPATH("//span[@class='ipc-metadata-list-summary-item__li']").text)
        if release_year in year:
            title_button.click()
        print("Button clicked successfully")
        
        rating = driver.find_element(By.XPATH, '(//span[@class="sc-eb51e184-1 ljxVSS"])[1]').text


        print(f"IMDb Rating for {title}: {rating}")
    except Exception as e:
        print(f"Failed to retrieve IMDb rating: {e}")
        rating = 'N/A'
    finally:
        driver.close() 
        driver.quit()
    return rating

# Example Usage
imdb_id = 'The Misfits'  # IMDb ID for Inception
rating = get_imdb_rating(imdb_id,"2021")
print(f"Inception's IMDb Rating: {rating}")