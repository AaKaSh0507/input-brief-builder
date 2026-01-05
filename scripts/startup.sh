#!/bin/bash

echo "=========================================="
echo "GPJ INPUT BRIEF ASSISTANT - STARTUP"
echo "=========================================="
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Install PostgreSQL if missing
if ! command_exists psql; then
    echo "📦 Installing PostgreSQL..."
    apt-get update > /dev/null 2>&1
    apt-get install -y postgresql postgresql-contrib > /dev/null 2>&1
    echo "✅ PostgreSQL installed"
else
    echo "✅ PostgreSQL already installed"
fi

# Install Redis if missing
if ! command_exists redis-cli; then
    echo "📦 Installing Redis..."
    apt-get install -y redis-server > /dev/null 2>&1
    echo "✅ Redis installed"
else
    echo "✅ Redis already installed"
fi

echo ""
echo "🚀 Starting services..."
echo ""

# Start PostgreSQL
echo "▶️  Starting PostgreSQL..."
sudo -u postgres pg_ctlcluster 15 main start 2>&1 | grep -v "already running" || echo "   PostgreSQL started"

# Create database if doesn't exist
echo "▶️  Checking database..."
sudo -u postgres psql -lqt 2>/dev/null | cut -d \| -f 1 | grep -qw gpj_briefs
if [ $? -ne 0 ]; then
    sudo -u postgres psql -c "CREATE DATABASE gpj_briefs;" 2>/dev/null
    sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD 'postgres';" 2>/dev/null
    echo "   ✅ Database created"
else
    echo "   ✅ Database exists"
fi

# Start Redis
echo "▶️  Starting Redis..."
redis-server --daemonize yes 2>/dev/null
sleep 1
redis-cli ping > /dev/null 2>&1 && echo "   ✅ Redis running" || echo "   ⚠️  Redis failed to start"

# Restart backend
echo "▶️  Restarting Backend..."
sudo supervisorctl restart backend > /dev/null 2>&1
sleep 3

# Restart frontend
echo "▶️  Restarting Frontend..."
sudo supervisorctl restart frontend > /dev/null 2>&1
sleep 2

echo ""
echo "=========================================="
echo "HEALTH CHECK"
echo "=========================================="
echo ""

# Check backend health
echo "🔍 Testing Backend API..."
BACKEND_HEALTH=$(curl -s http://localhost:8001/api/health 2>/dev/null)
if [ $? -eq 0 ]; then
    echo "   ✅ Backend is healthy"
    echo "   Response: $BACKEND_HEALTH"
else
    echo "   ❌ Backend is not responding"
    echo "   Check logs: tail -50 /var/log/supervisor/backend.err.log"
fi

# Check frontend
echo ""
echo "🔍 Testing Frontend..."
FRONTEND_TEST=$(curl -s http://localhost:3000/ 2>/dev/null | grep -o "<title>.*</title>")
if [ $? -eq 0 ]; then
    echo "   ✅ Frontend is running"
    echo "   Title: $FRONTEND_TEST"
else
    echo "   ❌ Frontend is not responding"
    echo "   Check logs: tail -50 /var/log/supervisor/frontend.err.log"
fi

# Check database
echo ""
echo "🔍 Testing Database..."
DB_TEST=$(sudo -u postgres psql -d gpj_briefs -c "SELECT COUNT(*) FROM briefs;" 2>/dev/null)
if [ $? -eq 0 ]; then
    echo "   ✅ Database is accessible"
else
    echo "   ❌ Database connection failed"
fi

# Check Redis
echo ""
echo "🔍 Testing Redis..."
REDIS_TEST=$(redis-cli ping 2>/dev/null)
if [ "$REDIS_TEST" = "PONG" ]; then
    echo "   ✅ Redis is running"
else
    echo "   ❌ Redis connection failed"
fi

echo ""
echo "=========================================="
echo "SERVICE STATUS"
echo "=========================================="
echo ""
sudo supervisorctl status | grep -E "(backend|frontend|mongodb)"

echo ""
echo "=========================================="
echo "✅ STARTUP COMPLETE"
echo "=========================================="
echo ""
echo "📍 Frontend: http://localhost:3000"
echo "📍 Backend API: http://localhost:8001/api"
echo "📍 API Docs: http://localhost:8001/docs"
echo "📍 Health Check: http://localhost:8001/api/health"
echo ""
echo "📚 Documentation:"
echo "   - README.md"
echo "   - API_DOCUMENTATION.md"
echo "   - PROJECT_SUMMARY.md"
echo ""
echo "🔑 Configured Keys:"
echo "   ✅ Emergent LLM Key (AI)"
echo "   ✅ PostgreSQL Database"
echo "   ✅ Redis Cache"
echo "   ⚠️  Google Sheets (Optional - add credentials)"
echo ""
