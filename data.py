import mysql.connector

db = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='InventarioEIE2409',
    database='inventarioeie'
)

mycursor = db.cursor()


mycursor.execute("CREATE TABLE Activos (placa int PRIMARY KEY, ubicacion TEXT(65535), tipo_de_activo TEXT(65535), ubicacion TEXT(65535))")