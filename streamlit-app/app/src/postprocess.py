import cv2


def post_process(results, probas, threshold, frame) -> dict:
    """バイクの座標と検出された確信度から、バイク画像のdictを返す"""
    bike_count = 0
    bike_imgs = {}
    for (xmin, ymin, xmax, ymax), p in zip(results, probas):
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

    return bike_imgs