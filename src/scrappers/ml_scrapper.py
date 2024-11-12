#MAC
#/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222

#UBUNTU
#google-chrome --remote-debugging-port=9222 --user-data-dir=/.config/ --no-first-run --no-default-browser-check

import sys
import os
import re
import json
from bs4 import BeautifulSoup
#from ...config.settings import Settings
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import clipboard as pc
import random
ruta = os.path.abspath(os.path.join(__file__, "../../../config"))
print(ruta)
sys.path.insert(0, ruta)
from settings import Settings

class MercadoLibreScrapper:

    def __init__(self):
        s=Settings()
        self.tiempo = s.selenium_tiempo()
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        pagina = random.randint(1, 20)
        url = "https://www.mercadolibre.com.mx/ofertas?page=" + str(pagina)
        self.driver.get(url)
        self.promo = {
            "url":"NADA",
            "titulo":"NADA",
            "imagen":"NADA",
            "precio":"NADA"
        }

        
    def buscar(self):
        lista_de_productos = []
        time.sleep(self.tiempo)

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
            "imagen":imagen_producto.get_attribute("src"),
            "precio":""
        }
        lista_de_productos.add(promo)
        #self.driver.close()
        self.driver.get("https://www.mercadolibre.com.mx/")
        return lista_de_productos
    
    def obtener_enlaces(self):
        enlaces = []
        html = self.driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        script_tag = soup.find(string=re.compile(r'window\.__PRELOADED_STATE__\s*=\s*(\{.*\});'))
        if script_tag:
            script_content = script_tag.string
            match = re.search(r'window\.__PRELOADED_STATE__\s*=\s*(\{.*\});', script_content)
            if match:
                js_object_str = match.group(1)
                js_object = json.loads(js_object_str)
                for item in js_object['data']['items']:
                    #print('URL = https://'+(item['metadata']['url']).strip())
                    #print('IMAGEN = ','https://http2.mlstatic.com/D_NQ_NP_2X_'+(item['pictures']['pictures'][0]['id']).strip()+'-F.webp')
                    titulo = next(i['title']['text'] for i in item['components'] if i['type'] == 'title')
                    #print('TITULO = ',titulo)
                    precio = next(i['price']['current_price']['value'] for i in item['components'] if i['type'] == 'price')
                    #print('PRECIO = ',precio)
                    self.promo['url'] = 'https://'+(item['metadata']['url']).strip()
                    self.promo['titulo'] = titulo
                    self.promo['imagen'] = 'https://http2.mlstatic.com/D_NQ_NP_2X_'+(item['pictures']['pictures'][0]['id']).strip()+'-F.webp'
                    self.promo['precio'] = precio
                    enlaces.append(self.promo)
            else:
                print("no se encontró match")
        return enlaces
    

#ml = MercadoLibreScrapper()
#links = ml.obtener_enlaces()
#print(len(links))