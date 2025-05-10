#!/bin/bash
echo "📦 Installing Streamlit if not already installed..."
pip install streamlit --quiet

echo "🚀 Launching TeleSkill Ultra Dashboard..."
streamlit run app_streamlit_dashboard_ultra.py
