#!/bin/bash

echo "🚀 Iniciando HidroChat..."
echo

echo "📦 Instalando dependencias del backend..."
cd backend
pip install -r requirements-simple.txt
if [ $? -ne 0 ]; then
    echo "❌ Error instalando dependencias del backend"
    exit 1
fi

echo
echo "📦 Instalando dependencias del frontend..."
cd ../frontend
npm install
if [ $? -ne 0 ]; then
    echo "❌ Error instalando dependencias del frontend"
    exit 1
fi

echo
echo "🎯 Iniciando ambos servicios..."
cd ..
npm run dev





