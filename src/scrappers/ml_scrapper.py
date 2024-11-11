from bs4 import BeautifulSoup
from ...config.settings import Settings
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import clipboard as pc
import random

class MercadoLibreScrapper:

    def __init__(self):
        s=Settings()
        self.tiempo = s.selenium_tiempo()
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        pagina = random.randint(1, 20)
        self.driver.get("https://www.mercadolibre.com.mx/ofertas?page=", pagina)

        
    def buscar(self):
        lista_de_productos = []
        time.sleep(self.tiempo)
        
        promo = {
            "url":"NADA",
            "titulo":"NADA",
            "imagen":"NADA"
        }

        try:
            titulo_producto = self.driver.find_element(By.XPATH,'//*[@id="ui-pdp-main-container"]/div[1]/div/div[1]/div[2]/div[1]/div/div[2]/h1')
            time.sleep(self.tiempo)
        except:
            titulo_producto = self.driver.find_element(By.XPATH,'//*[@id="header"]/div/div[2]/h1')
            time.sleep(self.tiempo)
        
        #/html/body/main/div[2]/div[5]/div[2]/div[2]/div[1]/div/div/div/div/span[1]/figure/img
        try:
            imagen_producto = self.driver.find_element(By.XPATH, "/html/body/main/div[2]/div[5]/div[2]/div[2]/div[1]/div/div/div/div/span[1]/figure/img")
        except:
            try:
                imagen_producto = self.driver.find_element(By.XPATH, "/html/body/main/div[2]/div[6]/div[2]/div[2]/div[1]/div/div/div/div/span[1]/figure/img")
            except:
                try:
                    imagen_producto = self.driver.find_element(By.XPATH, "/html/body/main/div[2]/div[3]/div[2]/div[2]/div[1]/div/div[1]/div[1]/div/div/div/span[1]/figure/img")
                except:
                    imagen_producto = self.driver.find_element(By.XPATH, "/html/body/main/div[2]/div[3]/div[3]/div[2]/div[1]/div/div[1]/div[1]/div/div/div/span[1]/figure/img")
        
        
        
        boton_gen_link = self.driver.find_element(By.XPATH, '//*[@id="P0-1"]')
        
        if boton_gen_link.is_displayed and boton_gen_link.is_enabled:
            boton_gen_link.click()
            time.sleep(self.tiempo)
        else:
            self.driver.get("https://www.mercadolibre.com.mx/")
            return promo
        
        promo = {
            "url":pc.paste(),
            "titulo":self.producto + ": " + titulo_producto.text,
            "imagen":imagen_producto.get_attribute("src")
        }
        lista_de_productos.add(promo)
        #self.driver.close()
        self.driver.get("https://www.mercadolibre.com.mx/")
        return lista_de_productos
    
    def obtener_enlaces(self):
        enlaces = []
        html = self.driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        objeto = soup.find("window.__PRELOADED_STATE__")
        print(objeto)
        return enlaces
    

ml = MercadoLibreScrapper
e = ml.obtener_enlaces()