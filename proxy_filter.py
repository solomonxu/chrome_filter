from selenium import webdriver
from browsermobproxy import Server
import re
import time

## Class ProxyFilter
class ProxyFilter:   
    # Init: 
    def __init__(self):
        # Start a http proxy
        self.proxy_server = Server("browsermob-proxy")
        self.proxy_server.start()
        self.proxy = self.proxy_server.create_proxy()
        # Configure chrome options
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("headless")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--ignore-certificate-errors')
        # Configure the proxy in chrome options        
        chrome_options.add_argument("--proxy-server={0}".format(self.proxy.proxy)) 
        # Start a browser       
        self.browser = webdriver.Chrome(chrome_options)

    # Filter: 
    def filterFileUrls(self, page_url, pattern):
        #Tag the har(network logs) with a name
        self.proxy.new_har(page_url)
        # Then you can navigate to page using selenium
        self.browser.get(page_url)        
        # Sleep, waiting for completion
        time.sleep(3)
        # After navigation, you can get the network logs in json format from the proxy
        urls = [entry['request']['url'] for entry in self.proxy.har['log']['entries']]
        # Extract URLs from the "entries" section of the .har file
        filtered_urls = [url for url in urls if re.search(pattern, url)]
        # return
        return filtered_urls

    # Filter: 
    def filterVideoUrls(self, page_url, pattern):
        return self.getFileUrl(self, page_url, pattern)
    
    # Cleanup: Also before quitting the driver, stop the proxy server as well at the end
    def cleanup(self):
        self.browser.quit()
        self.proxy_server.stop()
    