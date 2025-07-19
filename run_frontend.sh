#!/bin/bash

# Install dependencies if not already installed
echo "Installing Node.js dependencies..."
cd frontend
npm install

# Start React development server
echo "Starting Air Traffic Control Frontend..."
npm start 