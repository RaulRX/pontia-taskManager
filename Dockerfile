FROM python:3.11.15-slim-trixie

WORKDIR /app

COPY . /app

# No genera archivos .pyc (innecesarios en contenedor)
ENV PYTHONDONTWRITEBYTECODE=1
# No bufferiza stdout/stderr (logs en tiempo real)
ENV PYTHONUNBUFFERED=1
# No comprueba si hay versión más nueva de pip (más rápido)
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

EXPOSE ${APP_PORT}

VOLUME [ "/var/lib/postgresql/data" ]

ENTRYPOINT [ "python" ]

CMD [ "-m", "src.taskmanager.main"]

RUN pip install -q --no-cache-dir -r ./requirements.txt









