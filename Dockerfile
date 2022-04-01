FROM python:slim

RUN useradd app
WORKDIR /home/app

COPY requirements.txt requirements.txt
RUN python -m venv .env
RUN .env/bin/pip install -r requirements.txt
RUN .env/bin/pip install gunicorn pymysql cryptography
COPY app app
COPY migrations migrations
COPY config.py todo.py entrypoint.sh ./
RUN chmod +x entrypoint.sh

ENV FLASK_APP todo.py

RUN chown -R app:app ./

RUN mkdir /config && chown -R app:app /config

USER app
EXPOSE 5000
ENTRYPOINT ["./entrypoint.sh"]
