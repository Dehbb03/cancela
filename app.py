from flask import Flask, request, jsonify, render_template
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

# CONEXÃO COM BANCO DE DADOS
cred = credentials.Certificate("cancela-f0008-firebase-adminsdk-vf72o-73f406ccd2.json")
try:
    firebase_admin.initialize_app(cred)
    print('Conectado com o banco de dados com sucesso!')
except:
    print('Erro ao conectar com o banco de dados')

db = firestore.client()
cancela_reference = db.collection("Cancela")


# FUNÇÃO PARA REGISTRAR MOVIMENTAÇÃO
@app.route('/registro', methods=['POST'])
def registrar():
    data = request.get_json()
    tipo = data.get('tipo')
    if tipo not in ['Entrada', 'Saída']:
        return jsonify({'error': 'Tipo inválido, deve ser "Entrada" ou "Saída"'}), 400
    estacionamento = data.get('estacionamento')
    if estacionamento not in ['Ribeiro', 'Cardoso']:
        return jsonify({'error': 'Estacionamento inválido'}), 400
    registro = {
        'estacionamento': estacionamento,
        'tipo': tipo,
        'data': datetime.now().strftime(
            '%d-%m-%Y %H:%M:%S')}

    cancela_reference.add(registro)
    return jsonify({'message': 'Registro criado com sucesso'}), 201


# FUNÇÃO PARA LISTAR REGISTROS
@app.route('/registros', methods=['GET'])
def listar_registros():
    registros = cancela_reference.get()
    estacionamento = cancela_reference.get()
    entradas = 0
    saidas = 0
    novos_registros = []

    # CONTAGEM DE ENTRADAS E SAÍDAS
    for registro in registros:
        registro.to_dict()
        if registro.get("tipo") == "Entrada":
            entradas += 1
        elif registro.get("tipo") == "Saída":
            saidas += 1

        # SALVA OS CAMPOS EM novos_registros
        novos_registros.append({
            "id": registro.id,
            "estacionamento": registro.get("estacionamento"),
            "tipo": registro.get("tipo"),
            "data": registro.get("data")
        })

    return jsonify({
        'registros': novos_registros,
        'contagem': {
            'entradas': entradas,
            'saidas': saidas
        }
    })


# INTERFACE
@app.route('/')
def interface():
    return render_template('interface.html')


# PROGRAMA PRINCIPAL
if __name__ == '__main__':
    app.run()
