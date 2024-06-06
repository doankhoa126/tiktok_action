import queue
from PyQt6.QtCore import QThread, pyqtSignal, QObject
from selenium import webdriver
import time
import json
import utils
import random
from concurrent.futures import ThreadPoolExecutor
from PyQt6.QtCore import QObject, pyqtSignal
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from be_tiktok_tool.driverGPM import DriverGPM
from be_tiktok_tool.login import Login
from be_tiktok_tool.newfeed import NewFeed
from be_tiktok_tool.Interaction_tiktok import InteractionTikok
from be_tiktok_tool.testLogin2 import Login2

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


class TikTokActionWorker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(str)
    # update_table_signal = pyqtSignal(int, str)
    update_status  = pyqtSignal(int,str)
    update_profile_id = pyqtSignal(int,str)
    
    def extract_xpaths_from_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            xpath_list = data.get("xpath_list", [])
            xpaths = {key: value for item in xpath_list for key, value in item.items()}
        return xpaths

    def __init__(self, acc_tiktok_data, thread_value,tiktokTable):
        super().__init__()
        self.acc_tiktok_data = acc_tiktok_data
        self.thread_value = int(thread_value)
        self.account_queue = queue.Queue()
        self.tiktokTable = tiktokTable


        for account in self.acc_tiktok_data:
            self.account_queue.put(account)

    def run(self):
        self.progress.emit("Starting TikTok bot...")

        with ThreadPoolExecutor(max_workers=self.thread_value) as executor:
            futures = [
                executor.submit(self.process_task)
                for _ in range(self.thread_value)
            ]

            for future in futures:
                future.add_done_callback(self.task_done_callback)

        self.progress.emit("All accounts processed.")
        self.finished.emit()

    def process_task(self):
        while not self.account_queue.empty():
            account = self.account_queue.get()
            if account is None:
                break

            proxy = get_proxy(utils.PROXY_TXT)
            user_agent = get_user_agent(utils.USER_AGENT_TXT)
            print(proxy, user_agent)

            # insGPM = DriverGPM(proxy, user_agent)
            # driver = insGPM.driver
            # profile_id,dr2 = insGPM.createProfileDriver()

            # tikokIns = InteractionTikok(driver, insGPM, [account],self.regAccTable,)
            # success = tikokIns.run()
            # login_instance = Login(driver, insGPM, [account])
            driver = webdriver.Chrome()
            login_instance = Login2(driver, [account])
            login_instance.update_status_signal.connect(self.update_status)
            print('self.update_status',self.update_status)
            login_instance.runLogin()


            # if success:
            #     self.update_table_signal.emit(account, "success")
            # else:
            #     self.update_table_signal.emit(account, "error")

          

    def task_done_callback(self, future):
        # Check if there are more accounts to process
        if not self.account_queue.empty():
            with ThreadPoolExecutor(max_workers=50) as executor:
                executor.submit(self.process_task)


