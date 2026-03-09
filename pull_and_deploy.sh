#!/bin/bash


set -e

echo "Stopping existing containers..."
sudo docker compose down || true

echo "Removing old mysql container if it exists..."
sudo docker rm -f mysql_container || true

echo "Pulling latest images..."
sudo docker compose pull

echo "Starting containers..."
sudo docker compose up -d

echo "Deployment successful!"