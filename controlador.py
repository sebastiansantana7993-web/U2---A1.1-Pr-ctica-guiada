import pymysql.cursors
from models.bd import obtener_conexion
from werkzeug.security import generate_password_hash

#  VALIDAR USUARIO 
def validar_usuario(correo):
    """Devuelve un diccionario con los datos del usuario dado su correo"""
    conexion = obtener_conexion()
    usuario = None
    try:
        with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT * FROM usuarios WHERE correo=%s", (correo,))
            usuario = cursor.fetchone()
    finally:
        conexion.close()
    return usuario

#  OBTENER USUARIOS 
def obtener_usuarios():
    conexion = obtener_conexion()
    usuarios = []
    with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("SELECT id, nombre, apellido, carrera, correo, estatus FROM usuarios")
        usuarios = cursor.fetchall()
    conexion.close()
    return usuarios

#  INSERTAR USUARIO 
def insertar_usuario(nombre, apellido, carrera, correo, password, estatus):
    """Inserta un usuario nuevo con password hasheada. Devuelve False si el correo ya existe."""
    conexion = obtener_conexion()
    with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
        # Validar si ya existe el correo
        cursor.execute("SELECT id FROM usuarios WHERE correo = %s", (correo,))
        existe = cursor.fetchone()
        if existe:
            conexion.close()
            return False  # El correo ya existe
        
        pw_hash = generate_password_hash(password)  # 🔑 hash de la contraseña
        cursor.execute(
            "INSERT INTO usuarios(nombre, apellido, carrera, correo, password, estatus) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (nombre, apellido, carrera, correo, pw_hash, estatus),
        )
    conexion.commit()
    conexion.close()
    return True

#  OBTENER USUARIO POR ID 
def obtener_usuario_por_id(id):
    """Devuelve un usuario según su id"""
    conexion = obtener_conexion()
    usuario = None
    with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute(
            "SELECT id, nombre, apellido, correo, carrera, estatus FROM usuarios WHERE id = %s",
            (id,)
        )
        usuario = cursor.fetchone()
    conexion.close()
    return usuario

# ACTUALIZAR USUARIO 
def actualizar_usuario(id, nombre, apellido, carrera, correo, password, estatus):
    """Actualiza los datos de un usuario. Password se hashea si se recibe."""
    conexion = obtener_conexion()
    with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
        pw_hash = generate_password_hash(password) if password else None
        if pw_hash:
            cursor.execute(
                "UPDATE usuarios SET nombre=%s, apellido=%s, carrera=%s, correo=%s, password=%s, estatus=%s WHERE id=%s",
                (nombre, apellido, carrera, correo, pw_hash, estatus, id)
            )
        else:
            cursor.execute(
                "UPDATE usuarios SET nombre=%s, apellido=%s, carrera=%s, correo=%s, estatus=%s WHERE id=%s",
                (nombre, apellido, carrera, correo, estatus, id)
            )
    conexion.commit()
    conexion.close()

#  ELIMINAR USUARIO 
def eliminar_usuario(id):
    """Elimina un usuario por su ID"""
    conexion = obtener_conexion()
    with conexion.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute("DELETE FROM usuarios WHERE id = %s", (id,))
    conexion.commit()
    conexion.close()
