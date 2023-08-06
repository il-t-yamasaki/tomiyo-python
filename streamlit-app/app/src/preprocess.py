import cv2

from src.model import DetectorModel


def model_loader():
    """モデルを読み込む"""
    model = DetectorModel()
    return model

def capture_loader(movie_path:str):
    """ダウンロードした動画を読み込み、動画とFPSを返す"""
    cap = cv2.VideoCapture(movie_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    return cap, fps
