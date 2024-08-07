from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

class WebInteraction:
    
    def __init__(self):
        self.driver = None
        self.url = ""
        
    def init_browser(self, options):
        self.driver = webdriver.Chrome(options=options)
        
    def get_page(self):
        self.driver.get(self.url)
        self.driver.implicitly_wait(10)
        
    def click_button(self, xpath):
        button = self.driver.find_element(By.XPATH, xpath)
        button.click()
        
    def click_link(self, xpath):
        link = self.driver.find_element(By.XPATH, xpath)
        url = link.get_attribute('href')
        self.url = url
        self.get_page()
        
    def select_value(self, xpath, value):
        select_element = self.driver.find_element(By.XPATH, xpath)
        select = Select(select_element)
        select.select_by_value(value)
        
    def input_value(self, xpath, value):
        input_element = self.driver.find_element(By.XPATH, xpath)
        input_element.send_keys(value)
        
    def quit_browser(self):
        self.driver.quit()