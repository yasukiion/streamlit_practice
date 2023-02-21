import streamlit as st
import os
from PIL import Image
import shutil
import model

# フォルダのパスを指定
UPLOAD_FOLDER = "./uploads"

def save_uploaded_file(uploaded_file):
    # フォルダが存在しない場合は作成する
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    # ファイルを保存する
    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def main():
    st.title("結婚式場の画像をアップロードしてください")

    # フォルダをアップロードする
    folder = st.file_uploader("Upload a folder", type="zip")
    UPLOAD_FOLDER = "./uploads"
    if folder:
        # zipファイルを展開する
        path = os.path.join(os.getcwd(), folder.name)
        with open(path, "wb") as f:
            f.write(folder.getbuffer())
        os.makedirs(os.path.join(os.getcwd(), UPLOAD_FOLDER), exist_ok=True)
        shutil.unpack_archive(path, os.path.join(os.getcwd(),UPLOAD_FOLDER))
        os.remove(path)

        # フォルダ内の画像を表示する
        image_extensions = ["jpg", "jpeg", "png"]
        image_folder = st.sidebar.selectbox("Select a folder", os.listdir(os.path.join(os.getcwd(),UPLOAD_FOLDER)))
        for file_name in os.listdir(os.path.join(os.path.join(os.getcwd(),UPLOAD_FOLDER, image_folder))):
            if file_name.split(".")[-1] in image_extensions:
                image_path = os.path.join(os.path.join(os.path.join(os.getcwd(),UPLOAD_FOLDER, image_folder)), file_name)
                image = Image.open(image_path)
                st.image(image, caption=file_name, use_column_width=True)
                file_path = save_uploaded_file(folder)
                st.write("Saved file:", file_path)
                #selected_files.append(file_path)

        # サブミットボタンでフォームをサブミットする
        form = st.form(key='my-form')
        submit_button = form.form_submit_button('Submit')
        if submit_button:
            selected_files = [file_name for file_name in os.listdir(os.path.join(os.getcwd(),UPLOAD_FOLDER, image_folder)) if file_name.split(".")[-1] in image_extensions]
            st.write(selected_files)
            model.process_data(selected_files)

if __name__ == "__main__":
    main()

