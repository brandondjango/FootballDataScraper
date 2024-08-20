from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
import selenium

class MatchScraper:

    def url(self, id):
        return 'https://fbref.com/en/matches/' + id

    def scrape_match(self, id):
        chrome_options = Options()
        chrome_options.add_argument("--incognito")  # Use incognito mode

        capabilities = DesiredCapabilities.CHROME.copy()
        capabilities['browserName'] = 'chrome'

        options = webdriver.ChromeOptions()
        options.binary_location = "./chromedriver"
        #options

        driver = webdriver.Chrome(options)
        driver.get(self.url(id))


match = MatchScraper()
match.scrape_match("0b8f50a5")