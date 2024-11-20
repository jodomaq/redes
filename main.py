from config.settings import Settings
from src.scrappers.ml_scrapper import MercadoLibreScrapper
from src.database.db_handler import DatabaseHandler
import sys

try:
    if len(sys.argv) > 1:
        tipo_scipt = sys.argv[1]
    else:
        #print(sys.argv)
        raise Exception("debe seleccionar el modo: --scrap-- o --face--")
        
    if tipo_scipt == "scrap":
        ml = MercadoLibreScrapper()
        links = ml.obtener_promociones()
        db = DatabaseHandler()
        for promo in links:
            db.guardar_oferta(promo)
    elif tipo_scipt == "face":
        print(tipo_scipt)
    else:
        #print(tipo_scipt)
        raise Exception("debe seleccionar el modo: [scrap] o [face]")
except Exception as e:
    print(e)

# db = DatabaseHandler()
# promo = {'url': 'https://www.mercadolibre.com.mx/autoestereo-pioneer-mvhs235bt-fmusbbtaux-1din-50wx4/p/MLM38714924', 'titulo': 'Autoestereo Pioneer Mvhs235bt Fm/usb/bt/aux 1din 50wx4', 'imagen': 'https://http2.mlstatic.com/D_NQ_NP_2X_689419-MLU77991093984_082024-F.webp', 'precio': 1198, 'url_afiliados': 'https://mercadolibre.com/sec/1rF3yyX'}
# db.guardar_oferta(promo)