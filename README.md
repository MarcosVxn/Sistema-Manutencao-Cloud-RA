# Sistema de Manutenção Industrial Cloud com Realidade Aumentada (WebAR)

Projeto acadêmico desenvolvido para a disciplina de **Realidade Aumentada e Computação em Nuvem** da Faculdade de Tecnologia SENAI Antônio Adolpho Lobbe.

O sistema realiza o monitoramento IoT em tempo real de equipamentos industriais (Torno CNC e Furadeira Industrial), combinando arquitetura em nuvem, simulação de telemetria via MQTT, APIs REST em Flask, integração com ThingSpeak e visualização em Realidade Aumentada (WebAR).

---

## 🛠️ Tecnologias Utilizadas

### Backend & APIs

- **Python 3.10**
- **Flask**
- **Flask-CORS**
- **Gunicorn**
- **Requests**

### Mensageria IoT

- **MQTT**
- **Eclipse Mosquitto Broker**
- **Paho-MQTT**

### Plataforma Cloud & Telemetria

- **ThingSpeak**

### Containerização & Orquestração

- **Docker**
- **Docker Compose**

### Frontend / WebAR

- **HTML5**
- **CSS3**
- **JavaScript**
- **Fetch API**
- **AR.js**
- **A-Frame**

---
## 📁 Estrutura do Repositório

```text
Sistema-Manutencao-Cloud-RA/
│
├── backendCNC/                    # API REST Flask do Torno CNC + Integração ThingSpeak
│   ├── appCN.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── backendFrd/                    # API REST Flask da Furadeira Industrial
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── simuladorCNC/                  # Simulador de telemetria MQTT (Torno CNC)
│   ├── appCNC.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── SimuladorFrd/                  # Simulador de telemetria MQTT (Furadeira)
│   ├── appFrd.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── mqtt/                          # Configurações do Broker Mosquitto
│   └── mosquitto.conf
│
├── docs/                          # Documentação do projeto
│
├── frontend/                      # Aplicação WebAR (HTML/JS/CSS)
│   ├── assets/
│   ├── css/
│   ├── js/
│   └── index.html
│
├── compose.yaml                   # Orquestração dos microsserviços via Docker
│
└── README.md
```

### Descrição dos Diretórios

| Diretório | Descrição |
|---|---|
| `backendCNC/` | API REST Flask do Torno CNC e integração com ThingSpeak |
| `backendFrd/` | API REST Flask da Furadeira Industrial |
| `simuladorCNC/` | Simulador de telemetria MQTT do Torno CNC |
| `SimuladorFrd/` | Simulador de telemetria MQTT da Furadeira |
| `mqtt/` | Configurações do Broker Eclipse Mosquitto |
| `docs/` | Documentação do projeto |
| `frontend/` | Aplicação WebAR desenvolvida com HTML, CSS e JavaScript |
| `compose.yaml` | Orquestração dos microsserviços utilizando Docker Compose |

---
## 🚀 Arquitetura e Fluxo de Dados

O sistema realiza a integração entre os simuladores IoT, o broker MQTT, as APIs REST, a plataforma ThingSpeak e a aplicação WebAR.

### 1. Simulação de Sensores (IoT)

Os simuladores desenvolvidos em Python geram métricas industriais dinâmicas:

- Temperatura
- Vibração
- Status operacional

As informações são publicadas periodicamente no broker MQTT através de tópicos no formato:

```text
industria/<EQUIPAMENTO>/<METRICA>
```

### 2. Broker MQTT

O container `mosquitto_broker`, utilizando o **Eclipse Mosquitto**, centraliza e distribui as mensagens MQTT através da porta:

```text
1883
```

### 3. APIs Backend (Flask)

As APIs desenvolvidas em Flask recebem as métricas MQTT em segundo plano utilizando `paho-mqtt`.

Os dados de telemetria são atualizados em memória e disponibilizados através de endpoints REST para a interface WebAR.

### 4. Nuvem ThingSpeak

O backend do Torno CNC envia automaticamente as medições em tempo real para a plataforma **ThingSpeak**, utilizando chamadas HTTP REST.

### 5. Frontend WebAR

A aplicação WebAR consome os endpoints das APIs REST utilizando `fetch()` para obter os dados dos equipamentos.

As informações recebidas são utilizadas para renderizar hotspots dinâmicos e dados de telemetria sobre o marcador em Realidade Aumentada.

---
## 📊 Visualização de Telemetria (ThingSpeak)

O monitoramento remoto das métricas do Torno CNC (`CNC-01`) pode ser acompanhado ao vivo através do painel público do ThingSpeak:

- **Canal Público ThingSpeak:**  
  https://thingspeak.mathworks.com/channels/3516887

### Mapeamento dos Campos

| Campo | Informação |
|---|---|
| `Field 1` | Temperatura (°C) |
| `Field 2` | Vibração (mm/s) |
| `Field 3` | Status Operacional (`operando` / `alerta`) |

---
## ⚙️ Como Executar o Projeto

### Pré-requisitos

Antes de executar o projeto, certifique-se de possuir:

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado e em execução.
- [Git](https://git-scm.com/) instalado.

### Passos para Inicialização

#### 1. Clone o repositório

```bash
git clone https://github.com/MarcosVxn/Sistema-Manutencao-Cloud-RA.git
```

#### 2. Acesse o diretório do projeto

```bash
cd Sistema-Manutencao-Cloud-RA
```

#### 3. Inicie os serviços

```bash
docker compose up --build
```

O Docker Compose irá construir as imagens e iniciar os serviços definidos no arquivo `compose.yaml`.

---
## 🔗 Endpoints das APIs REST

### 🔩 Torno CNC (`CNC-01`) — Backend CNC

| Método | Endpoint | Descrição |
|---|---|---|
| `GET` | `/api/equipamentos/CNC-01` | Retorna dados cadastrais estáticos e status geral. |
| `GET` | `/api/equipamentos/CNC-01/telemetria` | Retorna a telemetria dinâmica em tempo real (JSON). |
| `GET` | `/health` | Healthcheck do serviço Flask. |

### 🔨 Furadeira Industrial (`FRD-01`) — Backend Furadeira

| Método | Endpoint | Descrição |
|---|---|---|
| `GET` | `/api/equipamentos/FRD-01` | Retorna identificação cadastral e hotspots da furadeira. |
| `GET` | `/api/equipamentos/FRD-01/telemetria` | Retorna telemetria simulada da furadeira em tempo real. |

---

## 🌐 Deploy do Frontend (WebAR)

A aplicação WebAR fica localizada no diretório:

```text
/frontend
```

Ela pode ser executada localmente ou acessada diretamente na nuvem através do **GitHub Pages**.

### GitHub Pages

https://marcosvxn.github.io/Sistema-Manutencao-Cloud-RA/

---
## 👥 Equipe do Projeto

### Marcos Vinicius

**Tech Lead & Backend Developer**

[GitHub — @MarcosVxn](https://github.com/MarcosVxn)

Responsabilidades:

- Liderança técnica do projeto.
- Arquitetura de software.
- Orquestração de microsserviços via Docker Compose.
- Estruturação da rede e broker MQTT.
- Desenvolvimento da API REST do Torno CNC (`CNC-01`).
- Desenvolvimento do simulador do Torno CNC.
- Integração com a nuvem do ThingSpeak.
- Configuração do deploy no GitHub Pages.

---

### Mikael Levi

**Backend Developer**

[GitHub — @MikaelLevi](https://github.com/MikaelLevi)

Responsabilidades:

- Desenvolvimento da API REST Flask referente ao módulo da Furadeira Industrial (`FRD-01`).
- Desenvolvimento do simulador de telemetria IoT referente ao módulo da Furadeira Industrial.

---

### Rhuan

**Frontend Developer**

[GitHub — @Rhuu4n](https://github.com/Rhuu4n)

Responsabilidades:

- Desenvolvimento da interface de usuário em Realidade Aumentada (WebAR).
- Renderização de modelos 3D.
- Consumo das APIs HTTP/REST.

---

## 📚 Contexto Acadêmico

Projeto desenvolvido como atividade acadêmica da disciplina de **Realidade Aumentada e Computação em Nuvem** da **Faculdade de Tecnologia SENAI Antônio Adolpho Lobbe**.

O projeto integra conceitos de:

- Internet das Coisas (IoT)
- Comunicação MQTT
- APIs REST
- Computação em Nuvem
- Docker
- Telemetria
- Realidade Aumentada
- Visualização de dados
- Arquitetura de microsserviços

---

## 📌 Status do Projeto

**Em desenvolvimento.**

O sistema possui integração entre os simuladores IoT, broker MQTT, backends Flask, ThingSpeak e frontend WebAR.
