import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from pandas_client import PandasClient

class WebInteraction:
    
    def __init__(self):
        self.driver = None
        
    def init_browser(self, options):
        self.driver = webdriver.Chrome(options=options)
        
    def get_page(self, url):
        self.driver.get(url)
        self.driver.implicitly_wait(10)
        
    def click_button(self, xpath):
        try:
            button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            button.click()
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error finding button: {e}")
        
    def click_link(self, xpath):
        try:
            link = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            url = link.get_attribute('href')
            self.get_page(url)
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error finding link: {e}")
        
    def select_value(self, xpath, value):
        try:
            select_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            select = Select(select_element)
            select.select_by_value(value)
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error finding select element: {e}")
        
    def input_value(self, xpath, value):
        try:
            input_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            input_element.send_keys(value)
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error finding input element: {e}")
        
    def quit_browser(self):
        self.driver.quit()

class DataExtraction:
    
    def __init__(self, driver):
        self.driver = driver
        
    def extract_data_table(self, xpath, filename):
        try:
            table = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            headers = [header.text for header in table.find_elements(By.XPATH, ".//th")]
            rows = table.find_elements(By.XPATH, ".//tr")
            
            data = []
            for row in rows:
                cells = row.find_elements(By.XPATH, ".//td")
                if headers:
                    row_data = {headers[i]: cells[i].text for i in range(len(cells))}
                else:
                    row_data = [cell.text for cell in cells]
                data.append(row_data)
            
            table_data = {
                "data": data
            }
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error finding table: {e}")
            table_data = {
                "data": []
            }
        
        excel_dir = 'excels'
        if not os.path.exists(excel_dir):
            os.makedirs(excel_dir)
        
        excel_path = os.path.join(excel_dir, f'{filename}.xlsx')
        PandasClient(table_data).to_excel(excel_path)
        
    def extract_data_list_or_div(self, xpath, filename, tag_name):
        try:
            elements = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, xpath))
            )
            data_list = [element.text for element in elements if element.tag_name == tag_name]
            
            json_dir = 'json_guardados'
            if not os.path.exists(json_dir):
                os.makedirs(json_dir)
                
            json_path = os.path.join(json_dir, f'{filename}.json')
            with open(json_path, 'w') as file:
                json.dump(data_list, file)
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error finding elements: {e}")

class SeleniumClient:
    
    def __init__(self, config_files):
        self.config_files = config_files
        self.browser_settings = WebInteraction()
        
    def read_configuration(self):
        self.browser_settings.init_browser(options=None)
        
        for config_file in self.config_files:
            with open(config_file, 'r') as file:
                config_data = json.load(file)
            
            data_extraction = DataExtraction(self.browser_settings.driver)
            
            for config in config_data["settings"]:
                action_type = config['TYPE']
                xpath = config['XPATH']
                filename = config.get('FILE', '')
                value = config.get('VALUE', '')
                
                action_mapping = {
                    'URL': self.browser_settings.get_page,
                    'CLICK': self.browser_settings.click_button,
                    'A': self.browser_settings.click_link,
                    'BUTTON': self.browser_settings.click_button,
                    'SELECT': self.browser_settings.select_value,
                    'INPUT': self.browser_settings.input_value,
                    'TABLE': lambda x, f: data_extraction.extract_data_table(x, f),
                    'OL': lambda x, f: data_extraction.extract_data_list_or_div(x, f, 'ol'),
                    'UL': lambda x, f: data_extraction.extract_data_list_or_div(x, f, 'ul'),
                    'DIV': lambda x, f: data_extraction.extract_data_list_or_div(x, f, 'div')
                }
                
                if action_type in action_mapping:
                    action_func = action_mapping[action_type]
                    if action_type in ['TABLE', 'OL', 'UL', 'DIV']:
                        action_func(xpath, filename)
                    elif action_type in ['SELECT', 'INPUT']:
                        action_func(xpath, value)
                    else:
                        action_func(xpath)
        
        self.browser_settings.quit_browser()


