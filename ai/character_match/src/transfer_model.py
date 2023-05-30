import os
import torch
from model import SimCharModel

def transfer_model(model, save_path: str, input_name: str, output_name: str, batch_size: int):
    """将模型转换为 ONNX 类型

    Args:
        model (_type_): 模型
        save_path (str): 权重文件保存路径
        input_name (str): 输入权重文件名
        output_name (str): 输出文件名
        batch_size (int): 输入 batch_size 大小

    Raises:
        RuntimeError: 找不到权重文件
    """
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    param_path = f"{save_path}/{input_name}"
    
    if os.path.exists(param_path):
        model.load_state_dict(torch.load(param_path))
    else:
        raise RuntimeError("Failed to find model weight file")
    
    model.to(device)
    model.eval()
    torch.onnx.export(model, torch.randn(batch_size, 1, model.size, model.size * 2, device=device), f"{save_path}/{output_name}")
    
    print("Transfer Model Successfully")
    
if __name__ == "__main__":
    save_path = './ai/character_match/param'
    input_name = 'simchar_weights_5_30_15_32.pth'
    output_name = 'simchar_5_30_15_32.onnx'
    
    batch_size = 1
    
    model = SimCharModel()
    transfer_model(model=model, save_path=save_path, input_name=input_name, output_name=output_name, batch_size=batch_size)