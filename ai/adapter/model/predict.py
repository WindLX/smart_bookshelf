import numpy as np
import onnx
import onnxruntime as ort
from functools import partial
from PIL import Image, ImageDraw, ImageFont

def predict(chars: tuple[str], save_path: str, font_path: str, weight_file: str, is_onnx: bool=False) -> float:
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
    
    if is_onnx:
        model = onnx.load(param_path)
        onnx.checker.check_model(model)
        ort_session = ort.InferenceSession(param_path, providers=['CPUExecutionProvider'])
        input = get_image(chars, font_path).astype(np.float32)
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

def get_image(chars: tuple[str], font_path: str, size: int=32) -> np.ndarray:
    """将汉字转换为图片

    Args:
        chars (tuple[str]): 汉字匹配组
        font_path (str): 字体文件路径
        size (int, optional): 图片大小. Defaults to 32.

    Returns:
        np.array: 图片数组，黑白图
    """
    font = ImageFont.truetype(font_path, size)
    image_width = size
    image_height = size
    
    combined_image = Image.new("L", (2 * image_width, image_height), color=0)

    for i, hanzi in enumerate(chars):
        hanzi_image = Image.new("L", (image_width, image_height), color=0)
        hanzi_draw = ImageDraw.Draw(hanzi_image)

        text_width, text_height = hanzi_draw.textsize(hanzi, font=font)
        text_x = int((image_width - text_width) / 2)
        text_y = int((image_height - text_height) / 2)
        hanzi_draw.text((text_x, text_y), hanzi, font=font, fill=255)

        combined_image.paste(hanzi_image, (i * image_width, 0))

    # 显示拼接后的图片
    # combined_image.show()

    image = np.array(combined_image) / 255
    
    return image


font_path = './ai/adapter/static/model/simhei.ttf'
save_path = './ai/adapter/static/model'
weight_file= 'simchar_5_30_15_32.onnx'

is_onnx = True

partial_predict = partial(predict, save_path=save_path, font_path=font_path, weight_file=weight_file, is_onnx=is_onnx)


def run(char_1: str, char_2: str) -> np.ndarray:
    result = get_similar_matrix(str1=char_1, str2=char_2, predict=partial_predict)
    sum = 0
    if result.shape[0] < result.shape[1]:
        num_rows = result.shape[0]
        for i in range(num_rows):
            row = result[i, :]
            max_value = np.max(row)
            sum += max_value
    else:
        num_columns = result.shape[1]
        for j in range(num_columns):
            column = result[:, j]
            max_value = np.max(column)
            sum += max_value
    sum /= min(result.shape[0], result.shape[1])
    return sum
