#!/bin/bash

# MongoDB Data Path (where MongoDB will store its data)
MONGO_DB_PATH="/Users/abhishekkumar/Documents/Flask_Practice/e_commerce_project/mongodb-data"

# MongoDB Log Path
LOG_PATH="/Users/abhishekkumar/Documents/Flask_Practice/e_commerce_project/logs/mongo/mongodb.log"

# MongoDB PID File (to track running process)
PID_FILE="/Users/abhishekkumar/Documents/Flask_Practice/e_commerce_project/logs/mongo/mongod.pid"

case $1 in
  start)
    echo "Starting MongoDB..."
    mongod --dbpath "$MONGO_DB_PATH" --logpath "$LOG_PATH" --fork --pidfilepath "$PID_FILE" --port 27017
    echo "MongoDB started with PID $(cat $PID_FILE)."
    ;;
  stop)
    if [ -f "$PID_FILE" ]; then
      echo "Stopping MongoDB..."
      kill $(cat "$PID_FILE")
      rm -f "$PID_FILE"
      echo "MongoDB stopped."
    else
      echo "PID file not found. Is MongoDB running?"
    fi
    ;;
  restart)
    echo "Restarting MongoDB..."
    $0 stop
    $0 start
    ;;
  *)
    echo "Usage: $0 {start|stop|restart}"
    exit 1
    ;;
esac
