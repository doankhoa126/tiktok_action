
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

HOTMAIL_JSON = resource_path('data_tiktok_tool/hotmail.json')
PROXY_TXT = resource_path('data_tiktok_tool/proxy.txt')
USER_AGENT_TXT = resource_path('data_tiktok_tool/user_agents.txt')
XPATH_REGACC_JSON = resource_path('data_json_scripts/xpath_reg_acc.json')
OUTPUT_ACC_FOLDER = resource_path('output_data')
JSON_REG_ACC = resource_path('data_json_scripts/xpath_reg_acc.json')
PROFILE_ID_TXT = resource_path('data_tiktok_tool/id_profile.txt')
ACC_TIKTOK_JSON = resource_path('data_tiktok_tool/acc_tiktok.json')
CONFIG_ACCTION_TIKTOK = resource_path('data_tiktok_tool/config_acc_tiktok.json')
XPATH_LOGIN_JSON = resource_path('data_json_scripts/xpath_login.json')
XPATH_NEWFEED_JSON = resource_path('data_json_scripts/xpath_newfeed.json')
XPATH_CONFIG_INTERACTION_JSON  = resource_path('data_json_scripts/xpath_interaction_tiktok.json')
