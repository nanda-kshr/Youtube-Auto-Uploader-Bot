from selenium import webdriver
from time import sleep

def setup_browser():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode if you don't need UI
    browser = webdriver.Chrome(options=options)
    return browser
