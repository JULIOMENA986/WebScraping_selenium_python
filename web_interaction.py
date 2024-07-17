from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select

class WebInteraction:
    
    def __init__(self):
        self.driver = None
        self.url = ""
    
    def init_browser(self, options):
        service = ChromeService(executable_path=ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        
    def get_page(self):
        self.driver.get(self.url)
        self.driver.implicitly_wait(10)
        
    def quit_browser(self):
        self.driver.quit()
        
    def click_button(self, xpath):
        button = self.driver.find_element(By.XPATH, xpath)
        button.click()
        
    def click_link(self, xpath):
        a = self.driver.find_element(By.XPATH, xpath)
        self.url = a.get_attribute('href')
        self.get_page()
        
    def select_value(self, xpath, value):
        try:
            select_element = self.driver.find_element(By.XPATH, xpath)
            select = Select(select_element)
            select.select_by_value(value)
        except NoSuchElementException as e:
            print(f"An error occurred: {e}")
        
    def input_value(self, xpath, value):
        try:
            input_element = self.driver.find_element(By.XPATH, xpath)
            input_element.send_keys(value)
        except NoSuchElementException as e:
            print(f"An error occurred: {e}")
