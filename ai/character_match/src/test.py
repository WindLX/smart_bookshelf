import os
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from data_loader import SimCharDataSet
from model import SimCharModel
from utils.accuracy import accuracy

def test(model, test_loader, save_path: str, weight_file: str):
    """测试模型

    Args:
        model (_type_): 模型
        test_loader (_type_): 测试数据集加载器
        save_path (str): 模型权重文件保存位置
        weight_file (str): 模型权重文件名
    """
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    param_path = f"{save_path}/{weight_file}"
    
    if os.path.exists(param_path):
        model.load_state_dict(torch.load(param_path))
    else:
        print("Failed to find model weight file")
        exit(0)
    
    model.to(device)
    
    criterion = nn.BCELoss()
    
    model.eval()
    test_loss = 0.0
    test_acc = 0.0
    
    test_len = len(test_loader)
    
    print(f"Test Start")
    
    for index, (images, labels) in enumerate(test_loader):
        images = images.to(device)
        labels = labels.to(device)

        outputs = model(images)
        
        loss = criterion(outputs, labels)
        acc = accuracy(labels, outputs)
        
        print(f"  Batch [{index}/{test_len}]: Loss: {loss}, Acc: {acc}")
        
        test_loss += loss.item()
        test_acc += acc
    
    epoch_loss = test_loss / test_len
    epoch_acc = test_acc / test_len
    
    print(f"[Summary] Loss: {epoch_loss:.4f}, Acc: {epoch_acc:.4f}")

if __name__ == "__main__":
    file_path = './ai/character_match/data/data_1.txt'
    font_path = './ai/character_match/fonts/simhei.ttf'
    save_path = './ai/character_match/param'
    weight_file = 'simchar_weights.pth'
    
    batch_size = 64
    shuffle = True
    num_workers = 4
    prop = 0
    dataset_size = 100
    
    test_dataset = SimCharDataSet(file_path=file_path, font_path=font_path, dataset_size=dataset_size, prop=prop, split="")
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=shuffle, num_workers=num_workers)
    model = SimCharModel()
    test(model, test_loader, save_path, weight_file)
