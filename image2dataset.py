import streamlit as st
from PIL import Image
import numpy as np
import os
import tensorflow as tf

# 指定されたディレクトリからすべての画像ファイルを取得する関数
def image_2_dataset(pre_image_folder_path):
        # ラベルを新たに与えたい画像フォルダのパス
        label_dict = {"not_ceremonyHall": 0, "ceremonyHall": 1}
        batch_size = 32

        # 画像ファイル名とラベルのリストを作成する
        image_filenames = []
        labels = []
        for label in label_dict.keys():
            label_path = os.path.join(pre_image_folder_path, label)
            for image_filename in os.listdir(label_path):
                image_filenames.append(os.path.join(label_path, image_filename))
                labels.append(label_dict[label])

        # 画像データとラベルをNumPy配列として読み込む
        images = []
        for image_filename in image_filenames:
            image = Image.open(image_filename)
            image = image.resize((28, 28))  # 画像サイズを調整する
            image = np.array(image)  # NumPy配列に変換する
            images.append(image)
        images = np.array(images)
        labels = np.array(labels)

        # 前処理を行う
        images = images.astype("float32") / 255.0  # 画素値を0-1の範囲にスケーリングする
        labels = tf.keras.utils.to_categorical(labels)  # ラベルをone-hot表現に変換する
        labels = labels[:, 1]

        # time_stepsを消す
        images = np.reshape(images, (-1, 28, 28, 3))

        # 訓練データとして使用するデータセットを作成する
        dataset = tf.data.Dataset.from_tensor_slices((images, labels))
        dataset = dataset.shuffle(len(images))
        return(dataset)

