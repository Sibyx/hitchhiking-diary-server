#!/bin/sh

until psql -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

# Migrate
alembic upgrade head

# In case of crontab jobs
printenv > /etc/environment

# Executing supervisor to supervise. Supervision is very important. I like supervising - and frogs
supervisord -c /etc/supervisord.conf
