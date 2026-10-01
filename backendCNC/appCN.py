import os
from datetime import datetime
from flask import Flask, jsonify
from flask_cors import CORS
import paho.mqtt.client as mqtt
import requests  # Importa a biblioteca para fazer chamadas HTTP

# A tua Write API Key do ThingSpeak
THINGSPEAK_WRITE_KEY = "SHIG9PDJH71881QA"

app = Flask(__name__)
CORS(app)  # Permite requisições do frontend WebAR sem bloqueio de segurança

def enviar_para_thingspeak(temperatura, vibracao, status):
    url = "https://api.thingspeak.com/update"
    
    # Mapeia os dados para os campos Field 1, Field 2 e Field 3 que configuraste
    payload = {
        'api_key': THINGSPEAK_WRITE_KEY,
        'field1': temperatura,
        'field2': vibracao,
        'field3': status
    }
    
    try:
        response = requests.get(url, params=payload, timeout=5)
        if response.status_code == 200 and response.text != '0':
            print(f"[THINGSPEAK] Dados enviados com sucesso! Resposta: {response.text}")
        else:
            print(f"[THINGSPEAK] Erro ou limite de taxa excedido (resposta: {response.text})")
    except Exception as e:
        print(f"[THINGSPEAK] Falha ao enviar dados: {e}")

# Configurações do Broker MQTT
MQTT_BROKER = os.getenv("MQTT_BROKER", "broker")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))

# Dados estáticos de cadastro do Torno CNC
CADASTRO_CNC = {
    "id": "CNC-01",
    "tipo": "Torno CNC",
    "setor": "Usinagem",
    "descricao": "Torno CNC de alta precisão para usinagem de peças cilíndricas.",
    "hotspots_estaticos": {
        "cabecote": "Cabeçote Principal / Placa de Fixação",
        "torre": "Torre Porta-Ferramentas de 8 Posições",
        "painel": "Painel de Comando Numérico Computadorizado",
        "protecao": "Carenagem e Porta de Proteção Industrial"
    }
}

# Armazenamento em memória da última telemetria recebida via MQTT
telemetria_cnc = {
    "temperatura": 0.0,
    "vibracao": 0.0,
    "status": "desconhecido",
    "atualizacao": "--:--:--"
}

# --- LÓGICA DO CLIENTE MQTT (SUBSCRIBER) ---

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("[BACKEND] Conectado ao Broker MQTT com sucesso!")
        # Assina apenas os tópicos do Torno CNC
        client.subscribe("industria/CNC-01/+")
    else:
        print(f"[BACKEND] Falha ao conectar no MQTT. Código de erro: {rc}")

def on_message(client, userdata, msg):
    try:
        # Exemplo de tópico recebido: industria/CNC-01/temperatura
        topico_partes = msg.topic.split('/')
        if len(topico_partes) == 3 and topico_partes[1] == "CNC-01":
            metrica = topico_partes[2]
            valor = msg.payload.decode("utf-8")

            if metrica == "temperatura":
                telemetria_cnc["temperatura"] = float(valor)
            elif metrica == "vibracao":
                telemetria_cnc["vibracao"] = float(valor)
            elif metrica == "status":
                telemetria_cnc["status"] = valor
                
                # ENVIA PARA O THINGSPEAK AQUI:
                # Dispara o envio ao ThingSpeak quando recebe o status
                enviar_para_thingspeak(
                    telemetria_cnc["temperatura"],
                    telemetria_cnc["vibracao"],
                    telemetria_cnc["status"]
                )

            # Atualiza o timestamp da última leitura recebida
            telemetria_cnc["atualizacao"] = datetime.now().strftime("%H:%M:%S")

    except Exception as e:
        print(f"[BACKEND] Erro ao processar mensagem MQTT: {e}")


def iniciar_mqtt():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()  # Executa a escuta do MQTT em uma thread separada
    except Exception as e:
        print(f"[BACKEND] Não foi possível conectar ao Broker MQTT no início: {e}")

# Inicializa o cliente MQTT junto com o backend
iniciar_mqtt()

# --- ENDPOINTS HTTP REST (FLASK) ---

@app.route('/api/equipamentos/CNC-01', methods=['GET'])
def obter_identificacao():
    """Retorna dados estáticos de identificação do Torno CNC."""
    resposta = CADASTRO_CNC.copy()
    resposta["status"] = telemetria_cnc["status"]
    return jsonify(resposta), 200


@app.route('/api/equipamentos/CNC-01/telemetria', methods=['GET'])
def obter_telemetria():
    """Retorna os dados dinâmicos de telemetria recebidos via MQTT."""
    return jsonify(telemetria_cnc), 200


@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint para checagem de saúde da API."""
    return jsonify({"status": "ok", "ativo": "CNC-01"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)