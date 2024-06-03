from PyQt6.QtCore import QThread, pyqtSignal, QObject
from selenium import webdriver
import time
import json 
import utils
import random
from concurrent.futures import ThreadPoolExecutor
import time
from PyQt6.QtCore import QObject, pyqtSignal
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from be_tiktok_tool.driverGPM import DriverGPM

def get_user_agent(file_path):
        print('get_user_agent')
        with open(file_path, 'r') as file:
            user_agents = [line.strip() for line in file if line.strip()]
        
        if user_agents:
            return random.choice(user_agents)
        else:
            raise ValueError("Lỗi lấy user agents")
def get_proxy(file_path):
    try:
        with open(file_path, 'r') as file:
            proxies = [line.strip() for line in file if line.strip()]
        
        if proxies:
            return random.choice(proxies)  # Chọn giá trị ngẫu nhiên từ danh sách
        else:
            raise ValueError("Lỗi lấy proxies")
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return None

class TikTokWorker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(str)
    

    def extract_xpaths_from_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            xpath_list = data.get("xpath_list", [])
            xpaths = {key: value for item in xpath_list for key, value in item.items()}
        return xpaths
    def __init__(self, reg_acc_data, thread_value):
        super().__init__()
        self.reg_acc_data = reg_acc_data
        self.thread_value = int(thread_value)  # Ensure thread_value is an integer

    def run(self):
        self.progress.emit("Starting TikTok bot...")

        # Ensure accounts_per_thread is at least 1
        accounts_per_thread = max(1, len(self.reg_acc_data) // self.thread_value)
        
        account_groups = [self.reg_acc_data[i:i+accounts_per_thread] for i in range(0, len(self.reg_acc_data), accounts_per_thread)]
        
        with ThreadPoolExecutor(max_workers=self.thread_value) as executor:
            for account_group in account_groups:
                executor.submit(self.process_task, account_group)

        self.progress.emit("All accounts processed.")
        self.finished.emit()
    def process_task(self, account_group):
        proxy = get_proxy(utils.PROXY_TXT)
      
        user_agent = get_user_agent(utils.USER_AGENT_TXT)
        print(proxy, user_agent)
        instance = DriverGPM(proxy,user_agent)
        driver = instance.driver
        xpaths = self.extract_xpaths_from_file(utils.JSON_REG_ACC)
        for account in account_group:
            driver.get("https://www.tiktok.com/signup/phone-or-email/email")
            time.sleep(3)
            
            #Choose month Birthday 
            month = random.randint(1, 12)
            xpath_MonthBirthday = xpaths['xpath_MonthBirthday'] 
            instance.click(xpath_MonthBirthday)

            xpath_choose1 = xpaths['xpath_ChooseMonthBirthday']
            xpath_ChooseMonthBirthday = xpath_choose1.format(month=month)
            instance.click(xpath_ChooseMonthBirthday)
            time.sleep(10)
            # xpath_choose2 = xpaths['xpath_ChooseDayBirthday']
            # xpath_ChooseDayBirthday = xpath_choose2.format(day=day)
            # ChooseDayBirthday_btn = WebDriverWait(driver, 10).until(
            #     EC.element_to_be_clickable((By.XPATH, xpath_ChooseDayBirthday))
            # )
            # ChooseDayBirthday_btn.click()
           
            driver.close()