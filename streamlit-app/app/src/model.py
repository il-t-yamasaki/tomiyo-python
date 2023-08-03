import torch
import torchvision.transforms as T


class DetectorModel:
    def __init__(self, model_name:str="detr_resnet50"):
        # DETRのモデルを読み込む
        self.model = torch.hub.load("facebookresearch/detr",
                                    model_name,
                                    pretrained=True)
        self.model.eval()

    def predict(self, image):
        output = self.model(image)
        return output
    

class ImageTransformer:
    """mean-std normalize the input image (batch-size: 1)"""
    def __init__(self):
        """standard PyTorch mean-std input image normalization"""
        self.transform = T.Compose([
            T.Resize(800),
            T.ToTensor(),
            T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
    
    def transform(self, image):
        """pil imageをモデルの入力形式に変換する"""
        transformed_image = self.transform(image).unsqueeze(0)
        return transformed_image