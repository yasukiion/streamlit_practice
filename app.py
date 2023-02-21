import streamlit as st
import os
from PIL import Image
import shutil
import model


# def get_report_ctx():
#     """Returns the ReportContext for the running thread or None."""
#     return getattr(_get_session(), REPORT_CONTEXT_ATTR_NAME, None)

# def get_session():
#     session_id = get_report_ctx().session_id
#     session_info = Server.get_current()._get_session_info(session_id)
#     return session_info.session

# def _get_session():
#     session = None
#     ctx = ReportThread.get_report_ctx()

#     if ctx is not None:
#         session = getattr(ctx, '_session', None)

#         if session is None:
#             session = Server.get_current().get_session_info(ctx.session_id).session
#             setattr(ctx, '_session', session)

#     return session

# class SessionState:
#     def __init__(self, **kwargs):
#         self._state = kwargs

#     def __getattr__(self, attr):
#         return self._state[attr]

#     def __setattr__(self, attr, value):
#         if attr != '_state':
#             self._state[attr] = value
#         else:
#             super().__setattr__(attr, value)

# # SessionStateを初期化する
# ss = SessionState(name='', subscribe=False)

# フォルダのパスを指定
UPLOAD_FOLDER = "./uploads"

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
    st.title("結婚式場の画像をアップロードしてください")

    # フォルダをアップロードする
    folder = st.file_uploader("Upload a folder", type="zip")
    UPLOAD_FOLDER = "uploads"
    if folder:
        # zipファイルを展開する
        path = os.path.join(os.getcwd(), folder.name)
        with open(path, "wb") as f:
            f.write(folder.getbuffer())
        os.makedirs(os.path.join(os.getcwd(), UPLOAD_FOLDER), exist_ok=True)
        shutil.unpack_archive(path, os.path.join(os.getcwd(),UPLOAD_FOLDER))
        os.remove(path)

        # フォルダ内の画像を表示する
        image_extensions = ["jpg", "jpeg", "png"]
        image_folder = st.sidebar.selectbox("Select a folder", os.listdir(os.path.join(os.getcwd(),UPLOAD_FOLDER)))
        for file_name in os.listdir(os.path.join(os.path.join(os.getcwd(),UPLOAD_FOLDER, image_folder))):
            if file_name.split(".")[-1] in image_extensions:
                image_path = os.path.join(os.path.join(os.path.join(os.getcwd(),UPLOAD_FOLDER, image_folder)), file_name)
                image = Image.open(image_path)
                st.image(image, caption=file_name, use_column_width=True)

        # サブミットボタンでフォームをサブミットする
        form = st.form(key='my-form')
        submit_button = form.form_submit_button('Submit')
        if submit_button:
            selected_files = [file_name for file_name in os.listdir(os.path.join(os.getcwd(),UPLOAD_FOLDER, image_folder)) if file_name.split(".")[-1] in image_extensions]
            st.write(selected_files)

            # ファイルをアップロードする
            uploaded_file = st.file_uploader("Choose a file", type=["jpg", "jpeg", "png"])
            if uploaded_file is not None:
              # アップロードされたファイルを保存する
              file_path = save_uploaded_file(uploaded_file)
              st.write("Saved file:", file_path)
            else:
              st.write("No file uploaded")
            model.process_data(selected_files)

if __name__ == "__main__":
    main()

