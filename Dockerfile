FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libssl-dev build-essential netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh


ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "backend.wsgi:application"]
