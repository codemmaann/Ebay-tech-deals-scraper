from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
from datetime import datetime
import os

def setup_driver():
    """Set up Chrome driver with headless option"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=chrome_options)

def scroll_to_bottom(driver):
    """Scroll to bottom of page to load all products"""
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        if new_height == last_height:
            break
        last_height = new_height

def extract_product_data(driver):
    """Extract product data from the page"""
    products = []
    
    # Wait for products to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='item']"))
    )
    
    product_elements = driver.find_elements(By.CSS_SELECTOR, "[data-testid='item']")
    
    for product in product_elements:
        try:
            # Extract title
            title_element = product.find_element(By.CSS_SELECTOR, "[data-testid='item-title']")
            title = title_element.text.strip()
            
            # Extract current price
            price_element = product.find_element(By.CSS_SELECTOR, "[data-testid='s-item-price']")
            price = price_element.text.strip()
            
            # Extract original price (if available)
            try:
                original_price_element = product.find_element(By.CSS_SELECTOR, "[data-testid='strikethrough-price']")
                original_price = original_price_element.text.strip()
            except:
                original_price = "N/A"
            
            # Extract shipping info
            try:
                shipping_element = product.find_element(By.CSS_SELECTOR, "[data-testid='item-shipping']")
                shipping = shipping_element.text.strip()
            except:
                shipping = "N/A"
            
            # Extract product URL
            url_element = product.find_element(By.CSS_SELECTOR, "a[data-testid='item-title']")
            item_url = url_element.get_attribute("href")
            
            products.append({
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'title': title,
                'price': price,
                'original_price': original_price,
                'shipping': shipping,
                'item_url': item_url
            })
            
        except Exception as e:
            print(f"Error extracting product: {e}")
            continue
    
    return products

def main():
    driver = setup_driver()
    
    try:
        print("Starting eBay scraping...")
        driver.get("https://www.ebay.com/globaldeals/tech")
        time.sleep(3)
        
        print("Scrolling to load all products...")
        scroll_to_bottom(driver)
        
        print("Extracting product data...")
        products = extract_product_data(driver)
        
        print(f"Found {len(products)} products")
        
        # Save to CSV
        df = pd.DataFrame(products)
        file_exists = os.path.exists('ebay_tech_deals.csv')
        
        if file_exists:
            df.to_csv('ebay_tech_deals.csv', mode='a', header=False, index=False)
        else:
            df.to_csv('ebay_tech_deals.csv', index=False)
            
        print("Data saved successfully!")
        
    except Exception as e:
        print(f"Error during scraping: {e}")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    main()