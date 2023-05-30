import os
import numpy as np
import onnx
import onnxruntime as ort
import torch
from utils.data_preprocess import get_image
from model import SimCharModel

def predict(chars: tuple[str], model, save_path: str, font_path: str, weight_file: str, is_onnx: bool=False) -> float:
    """预测模型

    Args:
        chars (tuple[str]): 待匹配的汉字元组
        model (_type_): 模型
        save_path (str): 模型type_type_存位置
        font_path (str): 字体文件保存位置
        weight_file (str): 模型权重文件名
        is_onnx (bool, optional): 是否为 ONNX 模型 . Defaults to False .
    
    Returns:
        float: 形近概率
    """
    param_path = f"{save_path}/{weight_file}"
    
    if not is_onnx:
        if os.path.exists(param_path):
            state_dict = torch.load(param_path)
            model.load_state_dict(state_dict)
        else:
            print("Failed to find weight file")
            exit(0)
        image = torch.from_numpy(get_image(chars, font_path)).unsqueeze(0).unsqueeze(0).float()
        model.eval()
        return model(image).detach().numpy()
    else:
        model = onnx.load(param_path)
        onnx.checker.check_model(model)
        ort_session = ort.InferenceSession(param_path, providers=['CUDAExecutionProvider'])
        input = get_image((char_1, char_2), font_path).astype(np.float32)
        input_shape = input.shape
        outputs = ort_session.run(
            None,
            {"input.1": input.reshape((1, 1, input_shape[0], input_shape[1]))},
        )
        return outputs
    

if __name__ == "__main__":
    font_path = './ai/character_match/fonts/simhei.ttf'
    save_path = './ai/character_match/param'
    weight_file= 'simchar_5_30_15_32.onnx'
    
    is_onnx = True
    
    char_1 = input("char_1:")
    char_2 = input("char_2:")

    result = predict((char_1, char_2), SimCharModel(), save_path, font_path, weight_file, is_onnx=is_onnx)
    
    print(result)
