from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Lista para armazenar os registros em memória
registros = []


# Função para registrar movimentação
@app.route('/registro', methods=['POST'])
def registrar():
    data = request.get_json()
    tipo = data.get('tipo')
    if tipo not in ['entrada', 'saida']:
        return jsonify({'error': 'Tipo inválido, deve ser "entrada" ou "saida"'}), 400  # Filtra apenas o input correto
    registro = {
        'tipo': tipo,
        'timestamp': datetime.now().strftime('%d-%m-%Y %H:%M:%S')}  # Registra a movimentação com seu tipo (entrada/saída) e o momento em que foi recebido o input

    registros.append(registro) # Adiciona o registro à lista de registros

    return jsonify({'message': 'Registro criado com sucesso'}), 201


# Função para listar os registros (quantas entradas e quantas saídas houveram)
@app.route('/registros', methods=['GET'])
def listar_registros():
    entradas = sum(1 for r in registros if r['tipo'] == 'entrada')  # Adiciona ao número de entradas
    saidas = sum(1 for r in registros if r['tipo'] == 'saida')  # Adiciona o número de saídas
    return jsonify({
        'registros': registros,
        'contagem': {
            'entradas': entradas,
            'saidas': saidas
        }
    })


# Código da interface
@app.route('/')
def index():
    return """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Registros de Entrada/Saída</title>
        <script>
            async function fetchRegistros() {
                const response = await fetch('/registros');
                const data = await response.json();
                const registrosDiv = document.getElementById('registros');
                const entradasCount = document.getElementById('entradasCount');
                const saidasCount = document.getElementById('saidasCount');

                registrosDiv.innerHTML = data.registros.map(r => `<p>${r.tipo} - ${r.timestamp}</p>`).join('');
                entradasCount.innerText = data.contagem.entradas;
                saidasCount.innerText = data.contagem.saidas;
            }

            window.onload = function() {
                fetchRegistros();
                setInterval(fetchRegistros, 5000); // Atualiza a cada 5 segundos
            };
        </script>
    </head>
    <body>
        <h1>Registros de Entrada/Saída</h1>       
        <div id="registros"></div>
        <div>
            <p>Entradas: <span id="entradasCount">0</span></p>
            <p>Saídas: <span id="saidasCount">0</span></p>
        </div>
    </body>
    </html>
    """


# Programa Principal
if __name__ == '__main__':
    app.run(debug=True)
