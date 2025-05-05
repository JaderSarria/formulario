from flask import Flask, request, render_template, jsonify
import json
from datetime import datetime
import os

app = Flask(__name__, template_folder='.')

# Nombre del archivo JSON único
ARCHIVO_UNICO = 'canciones.json'

@app.route('/')
def mostrar_formulario():
    return render_template('formulario.html')

@app.route('/guardar_respuesta', methods=['POST'])
def guardar_respuesta():
    if request.method == 'POST':
        himnario = request.form['himnario']
        numero = request.form.get('numero') # Usamos .get() porque puede no estar presente
        nombre_cancion = request.form['nombre_cancion']
        tono = request.form['tono']
        ocasion = request.form['ocasion']
        letra = request.form['letra']

        nueva_cancion = {
            "himnario": himnario,
            "nombre_cancion": nombre_cancion,
            "tono": tono,
            "ocasion": ocasion,
            "letra": letra
        }

        # Agregar el número solo si se proporcionó
        if himnario != 'no' and numero:
            nueva_cancion["numero"] = numero

        try:
            with open(ARCHIVO_UNICO, 'r') as f:
                datos_existentes = json.load(f)
                if isinstance(datos_existentes, list):
                    datos_existentes.append(nueva_cancion)
                else:
                    datos_existentes = [nueva_cancion]
        except FileNotFoundError:
            datos_existentes = [nueva_cancion]
        except json.JSONDecodeError:
            datos_existentes = [nueva_cancion]

        with open(ARCHIVO_UNICO, 'w') as f:
            json.dump(datos_existentes, f, indent=4)

        return "¡Canción guardada en el archivo!"

    return "Método no permitido"

if __name__ == '__main__':
    app.run(debug=True)