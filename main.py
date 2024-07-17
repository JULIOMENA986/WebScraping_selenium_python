from selenium_client import SeleniumClient

if __name__ == "__main__":
    config_files = ["config.json", "config2.json", "config3.json", "config4.json"]
    client = SeleniumClient(config_files)
    client.read_configuration()
