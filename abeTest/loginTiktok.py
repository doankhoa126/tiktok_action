import json
import time
import threading
from getDriver import DriverGPM
from getProxy import read_proxies
from getUserAgent import get_random_user_agent
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Function to read accounts from a JSON file
def read_accounts(file_path):
    with open(file_path, 'r') as file:
        accounts_data = json.load(file)
    return accounts_data['accounts']

class InteractionTiktok():
    
    def login_tiktok(self, proxy, user_agent, username, password):  
        instance = DriverGPM(proxy, user_agent)
        driver = instance.driver  # Use the driver from the instance
        driver.get('https://www.tiktok.com/login/phone-or-email/email')

        inputUsername_xpath = '//*[@id="loginContainer"]/div[1]/form/div[1]/input'
        inputUsername = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, inputUsername_xpath))
        )
        inputUsername.send_keys(username)

        inputPass_xpath = '//*[@id="loginContainer"]/div[1]/form/div[2]/div/input'
        inputPass = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, inputPass_xpath))
        )
        inputPass.send_keys(password)

        loginBtn_xpath = '//*[@id="loginContainer"]/div[1]/form/button'
        loginBtn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, loginBtn_xpath))
        )
        loginBtn.click()

        time.sleep(10)
        driver.quit()

def thread_function(proxy, user_agent, username, password):
    interaction = InteractionTiktok()
    driver = interaction.login_tiktok(proxy, user_agent, username, password)
    # You can perform additional actions with the driver here
    # Example: driver.quit() to close the browser instance after use

def main():
    file_path_proxy = '../data/proxy.txt'  
    file_path_user_agent = '../data/user_agents.txt'
    file_path_accounts = '../data/account.json'  # Path to the account.json file
    
    user_agent = get_random_user_agent(file_path_user_agent)
    print(user_agent)
    
    list_proxies = read_proxies(file_path_proxy)
    accounts = read_accounts(file_path_accounts)
    
    n = int(input("Enter the number of threads per proxy: "))
    
    threads = []
    account_index = 0

    def start_new_thread(proxy):
        nonlocal account_index
        if account_index < len(accounts):
            username = accounts[account_index]['username']
            password = accounts[account_index]['password']
            account_index += 1

            thread = threading.Thread(target=thread_function, args=(proxy, user_agent, username, password))
            thread.start()
            threads.append(thread)

    for proxy in list_proxies:
        print(proxy)
        # Create and start initial n threads for each proxy
        for _ in range(n):
            start_new_thread(proxy)

    while threads:
        for thread in threads:
            if not thread.is_alive():
                threads.remove(thread)
                for proxy in list_proxies:
                    start_new_thread(proxy)
                break

        time.sleep(1)

    print("All threads completed.")

if __name__ == "__main__":
    main()
