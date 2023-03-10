import streamlit as st
import os
from PIL import Image
import shutil
import image_explore
import model
from model import cnn
from image2dataset import image_2_dataset
from zipfile import ZipFile
import tensorflow as tf

# フォルダのパスを指定
#予測用のフォルダ
UPLOAD_FOLDER = "./ceremony/uploads"
#学習用
DATA_FOLDER = "./ceremony/data"
#モデルの場所
MODEL_FOLDER = "./ceremony/my_model"

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
    #cnnのモデルに学習させる
    st.title("モデルに学習させますか？")
    if st.button("Click me"):
      cnn(DATA_FOLDER,MODEL_FOLDER)
      st.write("学習完了しました。cnnモデルは最新です")
    
    #新たなデータを使って予測する
    st.title("結婚式場の画像をアップロードしてください")
    # フォルダをアップロードする
    folder = st.file_uploader("Upload a folder", type="zip")
    if folder:
        # zipファイルを展開する
        path = os.path.join(os.getcwd(), folder.name)
        with open(path, "wb") as f:
            f.write(folder.getbuffer())
        os.makedirs(os.path.join(os.getcwd(), UPLOAD_FOLDER), exist_ok=True)
        shutil.unpack_archive(path, os.path.join(os.getcwd(),UPLOAD_FOLDER))
        st.write(path)

        #予測用のデータが入っているフォルダ
        PREDICTION_FOLDER = save_uploaded_file(folder)
        st.write(PREDICTION_FOLDER)

        # フォルダ内の画像を表示する
        image_extensions = ["jpg", "jpeg", "png"]
        image_folder = st.sidebar.selectbox("Select a folder", os.listdir(os.path.join(os.getcwd(),UPLOAD_FOLDER)))
        for file_name in os.listdir(os.path.join(os.path.join(os.getcwd(),UPLOAD_FOLDER, image_folder))):
            if file_name.split(".")[-1] in image_extensions:
                image_path = os.path.join(os.path.join(os.path.join(os.getcwd(),UPLOAD_FOLDER, image_folder)), file_name)
                image = Image.open(image_path)
                st.image(image, caption=file_name, use_column_width=True)
                file_path = save_uploaded_file(folder)
                st.write("Saved file:", PREDICTION_FOLDER)
        st.write(PREDICTION_FOLDER)

        # Zipファイルを展開する
        with ZipFile(folder, "r") as zip:
          zip.extractall(UPLOAD_FOLDER)
          os.remove(PREDICTION_FOLDER)
        shutil.rmtree("./ceremony/uploads/__MACOSX")

        # サブミットボタンでフォームをサブミットする
        form = st.form(key='my-form')
        submit_button = form.form_submit_button('Submit')
        if submit_button:
            #入力した画像をモデルが読み込める形に変える
            data = image_explore.get_image_files(PREDICTION_FOLDER)
            pre_dataset = image_2_dataset(PREDICTION_FOLDER)
            # モデルを読み込む
            loaded_model = tf.keras.models.load_model(MODEL_FOLDER)
            # モデルを使用して予測を行う
            #エポック数いらないよね？
            predictions = loaded_model.predict(pre_dataset)
            #csvに変換
            predictions.to_csv("predictions.csv",index=False)

if __name__ == "__main__":
    main()

