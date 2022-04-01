# todo
*a simple web application for keeping track of tasks*

- add, edit, and delete tasks
- set deadlines
- receive reminders by mail

## Installation and usage
Copy/rename the file `.env.sample` to `.env` and adjust settings.

### Using docker-compose (easiest)
Run the following commands:
    git clone https://github.com/stefanvdlugt/todo.git
    cd todo/
    docker-compose build
    docker-compose up -d

### Using Docker
Run the following commands:
    git clone https://github.com/stefanvdlugt/todo.git
    cd todo/
    docker build -t todoapp .
    

### Standalone, using Python
Make sure you have a working installation of Python 3 with `pip` (and optionally `venv`) installed, and run
    git clone https://github.com/stefanvdlugt/todo.git
    cd todo/
    cp .env.sample .env
    # edit settings using your editor of choice:
    vi .env
    # optionally, if venv is installed:
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    flask db upgrade
    gunicorn -b :5000 --access-logfile - --error-logfile - todo:app


