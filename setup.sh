#!/bin/bash
# TalentCore Systems Employee Directory Setup Script

echo "🚀 Setting up TalentCore Systems Employee Directory..."

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

echo "✅ Setup complete!"
echo "📝 Please edit .env file with your MySQL credentials"
echo "🗄️  Run database_setup.sql in your MySQL server"
echo "▶️  Start the application with: python app.py"