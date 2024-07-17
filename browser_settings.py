from selenium import webdriver

class BrowserSettings:
    
    def __init__(self):
        self.options = webdriver.ChromeOptions()
    
    def configure(self):
        self.options.add_argument("--start-maximized")
        self.options.add_argument("--disable-extensions")
