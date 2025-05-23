FROM python:3.11-slim

# Instalar Ghostscript
RUN apt-get update && apt-get install -y \
    ghostscript \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Instalar Flask directamente
RUN pip install --no-cache-dir flask

# Copiar el código de la app
COPY app.py .
COPY index.html .
COPY script.js .
COPY style.css .
COPY imagenes/ imagenes/

# Puerto para App Runner (usa el 8080 por defecto)
EXPOSE 8080

# Comando de inicio
CMD ["python", "app.py"]
