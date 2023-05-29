import torch
import torch.nn as nn
import torch.nn.functional as F
import utils.layer_tools as tools

class SimCharModel(nn.Module):
    """网络的模型
    """
    def __init__(self, size: int=32) -> None:
        """构造函数

        Args:
            size (int, optional): 图片大小. Defaults to 32.
        """
        super().__init__()
        
        self.dropout1 = nn.Dropout(p=0.0)
        self.dropout2 = nn.Dropout(p=0.0)
        self.dropout3 = nn.Dropout(p=0.0)
        self.dropout4 = nn.Dropout(p=0.0)
        
        # 定义卷积层
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=8, kernel_size=5, stride=1, padding=1)
        h, w = tools.calc_conv_layer(size, 2 * size, 1, 5, 1)
        
        # 定义池化层
        self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)
        h, w = tools.calc_pool_layer(h, w, 2, 2)
        
        self.conv2 = nn.Conv2d(in_channels=8, out_channels=16, kernel_size=3, stride=1, padding=1)
        h, w = tools.calc_conv_layer(h, w, 1, 3, 1)
        
        self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)
        h, w = tools.calc_pool_layer(h, w, 2, 2)
        
        self.conv3 = nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, stride=1, padding=1)
        h, w = tools.calc_conv_layer(h, w, 1, 3, 1)
        
        self.pool3 = nn.MaxPool2d(kernel_size=2, stride=2)
        h, w = tools.calc_pool_layer(h, w, 2, 2)
        
        # 定义全连接层
        self.fc1 = nn.Linear(32 * int(h) * int(w), 64)
        self.fc2 = nn.Linear(64, 1)
        
    def forward(self, x):
        """前向传播
        """
        x = self.dropout1(x)
        
        x = self.conv1(x)
        x = F.relu(x)
        x = self.pool1(x)
        
        x = self.dropout2(x)
        
        x = self.conv2(x)
        x = F.relu(x)
        x = self.pool2(x)
        
        x = self.dropout3(x)
        
        x = self.conv3(x)
        x = F.relu(x)
        x = self.pool3(x)
        
        x = torch.flatten(x, 1)
        
        x = self.fc1(x)
        
        x = self.dropout4(x)
        
        x = F.relu(x)
        x = self.fc2(x)
        
        x = torch.sigmoid(x)
        
        return x

if __name__ == "__main__":
    model = SimCharModel()
    print(model)