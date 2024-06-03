import json
import requests
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from pywinauto.keyboard import send_keys
from selenium.webdriver.common.keys import Keys

class PostVideo:
    def read_path_video(self):
        path_file = '../data/video_des.json'
        try:
            with open(path_file, 'r') as f:
                data = json.load(f)
            videos = data.get('video', [])
            return videos
        except FileNotFoundError:
            print(f"File not found: {path_file}")
            return []
        except Exception as e:
            print(f"An error occurred while reading the JSON file: {e}")
            return []

    def read_id_profile(self):
        path_file = '../data/id_profile.txt'
        try:
            with open(path_file, 'r') as f:
                id_profile = f.read().strip()
            return id_profile
        except FileNotFoundError:
            print(f"File not found: {path_file}")
            return None
        except Exception as e:
            print(f"An error occurred while reading the profile ID: {e}")
            return None

    def getDriver(self, id_profile):
        if not id_profile:
            print("Profile ID is None")
            return None

        urlStart = 'http://127.0.0.1:19995/api/v3/profiles/start/'
        urlGetProfile = f'{urlStart}{id_profile}?win_scale=0.8&win_pos=300,300'

        try:
            response = requests.get(urlGetProfile)
            response.raise_for_status()  # Raise an error for bad status codes
            response_data = response.json()

            if response_data.get('success') and response_data['data'].get('remote_debugging_address'):
                remote_debugging_address = response_data['data']['remote_debugging_address']
                driver_path = response_data['data']['driver_path']
                print(f"Remote debugging address: {remote_debugging_address}")
                print(f"Driver path: {driver_path}")
            else:
                print("Failed to get remote debugging address or driver path")
                return None
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while making the request: {e}")
            return None
        except ValueError as e:
            print(f"An error occurred while parsing the response: {e}")
            return None

        try:
            options = Options()
            options.add_experimental_option("debuggerAddress", remote_debugging_address)
            service = Service(executable_path=driver_path)
            driver = webdriver.Chrome(service=service, options=options)
            return driver
        except Exception as e:
            print(f"An error occurred while initializing the WebDriver: {e}")
            return None

    def postVideo(self):
        id_profile = self.read_id_profile()
        if not id_profile:
            print("No profile ID available")
            return

        driver = self.getDriver(id_profile)
        if driver is None:
            print("Failed to initialize WebDriver")
            return

        try:
            videos = self.read_path_video()
            if not videos:
                print("No videos found in the JSON file")
                return

            # Randomly select a video and description
            video = random.choice(videos)
            path = video.get('path')
            description = video.get('description')

            driver.get('https://www.tiktok.com/tiktokstudio/upload?from=upload')

            iframe_xpath = '//*[@id="root"]/div/div[2]/div[2]/div/div/iframe'
            iframe = WebDriverWait(driver, 10).until(
                EC.frame_to_be_available_and_switch_to_it((By.XPATH, iframe_xpath))
            )

            aria_label_xpath = '//*[@aria-label="Chọn video"]'
            select_video_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, aria_label_xpath))
            )
            select_video_button.click()

            time.sleep(3)
            send_keys(path)
            send_keys("{ENTER}")

            time.sleep(3)
            xpath_hashtag = '//*[@id="root"]/div/div/div/div/div[2]/div[2]/div[1]/div/div[2]/div[1]/div/div/div'
            hashtag = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath_hashtag))
            )
            hashtag.click()
            hashtag.send_keys(Keys.CONTROL, 'a')
            hashtag.send_keys(Keys.DELETE)
            hashtag.send_keys(description)

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            postBtn_xpath = '//*[@id="root"]/div/div/div/div/div[2]/div[2]/div[9]/div[1]/button'
            postBtn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, postBtn_xpath))
            )
            postBtn.click()
            time.sleep(20)
        except Exception as e:
            print(f"An error occurred while posting the video: {e}")
        finally:
            driver.quit()

instance = PostVideo()
instance.postVideo()
