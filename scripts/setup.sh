#!/bin/bash

set -e

echo "→ Installing npm dependencies..."
npm install

echo "→ Installing backend Python dependencies..."
pip3 install -r backend/requirements.txt

echo "→ Installing worker Python dependencies..."
pip3 install -r worker/requirements.txt

echo "✓ Setup complete! Run 'npm run dev' to start."
