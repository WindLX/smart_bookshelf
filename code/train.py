from torch.utils.tensorboard import SummaryWriter
import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from data_loader import SimCharDataSet
from model import SimCharModel
from utils.accuracy import accuracy

def init_weight(m):
    """初始化模型权重

    Args:
        m (_type_): 模型中的层
    """
    if type(m) == nn.Linear or type(m) == nn.Conv2d:
        nn.init.xavier_uniform_(m.weight)

def train(model, train_loader, num_epochs: int, learning_rate: float, save_path: str, writer, input_name: str, output_name: str, weight_decay: float=0.0):
    """训练模型

    Args:
        model (_type_): 模型
        train_loader (_type_): 训练数据集加载器
        num_epochs (int): 训练代数
        learning_rate (float): 学习率
        save_path (str): 模型权重文件保存位置
        writer (_type_): TensorBoard 记录器
        input_name (str): 模型权重文件名称
        output_name (str): 模型权重文件保存名称
        weight_decay (float, optional): 权重衰退. Defaults to 0.0 .
    """
    try:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        param_path = f"{save_path}/{input_name}"
        save_path = f"{save_path}/{output_name}"
        
        if os.path.exists(param_path):
            model.load_state_dict(torch.load(param_path))
        else:
            print("Failed to find weight file, please make sure whether to train a new model [y/N]")
            option = input()
            if option == "y" or option == "Y":
                model.apply(init_weight)
            else:
                exit(0)
        
        model.to(device)
        
        criterion = nn.BCELoss()
        optimizer = optim.Adam(model.parameters(), lr=learning_rate, weight_decay=weight_decay)
        
        for epoch in range(num_epochs):
            model.train()
            running_loss = 0.0
            running_acc = 0.0
            
            for images, labels in train_loader:
                images = images.to(device)
                labels = labels.to(device)
                
                optimizer.zero_grad()

                outputs = model(images)
                
                loss = criterion(outputs, labels)
                
                acc = accuracy(labels, outputs)
                    
                loss.backward()
                optimizer.step()
                
                running_loss += loss.item()
                running_acc += acc
            
            for name, param in model.named_parameters():
                writer.add_histogram(name, param, epoch)
                writer.add_histogram(name + '/grad', param.grad, epoch)
            
            epoch_loss = running_loss / len(train_loader)
            epoch_acc = running_acc / len(train_loader)
            
            writer.add_scalar('Loss/train', epoch_loss, epoch)
            writer.add_scalar('Accuracy/train', epoch_acc, epoch)
            
            print(f"  Epoch [{epoch+1}/{num_epochs}]: Loss: {epoch_loss:.4f}, Acc: {epoch_acc:.4f}")
        torch.save(model.state_dict(), save_path)
        writer.close()
    except:
        torch.save(model.state_dict(), save_path)
        writer.close()

if __name__ == "__main__":
    file_path = './ai/character_match/data/data_1.txt'
    font_path = './ai/character_match/fonts/simhei.ttf'
    save_path = './ai/character_match/param'
    log_path = './ai/character_match/logs'
    input_name = 'simchar_weights_5_30_17_14.pth'
    output_name= 'simchar_weights.pth'
    
    train_times = 50
    batch_size = 64
    shuffle = True
    num_workers = 4
    prop = 0
    dataset_size = 15
    
    # 定义训练超参数
    num_epochs = 75
    learning_rate = 0.0005
    weight_decay = 0.001
    
    for time in range(train_times):
        print(f"Time [{time+1}/{train_times}]")
        train_dataset = SimCharDataSet(file_path=file_path, font_path=font_path, dataset_size=dataset_size, prop=prop, split="")
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=shuffle, num_workers=num_workers)
        model = SimCharModel()
        writer = SummaryWriter(log_dir=log_path)
        train(model, train_loader, num_epochs, learning_rate, save_path, writer, input_name, output_name, weight_decay=weight_decay)
