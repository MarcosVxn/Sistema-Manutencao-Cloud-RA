import os
import time
import random
import paho.mqtt.client as mqtt

# Configurações do Broker MQTT (lidas de variáveis de ambiente do Docker Compose)
MQTT_BROKER = os.getenv("MQTT_BROKER", "broker")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))

EQUIPAMENTO_ID = "CNC-01"

def conectar_mqtt():
    client = mqtt.Client()
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        print(f"[SIMULADOR] Conectado ao Broker MQTT em {MQTT_BROKER}:{MQTT_PORT}")
        return client
    except Exception as e:
        print(f"[SIMULADOR] Aguardando Broker MQTT... ({e})")
        return None

def rodar_simulador():
    client = conectar_mqtt()
    
    # Tentativa de reconexão automática se o broker demorar a subir no container
    while client is None:
        time.sleep(3)
        client = conectar_mqtt()

    print(f"[SIMULADOR] Iniciando envio de telemetria para o ativo: {EQUIPAMENTO_ID}")
    
    while True:
        try:
            # Geração de dados simulados (didáticos) para o Torno CNC
            temp = round(random.uniform(40.0, 55.0), 1)
            vibracao = round(random.uniform(1.2, 3.8), 2)
            status = random.choice(["operando", "operando", "operando", "alerta"])

            topic_prefix = f"industria/{EQUIPAMENTO_ID}"
            
            # Publicação nos tópicos MQTT conforme o requisito do projeto
            client.publish(f"{topic_prefix}/temperatura", temp)
            client.publish(f"{topic_prefix}/vibracao", vibracao)
            client.publish(f"{topic_prefix}/status", status)

            print(f"[SIMULADOR] [{EQUIPAMENTO_ID}] Temp: {temp}°C | Vib: {vibracao} mm/s | Status: {status}")

            time.sleep(5)  # Envia novas leituras a cada 5 segundos

        except Exception as e:
            print(f"[SIMULADOR] Erro ao enviar telemetria: {e}")
            time.sleep(3)

if __name__ == "__main__":
    rodar_simulador()