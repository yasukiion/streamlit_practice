import streamlit as st
import os
import pandas as pd
from PIL import Image
import shutil
import image_explore
import tensorflow as tf
import datetime
from model import cnn
from image_check import image_check
from image2dataset import image_2_dataset
from download_button import download_button
from image_plagiarism_check import is_similar_image,batch_process_images
from zipfile import ZipFile


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
che_csv_name = f"check_{today}.csv"
pre_csv_name = f"prediction_{today}.csv"
res_csv_name = f"result_{today}.csv"
# CSVファイルの保存先ディレクトリのパスを指定する
save_check = "./ceremony/check"
save_prediction = "./ceremony/prediction"
save_dir = "./ceremony/result"
# 保存先のパスとファイル名を結合する
csv_che = os.path.join(save_check, che_csv_name)
csv_pre = os.path.join(save_prediction, pre_csv_name)
csv_res = os.path.join(save_dir, res_csv_name)

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
        if st.button("look!"):
            image_check(UPLOAD_FOLDER,PREDICTION_FOLDER)

        #拾い画像かどうかをチェック
        # 画像ファイルが保存されているフォルダのパスを指定して、一括で判定する
        st.title("拾い画かどうかチェック")
        if st.button("Check now!"):
            df_plagiarism_check = batch_process_images(PREDICTION_FOLDER)
            df_plagiarism_check.to_csv(csv_che, index=False)

        # サブミットボタンでフォームをサブミットする
        st.title("予測を行います")
        form = st.form(key='my-form')
        submit_button = form.form_submit_button('Submit!')
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
            predictions_df['filename'] = [os.path.basename(f) for f in pre_filenames]
            # csvファイルに保存するs
            predictions_df.to_csv(csv_pre, index=False)
            st.write("予測が完了しました")
            #拾い画チェックした結果と予測した結果を画像名称でjoin
            result_df = pd.merge(df_plagiarism_check, predictions_df, on='filename')
            result_df.to_csv(csv_res, index=False)
            st.title("結果のダウンロード(csv)")
            download_button(result_df,res_csv_name)

if __name__ == "__main__":
    main()

