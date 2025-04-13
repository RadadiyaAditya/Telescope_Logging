#!/bin/bash

echo "Activating virtual environment..."
source tele/bin/activate

echo "Starting Daphne server..."
daphne daphne -b 0.0.0.0 -p 8000 telescope_log.asgi:application &

echo "Opening project in browser..."
xdg-open http://127.0.0.1:8000 2>/dev/null || open http://127.0.0.1:8000