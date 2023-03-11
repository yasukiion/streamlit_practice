import streamlit as st
import os
import pandas as pd
from PIL import Image
import shutil
import image_explore
import model
from model import cnn
from image_check import image_check
from image2dataset import image_2_dataset
from zipfile import ZipFile
import tensorflow as tf
import datetime

# フォルダのパスを指定
#予測用のフォルダ
UPLOAD_FOLDER = "./ceremony/uploads"
#学習用
DATA_FOLDER = "./ceremony/data"
#モデルの場所
MODEL_FOLDER = "./ceremony/my_model"
#なぜか作られてしまうゴミフォルダ
MACOSX = "./ceremony/uploads/__MACOSX"
#csvファイルを保存するフォルダ
# 現在の日付を取得する
today = datetime.date.today()
# CSVファイル名に日付を付けて生成する
csvname = f"predictions_{today}.csv"
# CSVファイルの保存先ディレクトリのパスを指定する
save_dir = "/csv/"
# 保存先のパスとファイル名を結合する
csvpath = os.path.join(save_dir, csvname)

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
        if os.path.exists(path):
            os.remove(path)
        #予測用のデータが入っているzipファイル
        PREDICTION_ZIP = save_uploaded_file(folder)
        #予測用のデータが入っているフォルダ
        PREDICTION_FOLDER = os.path.join(extract_path, os.path.splitext(folder.name)[0])

        # Zipファイルを展開する
        with ZipFile(folder, "r") as zip:
          zip.extractall(UPLOAD_FOLDER)
          os.remove(PREDICTION_ZIP)
        if os.path.exists(MACOSX):
            shutil.rmtree(MACOSX)
        
        #画像の目視チェック
        st.title("画像のチェック(任意)")
        if st.button("Check now!"):
            image_check(UPLOAD_FOLDER,PREDICTION_FOLDER)

        # サブミットボタンでフォームをサブミットする
        st.title("予測を行います")
        form = st.form(key='my-form')
        submit_button = form.form_submit_button('Submit!')
        st.write(PREDICTION_FOLDER)
        if submit_button:
            #入力した画像をモデルが読み込める形に変える
            #data = image_explore.get_image_files(PREDICTION_FOLDER)
            pre_dataset, pre_filenames = image_2_dataset(PREDICTION_FOLDER)
            # モデルを読み込む
            loaded_model = tf.keras.models.load_model(MODEL_FOLDER)
            # モデルを使用して予測を行う
            predictions = loaded_model.predict(pre_dataset)
            # 予測結果をデータフレームに変換する
            predictions_df = pd.DataFrame({"filename":pre_filenames,"predicted_label":predictions.argmax(axis=1)})
            # csvファイルに保存するs
            predictions_df.to_csv(csvpath, index=False)
        st.title("結果のダウンロード(csv)")

if __name__ == "__main__":
    main()

