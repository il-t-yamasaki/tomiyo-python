from pytube import YouTube


def download_movie(url:str) -> str:
    # 動画のメタデータ
    yt = YouTube(url)

    # 動画タイトル
    title = str(yt.title)

    available_list = yt.streams.all()
    for element in available_list:
        print(element)

    # ダウンロードするタイプ
    resolution = "720p" # ["720p", "better mp4"]
    if resolution == 'better mp4':
        # mp4の時
        yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()
    else:
        # mp4の時
        yt.streams.filter(resolution=resolution).first().download()
    
    return title
