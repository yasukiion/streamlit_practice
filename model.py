import streamlit as st
from session_state import get_state, SessionState
# 別のファイルで定義された関数をインポート
from app.py import process_data

def process_data(selected_files):
    print(f"Received data: name={selected_files}")

process_data()

