from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
import pandas as pd
import time
import json
import os

class PandasClient:
    
    def __init__(self, data):
        self.data = data
        
    def _normalize_data(self):
        if isinstance(self.data, dict) and 'data' in self.data:
            data_list = self.data['data']
            if isinstance(data_list, list):
                if all(isinstance(item, dict) for item in data_list):
                    return pd.json_normalize(data_list)
                elif all(isinstance(item, list) for item in data_list):
                    headers = data_list[0]
                    data = data_list[1:]
                    max_columns = len(headers)
                    adjusted_data = [row[:max_columns] for row in data]
                    return pd.DataFrame(adjusted_data, columns=headers)
                
        return pd.DataFrame()

    def to_excel(self, file_path):
        df = self._normalize_data()
        df.to_excel(file_path, index=False)


class seleniumClient:
    
    def __init__(self, config_path):
        self.driver = None
        self.options = None
        self.url = ""
        self.config_path = config_path
        
    # Configuración del navegador
    def settings(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--start-maximized")
        self.options.add_argument("--disable-extensions")
        
    # Inicializar el navegador con las configuraciones establecidas
    def initBrowser(self):
        service = ChromeService(executable_path=ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=self.options)
        
    def get_page(self):
        self.driver.get(self.url)
        self.driver.implicitly_wait(10)
        
    def readConfiguration(self):
        self.settings()
        self.initBrowser()
        
        with open(self.config_path, 'r') as file:
            config_data = json.load(file)
        
        for config in config_data["settings"]:
            if config['TYPE'] == 'URL':
                self.url = config['XPATH']
                self.get_page()
            if config['TYPE'] == 'TABLE':
                self.extractDataTable(config['XPATH'], config['FILE'])
                time.sleep(10)
            if config['TYPE'] in ['OL', 'UL']:
                self.extractDataList(config['XPATH'], config['FILE'])
                time.sleep(10)
            if config['TYPE'] == 'DIV':
                self.extractDataDiv(config['XPATH'], config['FILE'])
                time.sleep(10)
            if config['TYPE'] == 'A':
                self.clickLink(config['XPATH'])
                time.sleep(10)
            if config['TYPE'] == 'BUTTON':
                self.clickButton(config['XPATH'])
                time.sleep(10)
            if config['TYPE'] == 'SELECT':
                self.selectValue(config['XPATH'], config['VALUE'])
                time.sleep(10)
            if config['TYPE'] == 'INPUT':
                self.inputValue(config['XPATH'], config['VALUE'])
                time.sleep(10)
                
        self.driver.quit()
                
    def extractDataTable(self, xpath, filename):
        try:
            table = self.driver.find_element(By.XPATH, xpath)
            try:
                thead = table.find_element(By.TAG_NAME, 'thead')
                headers = [header.text for header in thead.find_elements(By.TAG_NAME, 'th')]
            except NoSuchElementException:
                headers = None
            
            tbody = table.find_element(By.TAG_NAME, 'tbody')
            rows = tbody.find_elements(By.TAG_NAME, 'tr')
            
            data = []
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, 'td')
                if headers:
                    row_data = {headers[i]: cells[i].text for i in range(len(cells))}
                else:
                    row_data = [cell.text for cell in cells]
                data.append(row_data)
            
            table_data = {
                "data": data
            }
        except NoSuchElementException as e:
            print(f"An error occurred: {e}")
            table_data = {
                "data": []
            }
        
        excel_dir = 'excels'
        if not os.path.exists(excel_dir):
            os.makedirs(excel_dir)
        
        excel_path = os.path.join(excel_dir, f'{filename}.xlsx')
        PandasClient(table_data).to_excel(excel_path)
        
    def extractDataList(self, xpath, filename):
        try:
            lista = self.driver.find_element(By.XPATH, xpath)
            items = lista.find_elements(By.TAG_NAME,'li')
            data_list = [item.text for item in items]       
            json_path = f'JsonGuardados/{filename}.json'
            with open(json_path, 'w') as file:
                json.dump(data_list, file)
        except NoSuchElementException as e:
            print(f"An error occurred: {e}")
        
    def extractDataDiv(self, xpath, filename):
        try:
            dataDiv = self.driver.find_element(By.XPATH,xpath)
            items = dataDiv.find_elements(By.TAG_NAME,'div')
            data_list = [item.text for item in items]
            json_path = f'JsonGuardados/{filename}.json'
            with open(json_path, 'w') as file:
                json.dump(data_list, file)
        except NoSuchElementException as e:
            print(f"An error occurred: {e}")
        
    def clickButton(self, xpath):
        button = self.driver.find_element(By.XPATH, xpath)
        button.click()
        
    def clickLink(self, xpath):
        a = self.driver.find_element(By.XPATH, xpath)
        url = a.get_attribute('href')
        self.url = url
        self.get_page()
        
    def selectValue(self, xpath, value):
        try:
            select_element = self.driver.find_element(By.XPATH, xpath)
            select = Select(select_element)
            select.select_by_value(value)
        except NoSuchElementException as e:
            print(f"An error occurred: {e}")
        
    def inputValue(self, xpath, value):
        try:
            input_element = self.driver.find_element(By.XPATH, xpath)
            input_element.send_keys(value)
            time.sleep(4)
        except NoSuchElementException as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    config_path = "config.json"  
    client = seleniumClient(config_path)
    client.readConfiguration()
