import streamlit as st
import os

#フォルダ内の画像を表示する
def image_check(UPLOAD_FOLDER,PREDICTION_ZIP):
        image_extensions = ["jpg", "jpeg", "png"]
        image_folder = st.sidebar.selectbox("Select a folder", os.listdir(os.path.join(os.getcwd(),UPLOAD_FOLDER)))
        for file_name in os.listdir(os.path.join(os.path.join(os.getcwd(),UPLOAD_FOLDER, image_folder))):
            if file_name.split(".")[-1] in image_extensions:
                image_path = os.path.join(os.path.join(os.path.join(os.getcwd(),UPLOAD_FOLDER, image_folder)), file_name)
                image = Image.open(image_path)
                st.image(image, caption=file_name, use_column_width=True)
                st.write("Saved file:", PREDICTION_ZIP)