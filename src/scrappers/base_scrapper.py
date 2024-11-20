import sys
import os
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
#ruta = os.path.abspath(os.path.join(__file__, "../../../config"))
#print(ruta)
#sys.path.insert(0, ruta)
from config.settings import Settings

class Scrapper:
    def __init__(self):
       pass
       
    def controlador(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        return self.driver
    
    def tiempo(self):
        s=Settings()
        self.tiempo = s.selenium_tiempo()
        return self.tiempo
