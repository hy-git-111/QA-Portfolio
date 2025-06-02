# utils/test_helper.py
from pages.signup_page import SignupPage
from config import config
import json, os

def get_test_data(key):
    with open(os.path.join(config.TEST_DATA_DIR, "test_data.json"), encoding="utf-8") as f:
        return json.load(f)[key]

def do_signup(driver, username, email, password):
    page = SignupPage(driver)
    page.navigate()
    page.signup(username, email, password)
    return page