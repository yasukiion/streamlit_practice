import streamlit as st
# 別のファイルで定義された関数をインポート
from app import process_data

def process_data(selected_files):
    print(f"Received data: name={selected_files}")

process_data()

