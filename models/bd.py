import pymysql

def obtener_conexion():
    return pymysql.connect(
        host='localhost',
        user='root', 
        password='23Febreroo', 
        db='orcoweb',
        autocommit=True
        )