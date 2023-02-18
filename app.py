import streamlit as st

st.checkbox("オラァ") #引数に入れることでboolを返す
st.button("スタンド使いは引かれ合う") #引数に入れるとboolで返す
st.selectbox("メニューリスト", ("覚悟はいいか", "復讐とは自分の運命に決着をつけることダァ!", "最高に「ハイ」ッッてやつダァァ")) #第一引数：リスト名、第二引数：選択肢
st.multiselect("スタンド使いですか？（複数選択可）", ("そうだ、素数を数えて落ち着こう....", "イチジクのジャム", "カブトムシ")) #第一引数：リスト名、第二引数：選択肢、複数選択可
st.radio("故郷に帰ったら何を食べたい", ("熱々のマルガリータ", "ドルチェ", "ロードローラー")) #第一引数：リスト名（選択肢群の上に表示）、第二引数：選択肢
# 以下をサイドバーに表示
st.sidebar.text_input("一味違うのね") #引数に入力内容を渡せる
st.sidebar.text_area("敵でもない、味方でもない、ただ希望なのだ")

import os
import streamlit as st

# フォルダ内の画像ファイルを読み込む関数
def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        if any(filename.lower().endswith(ext) for ext in ['.jpeg', '.jpg', '.png']):
            img_path = os.path.join(folder, filename)
            images.append(img_path)
    return images

# Streamlitアプリケーション
def main():
    # フォルダの選択
    folder = st.sidebar.selectbox("Select a folder", os.listdir("path/to/your/folder"))
    folder_path = os.path.join("path/to/your/folder", folder)

    # フォルダ内の画像ファイルを読み込む
    image_paths = load_images_from_folder(folder_path)

    # 画像ファイルを表示
    if len(image_paths) > 0:
        for path in image_paths:
            st.image(path)
    else:
        st.warning("No image file found in the selected folder")

if __name__ == '__main__':
    main()

