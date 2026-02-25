#!/usr/bin/env bash
set -euo pipefail

# Base URLs
VULN_BASE="http://localhost:8081"
SEC_BASE="http://localhost:8082"

echo "[[ Health checks ]]"
curl -s "$VULN_BASE/health" | sed 's/.*/VULN: &/'
curl -s "$SEC_BASE/health"  | sed 's/.*/SEC : &/'
echo
echo

echo "[[ Vulnerable: admin stats without auth (should be 200) ]]"
curl -i -s "$VULN_BASE/admin/stats" | head -n 20
echo
echo

echo "[[ Secure: admin stats without auth (should be 401) ]]"
curl -i -s "$SEC_BASE/admin/stats" | head -n 20
echo
echo

echo "[[ Secure: login with invalid credentials (should be 401) ]]"
curl -i -s -X POST "$SEC_BASE/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"wrongpass"}' | head -n 20
echo
echo

echo "[[ Secure: login as alice (user role) and extract token ]]"
ALICE_TOKEN="$(curl -s -X POST "$SEC_BASE/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"alice123"}' \
  | python -c "import sys,json; print(json.load(sys.stdin)['access_token'])")"
echo "Alice token acquired"
echo
echo

echo "[[ Secure: access /items/search with missing token (should be 401) ]]"
curl -i -s -X POST "$SEC_BASE/items/search" \
  -H "Content-Type: application/json" \
  -d '{"query":"test","limit":10}' | head -n 20
echo
echo

echo "[[ Secure: access /items/search with invalid token (should be 401) ]]"
curl -i -s -X POST "$SEC_BASE/items/search" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer invalid.token.value" \
  -d '{"query":"test","limit":10}' | head -n 20
echo
echo

echo "[[ Secure: access /items/search with alice token (should be 200) ]]"
curl -i -s -X POST "$SEC_BASE/items/search" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ALICE_TOKEN" \
  -d '{"query":"test","limit":10}' | head -n 30
echo
echo

echo "[[ Secure: validation failure (limit too high) (should be 422 with safe body) ]]"
curl -i -s -X POST "$SEC_BASE/items/search" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ALICE_TOKEN" \
  -d '{"query":"test","limit":999}' | head -n 30
echo
echo

echo "[[ Vulnerable: reflected feedback (should echo input) ]]"
curl -i -s -X POST "$VULN_BASE/items/feedback" \
  -H "Content-Type: application/json" \
  -d '{"email":"attacker@example.com","feedback":"<script>alert(1)</script>"}' | head -n 40
echo
echo

echo "[[ Secure: feedback requires auth (should be 401 without token) ]]"
curl -i -s -X POST "$SEC_BASE/items/feedback" \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","feedback":"hello"}' | head -n 20
echo
echo

echo "[[ Secure: feedback with alice token (should be 200) ]]"
curl -i -s -X POST "$SEC_BASE/items/feedback" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ALICE_TOKEN" \
  -d '{"email":"user@example.com","feedback":"hello"}' | head -n 30
echo
echo

echo "[[ Vulnerable: login can self-assign admin role (should succeed) ]]"
curl -i -s -X POST "$VULN_BASE/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"evil","password":"anything","role":"admin"}' | head -n 40
echo
echo

echo "[[ Secure: admin endpoint with alice token (should be 403) ]]"
curl -i -s "$SEC_BASE/admin/stats" \
  -H "Authorization: Bearer $ALICE_TOKEN" | head -n 30
echo
echo

echo "[[ Secure: login as admin and access admin stats (should be 200) ]]"
ADMIN_TOKEN="$(curl -s -X POST "$SEC_BASE/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' \
  | python -c "import sys,json; print(json.load(sys.stdin)['access_token'])")"
curl -i -s "$SEC_BASE/admin/stats" \
  -H "Authorization: Bearer $ADMIN_TOKEN" | head -n 40
echo
echo

echo "[[ Secure: rate limiting test on /items/search (expect some 429) ]]"
for i in {1..20}; do
  code="$(curl -s -o /dev/null -w "%{http_code}" -X POST "$SEC_BASE/items/search" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $ALICE_TOKEN" \
    -d '{"query":"ratelimit","limit":1}')"
  echo "Request $i -> $code"
done
echo
echo

echo "Done."