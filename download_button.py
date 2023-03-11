import streamlit as st
import pandas as pd
import base64

# csvファイルをダウンロードするボタン
def download_button(csv_file, csvname, file_label='Download CSV file', on_click=None):
    csv_file = csv_file.to_csv(index=False)
    b64 = base64.b64encode(csv_file.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download={csvname}>{file_label}</a>'
    return st.markdown(href, unsafe_allow_html=True)