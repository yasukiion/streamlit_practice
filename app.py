import streamlit as st
import os
from PIL import Image
import shutil
import image_explore
import model
from model import cnn
from image_check import image_check
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
    if st.button("Train now!"):
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
        extract_path = os.path.join(os.getcwd(), UPLOAD_FOLDER)
        shutil.unpack_archive(path, extract_path)
        #shutil.rmtree(path)
        #os.remove(path)
        #予測用のデータが入っているzipファイル
        PREDICTION_ZIP = save_uploaded_file(folder)
        #予測用のデータが入っているフォルダ
        PREDICTION_FOLDER = os.path.join(extract_path, os.path.splitext(folder.name)[0])

        # Zipファイルを展開する
        with ZipFile(folder, "r") as zip:
          zip.extractall(UPLOAD_FOLDER)
          os.remove(PREDICTION_ZIP)
        shutil.rmtree("./ceremony/uploads/__MACOSX")

        st.title("画像をチェックする(任意)")
        if st.button("Check now!"):
            image_check(UPLOAD_FOLDER,PREDICTION_ZIP)

        # サブミットボタンでフォームをサブミットする
        st.title("予測を行います")
        form = st.form(key='my-form')
        submit_button = form.form_submit_button('Submit!')
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
        st.title("結果のダウンロード(csv)")

if __name__ == "__main__":
    main()

