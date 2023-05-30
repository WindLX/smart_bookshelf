import os
import numpy as np
import onnx
import onnxruntime as ort
import torch
from functools import partial
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

def get_similar_matrix(str1: str, str2: str, predict: callable) -> np.ndarray:
    """计算相似度矩阵

    Args:
        str1 (str): 字符串1
        str2 (str): 字符串2
        predict (function): 预测函数

    Returns:
        np.ndarray: 相似度矩阵
    """
    str1 = str1.replace(" ", "")
    str2 = str2.replace(" ", "")

    if len(str1) <= len(str2):
        short_str = str1
        long_str = str2
    else:
        short_str = str2
        long_str = str1

    row_num = len(short_str)
    col_num = len(long_str)
    matrix = np.empty((row_num, col_num), dtype=float)

    for i in range(row_num):
        for j in range(col_num):
            matrix[i][j] = predict((short_str[i], long_str[j]))[0][0]

    return matrix

if __name__ == "__main__":
    font_path = './ai/character_match/fonts/simhei.ttf'
    save_path = './ai/character_match/param'
    weight_file= 'simchar_weights_5_30_15_32.pth'
    matrix_path = './ai/sentence_match/similar_matrix.txt'
    
    is_onnx = False
    
    char_1 = input("char_1:")
    char_2 = input("char_2:")

    partial_predict = partial(predict, model=SimCharModel(), save_path=save_path, font_path=font_path, weight_file=weight_file, is_onnx=is_onnx)
    
    # result = partial_predict((char_1, char_2))
    result = get_similar_matrix(str1=char_1, str2=char_2, predict=partial_predict)
    
    print(result)
    
    with open(matrix_path, 'w', encoding='utf-8') as file:
        file.write(f"{result.shape[0]} {result.shape[1]}\n")
        for i in range(result.shape[0]):
            for j in range(result.shape[1]):
                file.write(f"{result[i][j]:.6f} ")
            file.write("\n")
