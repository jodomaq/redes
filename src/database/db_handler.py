import mysql.connector as mysql
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
                    query = "INSERT INTO ventas (titulo, url, imagen, precio, url_afiliados, publicada) VALUES (%s, %s, %s, %s, %s, %s)"
                    values = (promo["titulo"], promo["url"], promo["imagen"], promo["precio"], promo["url_afiliados"], 0)
                    
                    # Ejecutar la consulta
                    cursor.execute(query, values)
                    
                    # Confirmar los cambios
                    db.commit()
                    
                    # Retornar el id del último registro insertado
                    return cursor.lastrowid
            
        except Exception as err:
            print(f"Error: {err}")
            return None


