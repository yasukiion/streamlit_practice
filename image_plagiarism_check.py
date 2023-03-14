import io
import os
import pandas as pd
from google.cloud import vision_v1
from google.cloud.vision_v1 import types
from google.oauth2 import service_account

# APIキーを設定する
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/nobutair/ceremony/authority/semiotic-pact-380611-164863744ba6.json"

# 認証情報を取得する
credentials = service_account.Credentials.from_service_account_file(
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'],
    scopes=['https://www.googleapis.com/auth/cloud-platform']
)

# 画像ファイルが拾い画像かどうかを判定する関数を定義する
def is_similar_image(filename):
    # 画像ファイルを読み込む
    with io.open(filename, 'rb') as image_file:
        content = image_file.read()
    image = types.Image(content=content)

    # Vision APIに接続する
    client = vision_v1.ImageAnnotatorClient(credentials=credentials)

    # 画像を分析し、拾い画像かどうかを判定する
    response = client.safe_search_detection(image=image)
    if response.safe_search_annotation.adult == 5 or response.safe_search_annotation.violence == 5 or response.safe_search_annotation.racy == 5:
        return {'is_similar_image': True}
    else:
        return {'is_similar_image': False}

# 指定されたフォルダにある画像ファイルを一括で判定する
def batch_process_images(folder_path):
    # フォルダ内の画像ファイルのパスを取得する
    file_list = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.jpg') or file.endswith('.jpeg') or file.endswith('.png')]

    # 各画像ファイルが拾い画像かどうかを判定する
    results = []
    for file in file_list:
        result = {'filename': os.path.basename(file), 'is_similar_image': is_similar_image(file)}
        results.append(result)

    # 結果をCSVファイルに出力する
    df = pd.DataFrame(results)
    return df
