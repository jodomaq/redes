import mysql
from config.settings import Settings

class DatabaseHandler():
    def __init__(self) -> None:
        settings = Settings()
        self.conexion = settings.DB_settings()
        pass
    
    
    def guardar_oferta(self, promo):
        try:
            with mysql.connect(
                host=self.conexion["servidor"],
                user=self.conexion["usuario"],
                passwd=self.conexion["contrasenia"],
                database=self.conexion["database"]
            ) as db:
                with db.cursor() as cursor:
                    
                    # Consulta segura usando placeholders
                    query = "INSERT INTO post (tema, vender, url, url_image, publicada) VALUES (%s, %s, %s, %s, %s)"
                    values = (promo["titulo"], 1, promo["url"], promo["imagen"], 0)
                    
                    # Ejecutar la consulta
                    cursor.execute(query, values)
                    
                    # Confirmar los cambios
                    db.commit()
                    
                    # Retornar el id del último registro insertado
                    return cursor.lastrowid
            
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None