import streamlit as st
# 別のファイルで定義された関数をインポート
from app import model
from PIL import Image
import numpy as np

def process_data(selected_files):
    print(f"Received data: name={model.selected_files}")
    for selected_file in selected_files:
        image = Image.open(selected_file).convert('L')  # convert to grayscale
        data = np.array(image)  # convert to numpy array
        st.image(data, caption=selected_file, use_column_width=True, format='JPEG')


