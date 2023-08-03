import glob
import os

import streamlit as st

from src import downloader, predictor, preprocess


st.title("動画からバイクの画像を切り抜いて表示するアプリ")

# サイドバー表示
url = st.sidebar.text_input("Youtubeの動画のURLを入力してください")
if st.sidebar.button(label="ダウンロード"):
    if url:
        title = downloader.download_movie(url)
        st.sidebar.text(f"{title} がダウンロードされました")

# 検出実行時
if st.button(label="検出！"):
    app_state = st.empty()
    movie_title = st.empty()
    time_st = st.empty()
    image_loc = st.empty()

    # 対向車線のみから取得する場合はTrueにする
    only_oncoming_lane = "True"
    threshold = 0.6

    # TODO: ちゃんと意図した動画を読み込むようにする
    cwd = os.getcwd()
    movie_path = glob.glob(f"{cwd}/*.mp4")[0]

    app_state.write("モデルダウンロード中...")
    # 前処理
    model = preprocess.model_loader()
    cap, fps = preprocess.capture_loader(movie_path)
    app_state.write('モデル準備完了！')
    movie_title.write(f"動画のタイトル：{os.path.basename(movie_path)}")

    frame_count = 0
    while True:
        ret, frame = cap.read()
        frame_count += 1
        time_in_sec = frame_count / fps
        if not ret:
            break
        # バイク画像を検出する
        bike_imgs = predictor.detect_bike(model,
                                          frame,
                                          only_oncoming_lane,
                                          threshold)
        # 動画内での時間とバイクの台数を出力する
        if bike_imgs:
            print(f'Time: {time_in_sec:.2f}s, {len(bike_imgs)} bikes')
            st.text(f"Time: {time_in_sec:.2f}s")
            for bike_img in bike_imgs.keys():
                st.image(bike_imgs[bike_img])
        
        if frame_count % (fps//10) == 0:
            print(f'Time: {(frame_count / fps):.2f}s')
            time_st.text(f"Time: {time_in_sec:.2f}s")

    cap.release()