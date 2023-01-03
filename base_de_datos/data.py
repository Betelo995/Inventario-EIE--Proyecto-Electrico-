import mysql.connector

db = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='InventarioEIE2409',
    database='inventarioeie'
)

mycursor = db.cursor()

#Código para crear las columnas de la tabla
#mycursor.execute("CREATE TABLE Activos (placa int PRIMARY KEY, ubicacion TEXT(65535), tipo_de_activo TEXT(65535), descripcion TEXT(65535))")

'''
Con este código se aseguró que la tabla exista y que los elementos 
puestos anteriormente fueran correctos.

mycursor.execute("DESCRIBE Activos")

for j in mycursor:
    print(j)

'''


'''
Para insertar datos en la tabla se usa:

mycursor.execute("INSERT INTO Activos (placa, ubicacion, tipo_de_activo, descripcion) VALUES (%s, %s, %s, %s)", (260255, "Sala de estudio EIE", "Silla", "Silla negra con rodines"))

db.commit()
'''

#Ahora vamos a obtener todos los datos que tenemos actualmente en la tabla

#mycursor.execute("SELECT * FROM Activos")

#for j in mycursor:
#    print(j)


#para ver si algun dato se encuentra en la base de datos:

mycursor.execute("SELECT * FROM Activos")
is_on = False
for j in mycursor:
    if j[0] == 260255:
        is_on = True
    else:
        pass

if is_on == True:
    print("Funcionó")

#Para extraer los datos de la base para una placa específica.

mycursor.execute("SELECT * FROM Activos WHERE placa = (%s)", (260255,)) #Hay que usar la coma al final si es solo  un elemento para que sea un tuple

for j in mycursor:
    print(j)

#Como modificar un valor específico

mycursor.execute("UPDATE Activos SET ubicacion = %s, descripcion = %s WHERE placa = %s", ("secretaria", "Silla sin ruedas", 260255))


#Solo compruba que si se hizo el update. En la aplicación vamos a updatear todos los valores en caso
#De que si se haya registrado anteriormente el activo
mycursor.execute("SELECT * FROM Activos")

for j in mycursor:
    print(j)