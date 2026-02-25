#!/usr/bin/env bash
set -euo pipefail

# Simple demo flow:
# 1) Start containers
# 2) Show endpoints
# 3) Run attack script

echo "Starting containers..."
docker compose up -d --build

echo
echo "Services:"
echo "Vulnerable API via NGINX: http://localhost:8081/docs"
echo "Secure API via NGINX    : http://localhost:8082/docs"
echo

echo "Running curl tests..."
bash scripts/attack_examples.sh