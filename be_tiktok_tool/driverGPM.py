from PyQt6 import QtWidgets, QtGui, QtCore
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import json
import random
import string
import utils  # Import your utility functions or constants here
import time
class DriverManager:
    drivers = []

    @classmethod
    def add_driver(cls, driver):
        cls.drivers.append(driver)

    @classmethod
    def close_all_drivers(cls):
        for driver in cls.drivers[:]:  # Iterate over a copy of the list
            try:
                driver.close()
            except Exception as e:
                print(f"An error occurred while closing driver: {str(e)}")
        cls.drivers.clear()



class DriverGPM:
    driver: webdriver.Chrome
    profile_name: str
    profile_id: str

    def __init__(self, proxy, user_agent):
        self.driver = self.createProfileDriver(proxy=proxy, user_agent=user_agent)
        if self.driver:
            DriverManager.add_driver(self)

    def scroll_(self, scroll_distance: int):
        self.driver.execute_script(f"window.scrollBy(0, {scroll_distance});")

    def redirect(self, url: str):
        self.driver.get(url)

    def input_(self, xpath: str, content: str, timeout=10):
        input_text = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        input_text.click()
        input_text.clear()
        for char in content:
            input_text.send_keys(char)
            time.sleep(0.1)

    def click(self, xpath: str, timeout=10) -> bool:
        accept_btn = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        accept_btn.click()

    def get_current_url(self):
        return self.driver.current_url

    def close(self):
        self.driver.close()

    def generate_profile_name(self, length: int):
        if length < 8:
            length = 8
        characters = string.ascii_letters + string.digits
        profile_name = ''.join(random.choice(characters) for i in range(length))
        return profile_name

    def createProfileDriver(self, proxy, user_agent):
        random_length = random.randint(8, 20)
        self.profile_name = self.generate_profile_name(random_length)

        urlCreate = 'http://127.0.0.1:19995/api/v3/profiles/create'
        dataJson = {
            "profile_name": self.profile_name,
            "group_name": "All",
            "browser_core": "chromium",
            "browser_name": "Chrome",
            "browser_version": "119.0.6045.124",
            "is_random_browser_version": False,
            "raw_proxy": proxy,
            "startup_urls": "",
            "is_masked_font": True,
            "is_noise_canvas": False,
            "is_noise_webgl": False,
            "is_noise_client_rect": False,
            "is_noise_audio_context": True,
            "is_random_screen": False,
            "is_masked_webgl_data": True,
            "is_masked_media_device": True,
            "is_random_os": False,
            "os": "Windows 11",
            "webrtc_mode": 2,
            "user_agent": user_agent
        }
        headers = {
            'Content-Type': 'application/json'
        }

        try:
            response = requests.post(urlCreate, data=json.dumps(dataJson), headers=headers)
            response.raise_for_status()
            response_data = response.json()
            print("Profile created successfully")
            
            self.profile_id = response_data.get('data', {}).get('id')
            fileID_path = utils.PROFILE_ID_TXT
            with open(fileID_path, 'a') as f:
                f.write(str(self.profile_id) + '\n')

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

        urlStart = f'http://127.0.0.1:19995/api/v3/profiles/start/{self.profile_id}?win_scale=0.8&win_pos=200,200&win_size=1200,800'
        
        try:
            response = requests.get(urlStart)
            response_data = response.json()
            if response_data.get('success') and response_data['data'].get('remote_debugging_address'):
                remote_debugging_address = response_data['data']['remote_debugging_address']
                driver_path = response_data['data']['driver_path']
            else:
                return None
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

        options = Options()
        options.add_experimental_option("debuggerAddress", remote_debugging_address)
        service = Service(executable_path=driver_path)
        driver = webdriver.Chrome(service=service, options=options)
        return self.profile_id,driver
