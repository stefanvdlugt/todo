#!/bin/bash

PUID=${PUID:-0}
PGID=${PGID:-0}
export DATABASE_URL=${DATABASE_URL:-'sqlite:////config/app.db'}

groupadd -og ${PGID} app
useradd -og ${PGID} -M -d /config -u ${PUID} app

chown -R app:app /config

su -s /bin/bash app <<'EOF'
cd /app
source venv/bin/activate
echo ${DATABASE_URL}
echo ${SECRET_KEY}
while true; do
    flask db upgrade
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Upgrade command failed, retrying in 5 secs...
    sleep 5
done
exec gunicorn -b :5000 --access-logfile - --error-logfile - todo:app
EOF
