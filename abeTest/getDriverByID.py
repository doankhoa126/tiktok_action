import requests
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

def read_id_profile():
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

def getDriver():
    id_profile = read_id_profile()
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