from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from selenium import webdriver
import json
# from webdriver_manager.chrome import ChromeDriverManager
import random
import requests
import string
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options



class DriverGPM():
    driver: webdriver.Chrome
    profile_name: str
    profile_id: str

    def __init__(self, proxy, user_agent) -> None:
        self.driver = self.createProfileDriver(proxy=proxy, user_agent=user_agent)

    def redirect(self, url: str):
        self.driver.get(url)

    def input_(self, xpath: str, content: str, timeout=2):
        input_text = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(
                (By.XPATH, xpath))
        )
        input_text.click()
        input_text.clear()
        for char in content:
            input_text.send_keys(char)
            time.sleep(0.1)

    def click(self, xpath: str, timeout=2) -> bool:
        accept_btn = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(
                (By.XPATH, xpath))
        )
        accept_btn.click()

    def get_current_url(self):
        return self.driver.current_url

    def close(self):
        self.driver.close()
        self.deleteProfileGPM()


    def generate_profile_name(self, length: int):
        if length < 8:
            length = 8
        characters = string.ascii_letters + string.digits
        profile_name = ''.join(random.choice(characters) for i in range(length))
        return profile_name

    def createProfileDriver(self, proxy,user_agent):
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

        print('create profile')
        try:
            response = requests.post(urlCreate, data=json.dumps(dataJson), headers=headers)
            response.raise_for_status() 
            response_data = response.json()
            print("Profile created successfully")
            
            # Lấy giá trị của id từ phản hồi JSON
            self.profile_id = response_data.get('data', {}).get('id')
            fileID_path  = '../data/id_profile.txt'
            with open(fileID_path, 'a') as f:
                f.write(str(self.profile_id) + '\n')

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: ", str(e))
            return None
        except Exception as e:
            print(f"An error occurred: ", str(e))
            return None

        urlStart = 'http://127.0.0.1:19995/api/v3/profiles/start/'
        urlGetProfile = f'{urlStart}{self.profile_id}?win_scale=0.8&win_pos=300,300'
        
        try:
            response = requests.get(urlGetProfile)
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
        return driver



# userAgent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
# proxy = '222.253.48.16:8080'
# instance = DriverGPM(proxy, userAgent)
# driver = instance.driver  # Use the driver from the instance
# driver.get('https://www.google.com')
# time.sleep(90000)