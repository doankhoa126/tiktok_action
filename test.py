from PyQt6.QtCore import pyqtSignal, QObject, QThread
from selenium import webdriver
import time
import json 
import utils
import random
from concurrent.futures import ThreadPoolExecutor
from be_tiktok_tool.driverGPM import DriverGPM
from be_tiktok_tool.get_OTP import verifiedTiktok

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
    update_status = pyqtSignal(int, str)

    def extract_xpaths_from_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            xpath_list = data.get("xpath_list", [])
            xpaths = {key: value for item in xpath_list for key, value in item.items()}
        return xpaths

    def __init__(self, reg_acc_data, thread_value, regAccTable):
        super().__init__()
        self.reg_acc_data = reg_acc_data
        self.thread_value = int(thread_value)  # Ensure thread_value is an integer
        self.regAccTable = regAccTable

    def run(self):
        self.progress.emit("Starting TikTok bot...")

        # Split the reg_acc_data into batches based on thread_value
        accounts_per_thread = max(1, len(self.reg_acc_data) // self.thread_value)
        account_batches = [self.reg_acc_data[i:i + accounts_per_thread] for i in range(0, len(self.reg_acc_data), accounts_per_thread)]

        # Create and execute threads for each batch
        with ThreadPoolExecutor(max_workers=self.thread_value) as executor:
            for idx, account_batch in enumerate(account_batches):
                executor.submit(self.process_batch, idx, account_batch)

        self.progress.emit("All accounts processed.")
        self.finished.emit()

    def process_batch(self, batch_index, account_batch):
        proxy = get_proxy(utils.PROXY_TXT)
        user_agent = get_user_agent(utils.USER_AGENT_TXT)
        print(proxy, user_agent)
        driver = webdriver.Chrome()
        xpaths = self.extract_xpaths_from_file(utils.JSON_REG_ACC)
        
        try:
            for idx, account in enumerate(account_batch):
                self.update_status.emit(batch_index, f"Processing account {idx + 1}/{len(account_batch)}")
                # Your account processing logic here
                driver.get("https://www.tiktok.com/signup/phone-or-email/email")
                time.sleep(3)
                # Implement your task processing logic here

                # Simulate processing
                time.sleep(random.randint(5, 10))
        finally:
            driver.quit()  # Ensure driver is closed after task completion

        self.update_status.emit(batch_index, f"Batch {batch_index} completed.")

        exit()
            # Choose month Birthday 
        month = random.randint(1, 12)
        self.update_status.emit(idx, "Choosing birthday month")
        xpath_MonthBirthday = xpaths['xpath_MonthBirthday'] 
        instance.click(xpath_MonthBirthday)

        xpath_choose1 = xpaths['xpath_ChooseMonthBirthday']
        xpath_ChooseMonthBirthday = xpath_choose1.format(month=month)
        instance.click(xpath_ChooseMonthBirthday)
        time.sleep(10)
        
        # Choose day Birthday
        day = random.randint(1, 28)
        self.update_status.emit(idx, "Choosing birthday day")
        xpath_DayBirthday = xpaths['xpath_DayBirthday'] 
        instance.click(xpath_DayBirthday)

        xpath_chooseDay = xpaths['xpath_ChooseDayBirthday']
        xpath_ChooseDayBirthday = xpath_chooseDay.format(day=day)
        instance.click(xpath_ChooseDayBirthday)
        
        # Choose year Birthday
        year = random.randint(23, 43)
        self.update_status.emit(idx, "Choosing birthday year")
        xpath_YearBirthday = xpaths['xpath_YearBirthday'] 
        instance.click(xpath_YearBirthday)

        xpath_chooseYear = xpaths['xpath_ChooseYearBirthday']
        xpath_ChooseYearBirthday = xpath_chooseYear.format(year=year)
        instance.click(xpath_ChooseYearBirthday)

        # Input Email
        self.update_status.emit(idx, "Entering email")
        xpath_InputEmail = xpaths['xpath_input_email'] 
        instance.input_(xpath_InputEmail, account['email'])

        # Input password 
        self.update_status.emit(idx, "Entering password")
        passwordTiktok = f'{account["password"]}@123'
        xpath_InputPassword = xpaths['xpath_input_password'] 
        instance.input_(xpath_InputPassword, passwordTiktok)

        # Click send code button
        self.update_status.emit(idx, "Clicking send code button")
        xpath_sendCodeBtn = xpaths['xpath_sendCodeBtn']
        instance.click(xpath_sendCodeBtn)

        time.sleep(30)
        self.update_status.emit(idx, "Waiting for verification code")
        verified_code = verifiedTiktok(account['email'], account['password'])
        
        # Input OTP 
        self.update_status.emit(idx, "Entering OTP")
        xpath_InputOTP = xpaths['xpath_inputOTP'] 
        instance.input_(xpath_InputOTP, verified_code)
        self.update_status.emit(idx, "Account registered")