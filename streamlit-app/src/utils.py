import torch


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

# 距離計算
def calc_distance(coods, old_coods):
    """ボックスの四角どうしの距離の和を算出"""
    distances = [abs(coods[i]-old_coods[i]) for i in range(4)]
    print("distances", distances)
    distance = sum(distances)
    return distance