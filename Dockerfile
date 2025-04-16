FROM python:3.11.12-slim AS builder
WORKDIR /app

# Instalar dependencias del sistema necesarias para psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
  libpq-dev \
  gcc \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip && \
  pip install -r requirements.txt --no-cache-dir && \
  rm -rf /root/.cache/pip

COPY yana/. yana/
COPY .github/scripts/start.py start.py

# Ajustar permisos para el usuario no root
RUN chown -R 65534:65534 /app /usr/local/lib/python3.11/site-packages

# Etapa 2: Imagen final
FROM gcr.io/distroless/python3-debian12:nonroot AS final
WORKDIR /app

# Copiar los paquetes de Python
COPY --from=builder --chown=65534:65534 /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Copiar bibliotecas necesarias
COPY --from=builder /usr/lib/x86_64-linux-gnu/libpq.so* /usr/lib/x86_64-linux-gnu/
COPY --from=builder /usr/lib/x86_64-linux-gnu/libssl.so* /usr/lib/x86_64-linux-gnu/
COPY --from=builder /usr/lib/x86_64-linux-gnu/libcrypto.so* /usr/lib/x86_64-linux-gnu/
COPY --from=builder /lib/x86_64-linux-gnu/librt.so* /lib/x86_64-linux-gnu/

# Copiar el código de la aplicación
COPY --from=builder --chown=65534:65534 /app/yana /app/yana
COPY --from=builder --chown=65534:65534 /app/start.py /app/start.py

ENV PYTHONUNBUFFERED=1 \
  PORT=8000 \
  PYTHONPATH=/app:/app/yana:/usr/local/lib/python3.11/site-packages

CMD ["/app/start.py"]