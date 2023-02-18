import streamlit as st
import os
from PIL import Image
import shutil

st.checkbox("オラオラオラオラオラ") #引数に入れることでboolを返す
st.button("スタンド使いは引かれ合う") #引数に入れるとboolで返す
st.selectbox("メニューリスト", ("覚悟はいいか", "復讐とは自分の運命に決着をつけることダァ!", "最高に「ハイ」ッッてやつダァァ")) #第一引数：リスト名、第二引数：選択肢
st.multiselect("つまづいたっていいじゃあないか（複数選択可）", ("そうだ、素数を数えて落ち着こう....", "イチジクのジャム", "カブトムシ")) #第一引数：リスト名、第二引数：選択肢、複数選択可
st.radio("故郷に帰ったら何を食べたい", ("熱々のマルガリータ", "ドルチェ", "ロードローラー")) #第一引数：リスト名（選択肢群の上に表示）、第二引数：選択肢
# 以下をサイドバーに表示
st.sidebar.text_input("一味違うのね") #引数に入力内容を渡せる
st.sidebar.text_area("敵でもない、味方でもない、ただ希望なのだ")

def main():
    st.title("「覚悟」をアップロードしてください")

    # フォルダをアップロードする
    folder = st.file_uploader("Upload a folder", type="zip")
    if folder:
        # zipファイルを展開する
        path = os.path.join(os.getcwd(), folder.name)
        with open(path, "wb") as f:
            f.write(folder.getbuffer())
        os.makedirs(os.path.join(os.getcwd(), os.path.splitext(folder.name)[0]), exist_ok=True)
        shutil.unpack_archive(path, os.path.splitext(folder.name)[0])
        os.remove(path)

        # フォルダ内の画像を表示する
        image_extensions = ["jpg", "jpeg", "png"]
        image_folder = st.sidebar.selectbox("Select a folder", os.listdir(os.path.splitext(folder.name)[0]))
        for file_name in os.listdir(os.path.join(os.path.splitext(folder.name)[0], image_folder)):
            if file_name.split(".")[-1] in image_extensions:
                image_path = os.path.join(os.path.join(os.path.splitext(folder.name)[0], image_folder), file_name)
                image = Image.open(image_path)
                st.image(image, caption=file_name, use_column_width=True)

if __name__ == "__main__":
    main()

