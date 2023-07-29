import os

import cv2
from PIL import Image
import torch
import torchvision.transforms as T
torch.set_grad_enabled(False)


# COCO classes
CLASSES = [
    'N/A', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
    'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'N/A',
    'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse',
    'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'N/A', 'backpack',
    'umbrella', 'N/A', 'N/A', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis',
    'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove',
    'skateboard', 'surfboard', 'tennis racket', 'bottle', 'N/A', 'wine glass',
    'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich',
    'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake',
    'chair', 'couch', 'potted plant', 'bed', 'N/A', 'dining table', 'N/A',
    'N/A', 'toilet', 'N/A', 'tv', 'laptop', 'mouse', 'remote', 'keyboard',
    'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'N/A',
    'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier',
    'toothbrush'
]

# colors for visualization
COLORS = [[0.000, 0.447, 0.741], [0.850, 0.325, 0.098], [0.929, 0.694, 0.125],
          [0.494, 0.184, 0.556], [0.466, 0.674, 0.188], [0.301, 0.745, 0.933]]

# standard PyTorch mean-std input image normalization
transform = T.Compose([
    T.Resize(800),
    T.ToTensor(),
    T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# for output bounding box post-processing
def box_cxcywh_to_xyxy(x):
    x_c, y_c, w, h = x.unbind(1)
    b = [(x_c - 0.5 * w), (y_c - 0.5 * h),
         (x_c + 0.5 * w), (y_c + 0.5 * h)]
    return torch.stack(b, dim=1)

def rescale_bboxes(out_bbox, size):
    img_w, img_h = size
    b = box_cxcywh_to_xyxy(out_bbox)
    b = b * torch.tensor([img_w, img_h, img_w, img_h], dtype=torch.float32)
    return b

# 検知処理
def pre_load(movie_path, threshold=0.5):
    # DETRのモデルを読み込む
    model = torch.hub.load('facebookresearch/detr', 'detr_resnet50', pretrained=True)
    model.eval()

    # ダウンロードした動画を読み込む
    cwd = os.getcwd()
    cap = cv2.VideoCapture(movie_path)

    # 動画のFPSを取得する
    fps = cap.get(cv2.CAP_PROP_FPS)

    return model, cap, fps, threshold

# 距離計算
def calc_distance(coods, old_coods):
    print("distance", [abs(coods[i]-old_coods[i]) for i in range(4)])
    distance = sum([abs(coods[i]-old_coods[i]) for i in range(4)])
    return distance

# バイクの検出を実行する
def detect_bike(model, frame, only_oncoming_lane, threshold):

    # フレームを右半分にする
    if only_oncoming_lane == "True":
        frame = frame[:,frame.shape[1]//2:]
    pil_image = Image.fromarray(frame)

    # 物体検出を実行する
    # mean-std normalize the input image (batch-size: 1)
    img = transform(pil_image).unsqueeze(0)

    # propagate through the model
    outputs = model(img)

    # keep only predictions with 0.7+ confidence
    probas = outputs['pred_logits'].softmax(-1)[0, :, :-1]
    keep = probas.max(-1).values > threshold

    # convert boxes from [0; 1] to image scales
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