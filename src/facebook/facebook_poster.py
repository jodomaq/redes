import os
import requests
from config.settings import Settings

# GROUP ID: 568052745799043

class Fb_poster:
    
    def __init__(self) -> None:
        pass
    
    def post_single_photo(page_id, page_access_token, message, link):
        url = f"https://graph.facebook.com/v20.0/{page_id}/feed"
        params = {
            'access_token': page_access_token,
            'message': message,
            'link': link,
        }

        try:
            response = requests.post(url, params=params)
            result = response.json()

            if 'id' in result:
                print("***********************************")
                print(f"FB posted successfully. Post ID: {result['id']}")
                print("***********************************")
            else:
                print("***********************************")
                print(f"Error posting FB: {result}")
                print("***********************************")

        except requests.exceptions.RequestException as e:
            print("***********************************")
            print(f"FB Request error: {e}")
            print("***********************************")

# load_dotenv()
# page_id = os.getenv("fb_page_id")
# page_access_token = os.getenv("token_fbap")
# message = 'Descubre el Poder del Cargador de Pared USB-C Rápido de 40W: ¡La Revolución en Carga Rápida!'
# link = 'https://plataformar21.mx/?p=549'
# post_single_photo(page_id, page_access_token, message, link)