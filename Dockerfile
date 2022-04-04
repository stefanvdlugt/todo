FROM python:slim

# Create application directory
RUN mkdir /app
WORKDIR /app

# Copy requirements file and install requirements
COPY requirements.txt ./
RUN python -m venv venv && . venv/bin/activate && pip install -r requirements.txt

# Copy application files
COPY app app/
COPY migrations migrations/
COPY config.py todo.py entrypoint.sh ./
RUN chmod +x entrypoint.sh

ENV FLASK_APP todo.py
EXPOSE 5000

ENV BASEDIR=/config/

ENTRYPOINT ["./entrypoint.sh"]
