import os
import json
import threading
from datetime import datetime
from flask import Flask, jsonify
from flask\_cors import CORS
import paho.mqtt.client as mqtt

app = Flask(__name__)
CORS(app)

EQUIPAMENTOS = {
    "furadeira": {
        "id": "furadeira",
        "tipo": "Furadeira de Bancada Industrial",
        "setor": "Furação e Usinagem",
        "status": "operacional",
        "componentes": ["Cabeçote", "Mandril", "Mesa de Fixação", "Proteção de Segurança"]
    }
}

TELEMETRIA = {
    "furadeira": {
        "temperatura": 38.5,
        "vibracao": 1.4,
        "rotacao": 1200,
        "status": "operando",
        "atualizacao": datetime.now().strftime("%H:%M:%S")
    }
}

BROKER = os.getenv("MQTT_BROKER", "localhost")
PORT = int(os.getenv("MQTT_PORT", 1883))
TOPICO = "industria/+/+"

def on_message(client, userdata, msg):
    try:
        topico_partes = msg.topic.split("/")
        if len(topico_partes) >= 3:
            eq_id = topico_partes[1]
            dado_tipo  = topico_partes[2]
            payload_str = msg.payload.decode("utf-8")

            if eq_id not in TELEMETRIA:
                TELEMETRIA[eq_id] = {
                    "temperatura": 0.0, 
                    "vibracao0": 0.0, 
                    "rotacao": 0, 
                    "staus": "desconhecido", 
                    "atualizacao": "--"
                    }
            if payload_str.startswith("{"):
                dados = json.loads(payload_str)
                TELEMETRIA[eq_id].update(dados)

            else:
                if dado_tipo in ["temperatura", "vibracao"]:
                    TELEMETRIA[eq_id][dado_tipo] = float(payload_str)
                elif dado_tipo == "rotacao":
                        TELEMETRIA[eq_id][dado_tipo] = int(payload_str)
                else:
                    TELEMETRIA[eq_id][dado_tipo] = payload_str

            TELEMETRIA[eq_id]["atualizacao"] = datetime.now().strftime("%H:%M:%S")
            print(f"[MQTT] Telemetria atualizada para {eq_id}:
{TELEMETRIA[eq_id]}")
    except Exception as e:
        print(f"[MQTT Error] Erro ao processar mensagem: {e}")


def iniciar_mqtt():
    try:
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        client.on_message = on_message 
        client.connect(BROKER, PORT, keepalive=60) 
        client.subscribe(TOPICO) 
        print(f"[MQTT] Conectado ao broker no tópico '{TOPICO}'") 
        client.loop_forever()
    except Exception as e:
        print(f"[MQTT Warning] Não foi possível conectar ao broker ({e}). Usando 
dados em memória.")

thread_mqtt = threading.Thread(target=iniciar_mqtt, daemon=True)
thread_mqtt.start()

@app.route("/", methods=["GET"])
def healthcheck():
    return jsonify({
        "servico": "API REST - Suporte à Manutenção (Furadeira)",
        "status": "online"
    }), 200

@app.route("/api/equipamentos/<id_equipamento>", methods=["GET"])
def obter_equipamento(id_equipamento):
    equipamento = EQUIPAMENTOS.get(id_equipamento)
    if equipamento:
        return jsonify(equipamento), 200
    return jsonify({"erro": "Equipamento não encontrado"}), 404

@app.route("/api/equipamentos/<id_equipamento>/telemetria", methods=["GET"])
def obter_telemetria(id_equipamento):
    telemetria = TELEMETRIA.get(id_equipamento)
    if telemetria:
        return jsonify(telemetria), 200
    return jsonify({"erro": "Telemetria não encontrada para o equipamento informado"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)



