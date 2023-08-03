import numpy as np
from PIL import Image
import torch
import torchvision.transforms as T
torch.set_grad_enabled(False)

from src.model import DetectorModel
from src.utils import rescale_bboxes
from src.postprocess import post_process


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

# バイクの検出を実行する
def detect_bike(model: DetectorModel,
                frame: np.ndarray,
                only_oncoming_lane: str,
                threshold: float) -> dict:

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
    
    # リザルトからバイク画像を抽出
    bike_imgs = post_process(results, probas[keep], threshold, frame)
    return bike_imgs
