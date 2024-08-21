from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


class DriverManager:


    def get_driver(self):
        return self.driver

    def create_driver(self):
        #open chrome
        chrome_options = Options()
        chrome_options.add_argument("--incognito")  # Use incognito mode

        capabilities = DesiredCapabilities.CHROME.copy()
        capabilities['browserName'] = 'chrome'

        options = webdriver.ChromeOptions()
        options.binary_location = "./chromedriver"

        self.driver = webdriver.Chrome(options)
        return self.driver