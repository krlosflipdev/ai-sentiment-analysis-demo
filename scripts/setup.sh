#!/bin/bash

set -e

echo "→ Installing npm dependencies..."
npm install

echo "→ Setting up backend Python environment..."
cd backend
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r requirements.txt
cd ..

echo "→ Setting up worker Python environment..."
cd worker
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r requirements.txt
cd ..

echo "✓ Setup complete! Run 'npm run dev' to start."
