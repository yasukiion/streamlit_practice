import streamlit as st
from PIL import Image
import numpy as np
import os

# 指定されたディレクトリからすべての画像ファイルを取得する関数
def get_image_files(directory):
    image_extensions = {"png", "jpg", "jpeg", "gif", "bmp"}
    image_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(tuple(image_extensions)):
                image_files.append(os.path.join(root, file))
    return image_files

