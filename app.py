from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin
from sistema_basado_reglas.sbr_principal import *

app = Flask(__name__)

CORS(app)
# Mysql Connection
app.config['MYSQL_HOST'] = 'bd-sbr-ia.ctl0hwzog7zq.us-east-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'Zacksykes.2018'
app.config['MYSQL_DB'] = 'sistema_de_reglas'
mysql = MySQL(app)

datos_usuario_temporal = []

@app.route('/')
def bienvenida():
    return jsonify({"bienvenida": "hola"})

@app.route("/agregar_usuario_temporal", methods=['POST'])
def agregar_usuario_temporal():
    #Se extraen los datos del POST, son específicamente 8 los cuales serán agregados a una lista global para ser manipulados
    datos_usuario = {
        'id_usuario': request.json['Id_usuario'],
        'nombre': request.json['Nombre'],
        'apellido': request.json['Apellido'],
        'respuesta_abdominal': request.json['Respuesta_abdominal'],
        'respuesta_diarrea': request.json['Respuesta_diarrea'],
        'respuesta_estrenimiento': request.json['Respuesta_estrenimiento'],
        'respuesta_acidez': request.json['Respuesta_acidez'],
        'respuesta_vomitos': request.json['Respuesta_vomitos']
    }

    datos_usuario_temporal.append(datos_usuario)

    Id_usuario = datos_usuario['id_usuario']
    Nombre = datos_usuario['nombre']
    Apellido = datos_usuario['apellido']
    Respuesta_abdominal = datos_usuario['respuesta_abdominal']
    Respuesta_diarrea = datos_usuario['respuesta_diarrea']
    Respuesta_estrenimiento = datos_usuario['respuesta_estrenimiento']
    Respuesta_acidez = datos_usuario['respuesta_acidez']
    Respuesta_vomitos = datos_usuario['respuesta_vomitos']
    Diagnostico_final = sbr(datos_usuario_temporal)

    print(Diagnostico_final)

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO Usuario_Respuestas (Id_usuario, Nombre, Apellido, Respuesta_abdominal, Respuesta_diarrea, Respuesta_estrenimiento, Respuesta_acidez, Respuesta_vomitos, Diagnostico_final) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (Id_usuario, Nombre, Apellido, Respuesta_abdominal, Respuesta_diarrea, Respuesta_estrenimiento, Respuesta_acidez, Respuesta_vomitos, Diagnostico_final))
    cur.close()
    datos_usuario_temporal.clear()
    mysql.connection.commit()
    print("Datos añadidos a la BD ")
    return jsonify({"informacion": "Registro exitoso del usuario y sus respuestas"})

@app.route("/respuesta_sbr/<id>", methods=['GET'])
def respuesta_sbr(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute(
            'SELECT * FROM Usuario_Respuestas WHERE Id_Usuario LIKE %s', [id])
        rv = cur.fetchall()
        cur.close()
        payload = []
        content = {}
        for result in rv:
            content = {"id_usuario": result[0], "Nombre": result[1], "Apellido": result[2], "Respuesta_abdominal": result[3], "Respuesta_diarrea": result[4],
                       "Respuesta_estrenimiento": result[5], "Respuesta_acidez": result[6], "Respuesta_vomitos": result[7], "Diagnostico_final": result[8]}
            payload.append(content)
            content = {}
        return jsonify(payload)
    except Exception as e:
        print(e)
        return jsonify({"informacion": e})

if __name__ == '__main__':
    app.run(debug=True, port=4000)
