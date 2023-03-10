import streamlit as st
from PIL import Image
import numpy as np
import os
import tensorflow as tf

# 指定されたディレクトリからすべての画像ファイルを取得する関数
def image_2_dataset(pre_image_folder_path):
        batch_size = 32
        # 画像ファイル名とラベルのリストを作成する
        image_filenames = [os.path.join(pre_image_folder_path, f) for f in os.listdir(pre_image_folder_path)]

        # 画像データとラベルをNumPy配列として読み込む
        images = []
        for image_filename in image_filenames:
            image = Image.open(image_filename)
            image = image.resize((28, 28))  # 画像サイズを調整する
            image = np.array(image)  # NumPy配列に変換する
            images.append(image)
        images = np.array(images)

        # 前処理を行う
        images = images.astype("float32") / 255.0  # 画素値を0-1の範囲にスケーリングする

        # time_stepsを消す
        images = np.reshape(images, (-1, 28, 28, 3))

        # 訓練データとして使用するデータセットを作成する
        dataset = tf.data.Dataset.from_tensor_slices((images))
        dataset = dataset.batch(batch_size)
        return dataset

