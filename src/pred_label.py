import numpy as np
import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
from torchvision import models
from pydicom import dcmread
from pydicom.errors import InvalidDicomError


labels = {0: 'Negative',
          1: "Positive"
          }


def dcm_loader(path: str):
    img = dcmread(path).pixel_array
    img = img.astype(np.float32)
    return img


transform = transforms.Compose(
    [transforms.ToTensor(),
     transforms.Resize((256, 256)),
     ])


def predict_label(img, model):
    img = img.to(device)
    img = img.unsqueeze(0)
    preds = model(img)
    _, preds = torch.max(preds, dim=1)
    return preds[0].item()


if __name__ == "__main__":
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    model = models.resnet18()
    model.conv1 = nn.Conv2d(1, 64, kernel_size=(7, 7), stride=(2, 2), padding=(3, 3), bias=False)
    model.fc = nn.Linear(512, 2)

    model = model.to(device)
    model.load_state_dict(
        torch.load('../models/resnet18_pos_neg.pth', map_location=torch.device(device)))

    while True:
        file_path = input('Укажите путь к снимку: ')
        try:
            img = dcm_loader(file_path)
            img = transform(img)
            pred_label = predict_label(img, model)
            print(f'Предсказан класс: {labels[pred_label]}')
            print()

        except FileNotFoundError:
            print('Ошибка: Файл не найден')
        except InvalidDicomError:
            print('Ошибка: Неверный формат файла. Укажите путь к файлу .dcm')


