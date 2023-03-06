import streamlit as st
from PIL import Image
import numpy as np
import os
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras.metrics import AUC
from tensorflow.keras.preprocessing.image import load_img, img_to_array

#式場の画像を学習していくcnnモデル
def cnn ():

  # ディレクトリ内の画像ファイルを取得する関数
  def get_image_files(directory):
      image_extensions = {"png", "jpg", "jpeg", "gif", "bmp"}
      image_files = []
      for root, dirs, files in os.walk(directory):
          for file in files:
              if file.lower().endswith(tuple(image_extensions)):
                  image_files.append(os.path.join(root, file))
      return image_files

  # 画像ファイルを読み込んで、NumPy配列に変換する関数
  def load_images(image_files, image_size):
      images = []
      for filename in image_files:
          img = load_img(filename, target_size=image_size)
          img = img_to_array(img)
          images.append(img)
      return np.asarray(images)

  # 画像フォルダのパスとラベルを定義する
  image_folder_path = "./ceremony/data"
  label_dict = {"not_ceremonyHall": 0, "ceremonyHall": 1}
  batch_size = 32

  # 画像ファイル名とラベルのリストを作成する
  image_filenames = []
  labels = []
  for label in label_dict.keys():
      label_path = os.path.join(image_folder_path, label)
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

  # 訓練データとテストデータに分割する
  train_size = int(len(image_filenames) * 0.8)
  val_size = len(image_filenames) - train_size
  train_dataset = dataset.take(train_size).batch(batch_size)
  val_dataset = dataset.skip(train_size).batch(batch_size)
  # ステップ数の計算
  train_steps_per_epoch = np.ceil(train_size / batch_size)
  val_steps_per_epoch = np.ceil(val_size / batch_size)


  # モデルの構築
  model = tf.keras.Sequential([
      # 畳み込み層1
      tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 3)),
      tf.keras.layers.MaxPooling2D((2, 2)),
      # 畳み込み層2
      tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
      tf.keras.layers.MaxPooling2D((2, 2)),
      # 畳み込み層3
      tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
      tf.keras.layers.Flatten(),
      # 全結合層1
      tf.keras.layers.Dense(64, activation='relu'),
      # 全結合層2
      tf.keras.layers.Dense(1, activation='sigmoid')
  ])

  # モデルのコンパイル
  model.compile(optimizer='rmsprop',
                loss='binary_crossentropy',
                metrics=[AUC()])

  # モデルの学習
  model.fit(train_dataset,
            epochs=5,
            steps_per_epoch=train_steps_per_epoch,
            validation_data=val_dataset,
            validation_steps=val_steps_per_epoch)
  
  # モデルを保存する
  model.save('./ceremony/my_model')

  # モデルの評価
  test_loss, test_auc = model.evaluate(val_dataset, steps=val_steps_per_epoch)
  st.write(test_auc)