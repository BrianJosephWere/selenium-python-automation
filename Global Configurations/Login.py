from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Initialize WebDriver
driver = webdriver.Firefox()
driver.set_page_load_timeout(60)

# Open the page
driver.get('https://69.62.113.171:8086/#/auth/login')
driver.maximize_window()

# Enter credentials
driver.find_element(By.ID, 'mat-input-0').send_keys('Brian1')
driver.find_element(By.ID, 'mat-input-1').send_keys('Admin!23')

# Example of clicking the login button (adjust selector if needed)
driver.find_element(By.XPATH, "//button[contains(span, 'Login')]").click()

time.sleep(4)
driver.quit()
