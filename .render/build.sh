#!/bin/bash

# Exit immediately if a command fails
set -e

echo "🚀 Starting setup.sh..."

# 🐧 Update apt and install system dependencies
echo "🔧 Updating apt and installing system packages (Python & ffmpeg)..."
apt-get update && apt-get install -y python3 python3-pip ffmpeg

# 🐍 Install Python dependencies
echo "🐍 Installing Python packages from requirements.txt..."
pip3 install -r requirements.txt

# 🟢 Install Node.js dependencies
echo "📦 Installing Node.js packages..."
npm install

echo "✅ All setup steps completed successfully!"
