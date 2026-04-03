FROM python:3.11.15-slim-trixie

ARG WORKDIR

# No genera archivos .pyc (innecesarios en contenedor)
ENV PYTHONDONTWRITEBYTECODE=1
# No bufferiza stdout/stderr (logs en tiempo real)
ENV PYTHONUNBUFFERED=1
# No comprueba si hay versión más nueva de pip (más rápido)
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

EXPOSE 8080

WORKDIR $WORKDIR/app

COPY requirements.txt README.md ./files/
RUN cd files && \
    pip install -q --no-cache-dir -r requirements.txt
COPY ./src ./src
COPY ./tests ./tests/

CMD [ "python", "-m", "src.taskmanager.main"]











