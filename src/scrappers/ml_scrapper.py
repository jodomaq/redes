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
from .base_scrapper import Scrapper
import time
import clipboard as pc
import random
#ruta = os.path.abspath(os.path.join(__file__, "../../../config"))
#print(ruta)
#sys.path.insert(0, ruta)
#from settings import Settings

class MercadoLibreScrapper(Scrapper):

    def __init__(self):
        pagina = random.randint(1, 20)
        url = "https://www.mercadolibre.com.mx/ofertas?page=" + str(pagina)
        self.driver = super().controlador()
        self.driver.get(url)
        self.tiempo = super().tiempo()
        time.sleep(self.tiempo)
        self.promo = {
            "url":"NADA",
            "titulo":"NADA",
            "imagen":"NADA",
            "precio":"NADA",
            "url_afiliados":"NADA"
        }
        self.enlaces = []

        
    def obtener_enlace_afiliados_rand(self):
        try:
            #print("len de enlaces: ", len(self.enlaces))
            if len(self.enlaces) > 0:
                for x in range(len(self.enlaces)):
                    producto = random.randint(0, len(self.enlaces))
                    url = self.enlaces[producto]["url"].strip()
                    #print("enlace: -"+str(url)+"-")
                    self.driver.get(str(url))
                    #self.driver.get("https://google.com")
                    time.sleep(self.tiempo)
                    boton_gen_link = self.driver.find_element(By.XPATH, '//*[@id="P0-1"]')
                    
                    if boton_gen_link.is_displayed and boton_gen_link.is_enabled:
                        time.sleep(self.tiempo)
                        boton_gen_link.click()
                        time.sleep(self.tiempo)
                        return str(pc.paste())
                        exit
            else:
                raise Exception("Primero debe obtener promociones")
        except Exception as e:
            print(e)
    
    def obtener_promociones(self):
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
                    self.promo['url_afiliados'] = self.obtener_enlace_afiliado('https://'+(item['metadata']['url']).strip())
                    if self.obtener_enlace_afiliado('https://'+(item['metadata']['url']).strip()) is not None:
                        self.enlaces.append(self.promo)
                        print(self.promo)
            else:
                print("no se encontró match")
        return self.enlaces

    def obtener_afiliados_lista(self):
        try:
            print("len de enlaces: ", len(self.enlaces))
            if len(self.enlaces) > 0:
                i=0
                for p in self.enlaces:
                    url = p["url"].strip()
                    print(url)
                    self.driver.get(str(url))
                    time.sleep(self.tiempo)
                    boton_gen_link = self.driver.find_element(By.XPATH, '//*[@id="P0-1"]')
                    
                    if boton_gen_link.is_displayed and boton_gen_link.is_enabled:
                        time.sleep(self.tiempo)
                        boton_gen_link.click()
                        time.sleep(self.tiempo)
                        self.enlaces[i]["url_afiliados"] = str(pc.paste())
                        print(self.enlaces[i])
                        print(i)
                    i=i+1
            else:
                raise Exception("Primero debe obtener promociones")
            return self.enlaces
        except Exception as e:
            print("Error en obtener_afiliados_lista")
            print(e)


    def obtener_enlace_afiliado(self, enlace_generico):
        try:
            self.driver.get(enlace_generico)
            time.sleep(self.tiempo)
            boton_gen_link = self.driver.find_element(By.XPATH, '//*[@id="P0-1"]')
            if boton_gen_link.is_displayed and boton_gen_link.is_enabled:
                time.sleep(self.tiempo)
                boton_gen_link.click()
                time.sleep(self.tiempo)
                return(str(pc.paste()))
        except Exception as e:
            print("Error en obtener_afiliados_lista")
            print(e)


#ml = MercadoLibreScrapper()
#links = ml.obtener_promociones()
#afilia = ml.obtener_enlace_afiliados()
#print(afilia)