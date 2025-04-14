#!/bin/bash

# Exit immediately if a command fails
set -e

echo "🚀 Starting setup.sh..."

# 🐧 Update apt and install system dependencies
echo "🔧 Updating apt and installing system packages (Python & ffmpeg)..."
apt-get update && apt-get install -y python3 python3-pip ffmpeg

# 🐍 Install each Python dependency individually
echo "🐍 Installing torch..."
pip3 install torch

echo "🐍 Installing faiss-cpu..."
pip3 install faiss-cpu

echo "🐍 Installing numpy..."
pip3 install numpy

echo "🐍 Installing pydub..."
pip3 install pydub

echo "🐍 Installing sentence-transformers..."
pip3 install sentence-transformers

echo "🐍 Installing transformers..."
pip3 install transformers

echo "🐍 Installing edge-tts..."
pip3 install edge-tts

echo "🐍 Installing colorama..."
pip3 install colorama

# 🟢 Install Node.js dependencies
echo "📦 Installing Node.js packages..."
npm install

echo "✅ All setup steps completed successfully!"
