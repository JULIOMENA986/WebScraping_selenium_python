from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

class BrowserSettings:
    
    def __init__(self):
        self.options = None
        
    def configure(self):
        self.options = Options()
        self.options.add_argument("--start-maximized")
        self.options.add_argument("--disable-extensions")
        
    def init_browser(self):
        service = ChromeService(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=self.options)
        return driver