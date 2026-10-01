# 1. Imagem base oficial do Python
FROM python:3.10-slim

# 2. Define o diretório de trabalho dentro do container
WORKDIR /app

# 3. Copia o ficheiro de dependências
COPY requirements.txt .

# 4. Instala as dependências (paho-mqtt)
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copia o código do simulador
COPY . .

# 6. Executa o script do simulador (repara que no teu print o ficheiro se chama appCNC.py)
CMD ["python", "appCNC.py"]