import streamlit as st
# 別のファイルで定義された関数をインポート
from app import model

def process_data(selected_files):
    print(f"Received data: name={model.selected_files}")

