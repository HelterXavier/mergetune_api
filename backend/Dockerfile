# backend/Dockerfile
FROM python:3.12-slim

# Evita arquivos .pyc
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Define o diretório padrão dentro do container
WORKDIR /app

# Copia as dependências e instala
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia o restante do código
COPY . .

# Expõe a porta padrão do Django
EXPOSE 8000

# Comando padrão para subir o servidor de desenvolvimento do Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]