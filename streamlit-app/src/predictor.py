import cv2
import numpy as np
from PIL import Image
from typing import Union
import torch
import torchvision.transforms as T
torch.set_grad_enabled(False)

from src.model import DetectorModel, ImageTransformer
from src.utils import rescale_bboxes


# 画像前処理器をロード
#image_transformer = ImageTransformer()
# TODO:transformを直に定義しないとエラーになる
transform = T.Compose(
                [
                    T.Resize(800),
                    T.ToTensor(),
                    T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
                ]
            )
    
# 検知処理
def pre_load(movie_path:str, threshold:float=0.5):
    # DETRのモデルを読み込む
    model = DetectorModel()

    # ダウンロードした動画を読み込む
    cap = cv2.VideoCapture(movie_path)

    # 動画のFPSを取得する
    fps = cap.get(cv2.CAP_PROP_FPS)

    return model, cap, fps, threshold

# バイクの検出を実行する
def detect_bike(model: DetectorModel,
                frame,
                only_oncoming_lane,
                threshold) -> Union[np.ndarray, None]:

    # フレームを右半分にする
    if only_oncoming_lane == "True":
        frame = frame[:,frame.shape[1]//2:]
    pil_image = Image.fromarray(frame)

    # 物体検出を実行する
    #transformed_image = image_transformer.transform(pil_image)
    transformed_image = transform(pil_image).unsqueeze(0)
    outputs = model.predict(transformed_image)

    # しきい値以上の検出結果を採用
    probas = outputs['pred_logits'].softmax(-1)[0, :, :-1]
    keep = probas.max(-1).values > threshold

    # bboxのスケールをもとの画像サイズに変換
    results = rescale_bboxes(outputs['pred_boxes'][0, keep], pil_image.size)

    # バイクの座標と検出された確信度を取得する
    bike_count = 0
    bike_imgs = {}
    for (xmin, ymin, xmax, ymax), p in zip(results, probas[keep]):
        x1 = int(xmin)
        y1 = int(ymin)
        x2 = int(xmax)
        y2 = int(ymax)
        cl = p.argmax()
        score = p[cl]
        # 閾値以上のバイクだけ
        if cl != 4 or score < threshold:
            continue
        bike_count += 1

        # bikeの画像を切り出す
        #x1, y1 = max(0, x1), max(0, y1)
        #x2, y2 = min(frame.shape[1], x2), min(frame.shape[0], y2)
        bike_img = frame[y1:y2, x1:x2]
        resized_bike_img = cv2.resize(bike_img, dsize=None, fx=2.0, fy=2.0)

        bike_imgs[f"{bike_count}"] = resized_bike_img
        print(f'Bike {bike_count}: ({x1}, {y1}), ({x2}, {y2})')

    if bike_count:
        return bike_imgs
    else:
        return None