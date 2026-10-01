# Sistema de Manutenção Industrial Cloud com Realidade Aumentada (WebAR)

Projeto acadêmico desenvolvido para a disciplina de **Realidade Aumentada e Computação em Nuvem** da Faculdade de Tecnologia SENAI Antônio Adolpho Lobbe.

O sistema realiza o monitoramento IoT em tempo real de equipamentos industriais (Torno CNC e Furadeira Industrial) combinando arquitetura em nuvem, simulação de telemetria via MQTT, APIs REST em Flask, integração com ThingSpeak e visualização em Realidade Aumentada (WebAR).

---

## 🛠️ Tecnologias Utilizadas

- **Backend & APIs:** Python 3.10, Flask, Flask-CORS, Gunicorn, Requests
- **Mensageria IoT:** MQTT, Eclipse Mosquitto Broker, Paho-MQTT
- **Plataforma Cloud & Telemetria:** ThingSpeak
- **Containerização & Orquestração:** Docker & Docker Compose
- **Frontend / WebAR:** HTML5, CSS3, JavaScript (Fetch API, AR.js / A-Frame)

---

## 📁 Estrutura do Repositório

```text
Sistema-Manutencao-Cloud-RA/
├── backendCNC/          # API REST Flask do Torno CNC + Integração ThingSpeak
│   ├── appCN.py
│   ├── Dockerfile
│   └── requirements.txt
├── backendFrd/          # API REST Flask da Furadeira Industrial
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── simuladorCNC/        # Simulador de telemetria MQTT (Torno CNC)
│   ├── appCNC.py
│   ├── Dockerfile
│   └── requirements.txt
├── SimuladorFrd/        # Simulador de telemetria MQTT (Furadeira)
│   ├── appFrd.py
│   ├── Dockerfile
│   └── requirements.txt
├── mqtt/                # Configurações do Broker Mosquitto
│   └── mosquitto.conf
├── docs/                # Documentação do projeto
├── frontend/            # Aplicação WebAR (HTML/JS/CSS)
│   ├── assets/
│   ├── css/
│   ├── js/
│   └── index.html
├── compose.yaml         # Orquestração de todos os microsserviços via Docker
└── README.md
---

## 🚀 Arquitetura e Fluxo de Dados

1. **Simulação de Sensores (IoT):** Os simuladores em Python geram métricas industriais dinâmicas (temperatura, vibração e status) e publicam periodicamente no broker MQTT nos tópicos `industria/<EQUIPAMENTO>/<METRICA>`.
2. **Broker MQTT:** O container `mosquitto_broker` (Eclipse Mosquitto) centraliza e distribui a mensageria na porta `1883`.
3. **APIs Backend (Flask):** Ouvem as métricas MQTT em segundo plano via `paho-mqtt`, atualizam a telemetria em memória e servem os endpoints REST para a interface WebAR.
4. **Nuvem ThingSpeak:** O backend do Torno CNC despacha automaticamente as medições em tempo real via chamadas HTTP REST para a nuvem do ThingSpeak.
5. **Frontend WebAR:** Consome os endpoints das APIs REST via `fetch()` para renderizar os hotspots dinâmicos e os dados de telemetria sobre o marcador em Realidade Aumentada.

---

## 📊 Visualização de Telemetria (ThingSpeak)

O monitoramento remoto das métricas do Torno CNC (`CNC-01`) pode ser acompanhado ao vivo no painel público do ThingSpeak:

- **Canal Público ThingSpeak:** [Canal 3516887](https://thingspeak.mathworks.com/channels/3516887)
- **Mapeamento dos Campos:**
  - `Field 1`: Temperatura (°C)
  - `Field 2`: Vibração (mm/s)
  - `Field 3`: Status Operacional (`operando` / `alerta`)

---

## ⚙️ Como Executar o Projeto

### Pré-requisitos
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado e em execução.
- [Git](https://git-scm.com/) instalado.

### Passos para Inicialização

1. Clone o repositório:
   ```bash
   git clone [https://github.com/MarcosVxn/Sistema-Manutencao-Cloud-RA.git](https://github.com/MarcosVxn/Sistema-Manutencao-Cloud-RA.git)
   cd Sistema-Manutencao-Cloud-RA
---

## 🔗 Endpoints das APIs REST

### 🔩 Torno CNC (`CNC-01`) - Backend CNC
| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| `GET` | `/api/equipamentos/CNC-01` | Retorna dados cadastrais estáticos e status geral. |
| `GET` | `/api/equipamentos/CNC-01/telemetria` | Retorna a telemetria dinâmica em tempo real (JSON). |
| `GET` | `/health` | Healthcheck do serviço Flask. |

### 🔨 Furadeira Industrial (`FRD-01`) - Backend Furadeira
| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| `GET` | `/api/equipamentos/FRD-01` | Retorna identificação cadastral e hotspots da furadeira. |
| `GET` | `/api/equipamentos/FRD-01/telemetria` | Retorna telemetria simulada da furadeira em tempo real. |

---

## 🌐 Deploy do Frontend (WebAR)

A aplicação WebAR fica alocada no diretório `/frontend` e pode ser executada localmente ou acessada diretamente na nuvem via **GitHub Pages**:

- **URL do GitHub Pages:** `https://marcosvxn.github.io/Sistema-Manutencao-Cloud-RA/`

---

## 👥 Equipe do Projeto

- **Marcos Vinicius** ([@MarcosVxn](https://github.com/MarcosVxn)) – **Tech Lead & Backend Developer**
  - Liderança técnica do projeto, arquitetura de software, orquestração de microsserviços via Docker Compose, estruturação da rede e broker MQTT, desenvolvimento da API REST e simulador do Torno CNC (`CNC-01`),integração com a nuvem do ThingSpeak e configuração do deploy no GitHub Pages..
- **Mikael Levi** ([@MikaelLevi](https://github.com/MikaelLevi)) – **Backend Developer**
  - Desenvolvimento da API REST Flask e do simulador de telemetria IoT referente ao módulo da Furadeira Industrial (`FRD-01`).
- **Rhuan** ([@Rhuu4n](https://github.com/Rhuu4n)) – **Frontend Developer**
  - Desenvolvimento da interface de usuário em Realidade Aumentada (WebAR), renderização de modelos 3D, consumo das APIs HTTP/REST