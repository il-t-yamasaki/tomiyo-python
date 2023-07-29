import glob
import os

import streamlit as st

import downloader
import predictor


st.title("動画からバイクの画像を切り抜いて表示するアプリ")

# 以下をサイドバーに表示
url = st.sidebar.text_input("Youtubeの動画のURLを入力してください")
if st.sidebar.button(label="ダウンロード"):
    if not url or "http" not in url:
        url = "https://www.youtube.com/watch?v=VxM206Fd1nY"
    title = downloader.download_movie(url)

if st.button(label="検出！"):
    app_state = st.empty()
    movie_title = st.empty()
    time_st = st.empty()
    image_loc = st.empty()

    cwd = os.getcwd()
    movie_path = glob.glob(f"{cwd}/*.mp4")[0]

    #@title バイク検出実行 対向車線のみから取得する場合はTrueにする
    app_state.write("モデルダウンロード中...")
    only_oncoming_lane = "True"
    model, cap, fps, threshold = predictor.pre_load(movie_path=movie_path, threshold=0.6)
    print(movie_path , fps)
    app_state.write('モデル準備完了！')
    movie_title.write(f"動画のタイトル：{movie_path}")

    frame_count = 0
    while True:
        ret, frame = cap.read()
        frame_count += 1
        time_in_sec = frame_count / fps
        if not ret:
            print("Stop")
            break

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