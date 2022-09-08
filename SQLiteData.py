import sys
from tkinter.ttk import Separator
import zipfile #from zipfile import ZipFile
import pandas as pd
import sqlite3
from os import remove

basededatos = 'coches.db'

def consultar(conexion):
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM COCHES LIMIT 20')
    filas = cursor.fetchall()
    for fila in filas:
        print(fila)

def numeroCoches(conexion):
    cursor = conexion.cursor()
    cursor.execute('SELECT COUNT(*) FROM COCHES')
    dato = cursor.fetchall()
    numero = dato[0][0]
    return numero

def precioTotal(conexion):
    cursor = conexion.cursor()
    cursor.execute('SELECT SUM(Precio) FROM COCHES')
    dato = cursor.fetchall()
    precio = dato[0][0]
    return precio

def cocheBarato(conexion):
    cursor = conexion.cursor()
    cursor.execute("SELECT Marca, Modelo, MIN(Precio) FROM COCHES")
    barato = cursor.fetchall()
    print(f"El coche más barato es un {barato[0][0]} {barato[0][1]} por {barato[0][2]}€")

def precioMedioMarca(conexion):
    cursor = conexion.cursor()
    cursor.execute('SELECT Marca, AVG(Precio) FROM COCHES GROUP BY Marca')
    datos = cursor.fetchall()
    for i in datos:
        print(i[0], i[1])

def borrar_datos():
    try:
        remove(basededatos)
    except FileNotFoundError:
        pass

def descomprimir(archivo):
    with zipfile.ZipFile(archivo,'r') as zip:
        zip.extractall()

def leer_fichero(archivo):
    datos = pd.read_csv(archivo, delimiter=";")
    return datos

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print("Error numero de argumentos incorrecto: python3 SQLiteData.py <file>")
        exit()
    else: 

        borrar_datos()

        #Crear dataframe desde 
        fichero = sys.argv[1]
        descomprimir(fichero)
        datos = leer_fichero(fichero)
        print(datos)

        #Crear tabla SQLite
        try:
            conexion = sqlite3.connect("coches.db")
        except sqlite3.Error:
            print("Error al conectar base de datos")
        #Crear tabla:
        cursor = conexion.cursor()
        cursor.execute("CREATE TABLE COCHES(Marca TEXT, Modelo TEXT, Combustble TEXT, Transmision TEXT, Estado TEXT, Matriculacion INTEGRER, Kilometraje INTEGRER, Potencia INTEGRER, Precio INTEGRER)")
        conexion.commit()
        #Insertar varias filas:
        lista_elementos = datos.to_numpy().tolist()
        cursor.executemany("INSERT INTO COCHES VALUES (?,?,?,?,?,?,?,?,?)", lista_elementos)
        conexion.commit()

        consultar(conexion)
        print(f"El numero de coches es: {numeroCoches(conexion)}")
        print(f"El precio total de todos los coches es: {'{:,}'.format(precioTotal(conexion))}")
        cocheBarato(conexion)
        precioMedioMarca(conexion)
        cursor.close()