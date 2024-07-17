from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By  # Importa By aquí
import os
import json
from pandas_client import PandasClient

class DataExtraction:
    
    def __init__(self, driver):
        self.driver = driver
        
    def extract_data_table(self, xpath, filename):
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
        
    def extract_data_list_or_div(self, xpath, filename, tag_name):
        try:
            elements = self.driver.find_elements(By.XPATH, xpath)
            data_list = [element.text for element in elements if element.tag_name == tag_name]
            
            json_dir = 'json_guardados'
            if not os.path.exists(json_dir):
                os.makedirs(json_dir)
                
            json_path = os.path.join(json_dir, f'{filename}.json')
            with open(json_path, 'w') as file:
                json.dump(data_list, file)
        except NoSuchElementException as e:
            print(f"An error occurred: {e}")
