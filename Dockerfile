FROM python:3.11.15-slim-trixie

WORKDIR /app

COPY . /app

EXPOSE ${APP_PORT}

VOLUME [ "/var/lib/postgresql/data" ]

ENTRYPOINT [ "python" ]

CMD [ "-m", "src.taskmanager.main"]

RUN pip install -q --no-cache-dir -r ./requirements.txt









