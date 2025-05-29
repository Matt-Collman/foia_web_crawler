from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

class SeleniumMiddleware:
    def __init__(self):
        firefox_options = Options()
        firefox_options.add_argument('--headless')
        self.driver = webdriver.Firefox(service=Service('C:/Users/scoll/downloads/geckodriver-v0.34.0-win64/geckodriver.exe'), options=firefox_options)

    def process_request(self, request, spider):
        self.driver.get(request.url)
        body = self.driver.page_source
        return HtmlResponse(self.driver.current_url, body=body, encoding='utf-8', request=request)

    def __del__(self):
        self.driver.quit()
