FROM python:slim

RUN mkdir /app; mkdir /config
WORKDIR /app
COPY app app/
COPY migrations migrations/
COPY config.py requirements.txt todo.py ./

ENTRYPOINT ["/bin/bash"]

RUN python -m venv venv && . venv/bin/activate && pip install -r requirements.txt

ENV FLASK_APP todo.py

EXPOSE 5000

COPY entrypoint.sh ./
RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
