# todo
*a simple web application for keeping track of tasks*

- add, edit, and delete tasks
- set deadlines
- receive reminders by mail

## Installation and usage

### Using docker-compose (easiest)
Clone the repository:
```
git clone https://github.com/stefanvdlugt/todo.git
cd todo/
```
Rename/copy the file `todo.env.sample` to `todo.env` and edit it to set some application options.
Then run the following commands:
```
docker-compose build
docker-compose up -d
```
The application will listen on port 5000.

### Standalone, using Python
Clone the repository
```
git clone https://github.com/stefanvdlugt/todo.git
cd todo/
```
(Optionally) create and activate a virtual environment
```
python -m venv venv
source venv/bin/activate
```
Install dependencies
```
pip install -r requirements.txt
```
Rename/copy the file `todo.env.sample` to `todo.env` and edit it to set some application options.
Then run the application:
```
./run.sh
```
