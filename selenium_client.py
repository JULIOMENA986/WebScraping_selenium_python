import json
from browser_settings import BrowserSettings
from web_interaction import WebInteraction
from data_extraction import DataExtraction

class SeleniumClient:
    
    def __init__(self, config_paths):
        self.config_paths = config_paths
        self.browser_settings = BrowserSettings()
        self.web_interaction = WebInteraction()
        
    def read_configuration(self):
        self.browser_settings.configure()
        self.web_interaction.init_browser(self.browser_settings.options)
        
        for config_path in self.config_paths:
            with open(config_path, 'r') as file:
                config_data = json.load(file)
            
            data_extraction = DataExtraction(self.web_interaction.driver)
            
            for config in config_data["settings"]:
                action_type = config['TYPE']
                xpath = config['XPATH']
                filename = config.get('FILE', '')
                value = config.get('VALUE', '')
                
                if action_type == 'URL':
                    self.web_interaction.url = xpath
                    self.web_interaction.get_page()
                elif action_type == 'TABLE':
                    data_extraction.extract_data_table(xpath, filename)
                elif action_type in ['OL', 'UL']:
                    data_extraction.extract_data_list_or_div(xpath, filename, 'li')
                elif action_type == 'DIV':
                    data_extraction.extract_data_list_or_div(xpath, filename, 'div')
                elif action_type == 'A':
                    self.web_interaction.click_link(xpath)
                elif action_type == 'BUTTON':
                    self.web_interaction.click_button(xpath)
                elif action_type == 'SELECT':
                    self.web_interaction.select_value(xpath, value)
                elif action_type == 'INPUT':
                    self.web_interaction.input_value(xpath, value)
        
        self.web_interaction.quit_browser()
