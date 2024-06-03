from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize WebDriver (Make sure to specify the path to your WebDriver)
driver = webdriver.Chrome()

try:
    # Navigate to the login page
    driver.get("https://www.mexc.com/login")
    
    # Click on the button to choose phone login
    choose_phone_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[3]/div[2]/div/div[1]/div[2]/div[2]'))
    )
    choose_phone_btn.click()
    
    # Click to choose the region
    choose_region_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="login"]/div[1]/div/div/div/div/div/div/div/div[1]'))
    )
    choose_region_btn.click()

    # choose_cam_region_btn = WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, '/html/body/div[7]/div/div[2]/div/div[2]/div/div/div[2]/div/div[1]/form/div[1]/div/div/div/div/div/div/div/div[2]/div[1]/input'))
    # )
    # choose_cam_region_btn.click()
    # choose_cam_region_btn.send_keys('Cambodia')
    # Additional steps can be added here as needed...
    
    choose_region_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[7]/div/div[2]/div/div[2]/div/div/div[2]/div/div[1]/form/div[1]/div/div/div/div/div/div/div/div[2]/div[3]/dl[2]/dd[33]'))
        )
    choose_region_btn.click()
finally:
    # Close the driver
    driver.quit()
