import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from getDriverByID import getDriver
import time

class Newfeed:

    def _like(self, driver):
        like_icon_xpath = '//*[@data-e2e="like-icon"]'
        like_icon = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, like_icon_xpath))
        )
        like_icon.click()

    def _share(self, driver):
        share_icon_xpath = '//*[@data-e2e="share-icon"]'
        share_icon = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, share_icon_xpath))
        )
        share_icon.click()

    def _follow(self, driver):
        follow_icon_xpath = '//*[@data-e2e="feed-follow"]'
        follow_icon = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, follow_icon_xpath))
        )
        follow_icon.click()


    def tiktok_newsfeed_interaction(self):
        driver = getDriver()
        driver.get('https://www.tiktok.com')
        
        time.sleep(10)

        actions = [self._like, self._share, self._follow]
        num_actions = random.randint(5, 15) 
        for _ in range(num_actions):
            action = random.choice(actions)
            try:
                action(driver)
                time.sleep(random.uniform(1, 5))
            except Exception as e:
                print(f"An error occurred: {e}")

        driver.quit()

if __name__ == "__main__":
    a = Newfeed()
    a.tiktok_newsfeed_interaction()
