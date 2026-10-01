# 1. Imagem base oficial do Python
FROM python:3.10-slim

# 2. Define o diretório de trabalho dentro do container
WORKDIR /app

# 3. Copia o ficheiro de dependências
COPY requirements.txt .

# 4. Instala as dependências (Flask, Flask-CORS, paho-mqtt, etc.)
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copia todo o código da pasta backendCNC para o container
COPY . .

# 6. Expõe a porta em que a API Flask vai rodar
EXPOSE 5000

# 7. Comando para iniciar a aplicação quando o container subir
CMD ["python", "appCN.py"]