from selenium_client import SeleniumClient

if __name__ == "__main__":
    config_path = "config.json"  
    client = SeleniumClient(config_path)
    client.read_configuration()
