#!/bin/sh
set -e

host="db"
user="todo_user"
db="todo_db"

echo "Waiting for Postgres to be ready..."
until pg_isready -h $host -U $user -d $db; do
  sleep 2
done

echo "Postgres is ready! Starting backend..."
exec "$@"
