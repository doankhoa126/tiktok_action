import time
import json
import utils
from PyQt6.QtCore import QObject, pyqtSignal

class Login2(QObject):
    update_status_signal = pyqtSignal(int, str)

    def __init__(self, driver, account_group) -> None:
        super().__init__()
        self.driver = driver
        self.account_group = account_group

    def get_xpath_list(file_path, interaction_name):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                for interaction in data:
                    if interaction["name_interaction"] == interaction_name:
                        return interaction["xpath_list"]
                return None
        except Exception as e:
            print(f"Error reading JSON file: {e}")
            return None

    def runLogin(self):
        email = self.account_group[0]['email']
        password = self.account_group[0]['password']
        index = self.account_group[0]['index']
        print('login2')
        print(index)
        xpaths = self.get_xpath_list(utils.XPATH_LOGIN_JSON, 'login')
        self.driver.get('https://www.tiktok.com/login/phone-or-email/email')
        self.update_status_signal.emit(index, "Login started")  # Phát tín hiệu
        # Thực hiện các thao tác đăng nhập
        # Ví dụ: driver.find_element(...)
        # Giả sử đăng nhập thành công:
        self.update_status_signal.emit(index, "Login successful")