#Archivo para almacenar variables de configuración, como claves de API de Facebook, URL de la base de datos, y configuraciones para el navegador Selenium.
from dotenv import load_dotenv
import os
class Settings:
    
    def __init__(self) -> None:
        self.selenium_tiempo
        load_dotenv()
        pass
    
    def selenium_tiempo(self):
        self.selenium_tiempo = 3
        return self.selenium_tiempo
    
    def DB_settings(self):
        db_sett = {
            "usuario":os.getenv("usr"),
            "contrasenia":os.getenv("passwd"),
            "database":os.getenv("database"),
            "servidor":os.getenv("host")
        }
        return db_sett