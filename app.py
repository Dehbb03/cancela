from flask import Flask, request, jsonify, render_template
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

cred = credentials.Certificate("cancela-f0008-firebase-adminsdk-vf72o-73f406ccd2.json")
try:
    firebase_admin.initialize_app(cred)
    print('Conectado com o banco de dados com sucesso!')
except:
    print('Erro ao conectar com o banco de dados')

db = firestore.client()

cancela_reference = db.collection("Cancela")


# Função para registrar movimentação
@app.route('/registro', methods=['POST'])
def registrar():
    data = request.get_json()
    tipo = data.get('tipo')
    if tipo not in ['Entrada', 'Saída']:
        return jsonify({'error': 'Tipo inválido, deve ser "entrada" ou "saida"'}), 400  # Filtra apenas o input correto
    registro = {
        'tipo': tipo,
        'data': datetime.now().strftime(
            '%d-%m-%Y %H:%M:%S')}  # Registra a movimentação com seu tipo (entrada/saída) e o momento em que foi recebido o input

    cancela_reference.add(registro)  # Adiciona o registro à lista de registros

    return jsonify({'message': 'Registro criado com sucesso'}), 201


# Função para listar os registros (quantas entradas e quantas saídas houveram)
@app.route('/registros', methods=['GET'])
def listar_registros():
    registros = cancela_reference.get()
    entradas = 0
    saidas = 0
    novos_registros = []

    for registro in registros:
        registro.to_dict()
        if registro.get("tipo") == "Entrada":
            entradas += 1
        elif registro.get("tipo") == "Saída":
            saidas += 1

        # Save the required fields into novos_registros
        novos_registros.append({
            "id": registro.id,  # Get the document ID
            "tipo": registro.get("tipo"),  # Get the "tipo" field
            "data": registro.get("data")  # Get the "data" field
        })

    return jsonify({
        'registros': novos_registros,
        'contagem': {
            'entradas': entradas,
            'saidas': saidas
        }
    })


# Código da interface
@app.route('/')
def interface():
    return render_template('interface.html')


# Programa Principal
if __name__ == '__main__':
    app.run()
