import streamlit as st

st.checkbox("オラァ") #引数に入れることでboolを返す
st.button("スタンド使いは引かれ合う") #引数に入れるとboolで返す
st.selectbox("メニューリスト", ("覚悟はいいか", "復讐とは自分の運命に決着をつけることダァ!", "最高に「ハイ」ッッてやつダァァ")) #第一引数：リスト名、第二引数：選択肢
st.multiselect("スタンド使いですか？（複数選択可）", ("そうだ、素数を数えて落ち着こう....", "イチジクのジャム", "カブトムシ")) #第一引数：リスト名、第二引数：選択肢、複数選択可
st.radio("故郷に帰ったら何を食べたい", ("熱々のマルガリータ", "ドルチェ", "ロードローラー")) #第一引数：リスト名（選択肢群の上に表示）、第二引数：選択肢
# 以下をサイドバーに表示
st.sidebar.text_input("一味違うのね") #引数に入力内容を渡せる
st.sidebar.text_area("敵でもない、味方でもない、ただ希望なのだ")

# マルチアップロードのためのファンクション
def multi_file_uploader():
    uploaded_files = st.file_uploader("Choose your image files", accept_multiple_files=True)
    return uploaded_files

# Streamlitアプリケーション
def main():
    # ファイルアップローダーの表示
    uploaded_files = multi_file_uploader()
    if uploaded_files is not None:
        for file in uploaded_files:
            # 画像ファイルを表示
            st.image(file)

if __name__ == '__main__':
    main()
