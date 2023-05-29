import os
import torch
from utils.data_preprocess import get_image
from model import SimCharModel

def predict(chars: tuple[str], model, save_path: str, font_path: str) -> float:
    """预测模型

    Args:
        chars (tuple[str]): 待匹配的汉字元组
        model (Module): 模型
        save_path (str): 模型权重文件保存位置
        font_path (str): 字体文件保存位置
    
    Returns:
        float: 形近概率
    """
    param_path = f"{save_path}/simchar_weights.pth"
    
    if os.path.exists(param_path):
        state_dict = torch.load(param_path)
        model.load_state_dict(state_dict)
    else:
        print("Failed to find weight file")
        exit(0)
    image = torch.from_numpy(get_image(chars, font_path)).unsqueeze(0).unsqueeze(0).float()
    return model(image)
    

if __name__ == "__main__":
    font_path = './ai/character_match/fonts/simhei.ttf'
    save_path = './ai/character_match/param'
    
    char_1 = input("char_1:")
    char_2 = input("char_2:")
    
    result = predict((char_1, char_2), SimCharModel(), save_path, font_path)
    
    print(result)
