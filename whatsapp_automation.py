from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import random

def setup_driver():
    """Setup Chrome driver with stealth options"""
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver

def report_number_via_whatsapp(number, proxy=None):
    """
    Actual WhatsApp reporting automation
    Requires: ChromeDriver, logged-in WhatsApp Web
    """
    driver = setup_driver()
    
    try:
        # Open WhatsApp Web
        driver.get('https://web.whatsapp.com/')
        
        # Wait for QR scan (manual step - you need to scan once)
        input("Scan QR code and press Enter...")
        
        # Search for the number
        search_box = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
        )
        search_box.click()
        search_box.send_keys(number)
        time.sleep(2)
        
        # Click on the chat
        chat = driver.find_element(By.XPATH, f'//span[@title="{number}"]')
        chat.click()
        time.sleep(1)
        
        # Click menu (three dots)
        menu_button = driver.find_element(By.XPATH, '//div[@data-testid="menu"]')
        menu_button.click()
        time.sleep(1)
        
        # Click Report
        report_option = driver.find_element(By.XPATH, '//div[text()="Report"]')
        report_option.click()
        time.sleep(1)
        
        # Select reason and submit
        spam_option = driver.find_element(By.XPATH, '//div[text()="Spam"]')
        spam_option.click()
        time.sleep(1)
        
        submit_button = driver.find_element(By.XPATH, '//div[@data-testid="popup-controls-ok"]')
        submit_button.click()
        time.sleep(2)
        
        print(f"Successfully reported {number}")
        return True
        
    except Exception as e:
        print(f"Error reporting {number}: {e}")
        return False
    finally:
        driver.quit()

# Mass reporting function
def mass_report(number, count=50):
    successful = 0
    for i in range(count):
        print(f"Report {i+1}/{count} for {number}")
        if report_number_via_whatsapp(number):
            successful += 1
        time.sleep(random.uniform(5, 15))  # Avoid rate limiting
    return successful
