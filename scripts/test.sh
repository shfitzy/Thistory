#!/bin/bash
echo "Running all tests..."
PASS=0
FAIL=0

echo ""
echo "=== Backend Tests ==="
cd backend
source venv/bin/activate
python3 -m pytest -v
if [ $? -eq 0 ]; then
  PASS=$((PASS + 1))
else
  FAIL=$((FAIL + 1))
fi
deactivate
cd ..

echo ""
echo "=== Frontend Tests ==="
cd frontend
npm test -- --run
if [ $? -eq 0 ]; then
  PASS=$((PASS + 1))
else
  FAIL=$((FAIL + 1))
fi
cd ..

echo ""
echo "=== Results ==="
echo "Passed: $PASS/2 suites"
if [ $FAIL -gt 0 ]; then
  echo "Failed: $FAIL/2 suites"
  exit 1
fi
