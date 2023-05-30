import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont

class DataPreprocesser:
    """形近字数据库预处理类
    """
    def __init__(self, file_path: str, dataset_size: int, split: str, prop: float=0.0) -> None:
        """构造函数

        Args:
            file_path (str): 数据文件路径
            dataset_size (int): 数据集的大小
            split (str): 分隔符
            prop (float, optional): 相似度容限. Defaults to 0.0 .
        """
        self.file_path = file_path
        self.dataset_size = dataset_size
        self.prop = prop
        self.split = split
        self.len = self.__calc_len(dataset_size)
        self.data = self.get_partial_characters()
        
    def __len__(self) -> int:
        """获取汉字数量

        Returns:
            int: 数量
        """
        return self.len
    
    def __getitem__(self, index: int) -> tuple[str]:
        """按索引获取两个汉字的匹配组

        Args:
            index (int): 索引

        Returns:
            tuple(str): 两个汉字构成的元组
        """
        offset_x = index // self.len
        offset_y = index % self.len
        return (self.data[offset_x], self.data[offset_y])

    def get_form_character(self, character: str) -> list[str]:
        """在数据文件中查找一个汉字的所有形近字

        Args:
            file_path (str): 数据文件的路径
            character (str): 待查找的汉字

        Returns:
            list[str]: 匹配结果
        """
        with open(self.file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line != "":
                    if line[-1] == "，":
                        line = line[:-1]
                if character in line:
                    if self.split != "":
                        characters = line.split(self.split)
                    else:
                        characters = list(line)
                    characters = list(filter(lambda x: x != "", characters))
                    return characters
        return None
    
    def __calc_len(self, dataset_size: int) -> int:
        """计算数据文件中的汉字数量

        Args:
            dataset_size (int): 数据集的大小.
        
        Returns:
            int: 汉字数量
        """
        count = 0
        with open(self.file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line != "":
                    if line[-1] == "，":
                        line = line[:-1]
                    if self.split != "":
                        characters = line.split(self.split)
                    else:
                        characters = list(line)
                    characters = list(filter(lambda x: x != "", characters))
                    count += len(characters)
        if dataset_size < count:
            return dataset_size
        else:
            raise IndexError("dataset_size is huge than data file")
    
    def get_label(self, index: int) -> float:
        """获取相似度

        Args:
            index (int): 匹配组索引

        Returns:
            float: 相似度
        """
        char_1, char_2 = self.__getitem__(index)
        return random.uniform(1.0 - self.prop, 1.0) if char_2 in self.get_form_character(char_1) else random.uniform(0, self.prop)
    
    def get_partial_characters(self) -> np.ndarray[str]:
        """获取部分汉字
        
        Returns:
            np.ndarray[str]: 所有汉字
        """
        all_chars = np.array([], dtype='U1')
        with open(self.file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line != "":
                    if line[-1] == "，":
                        line = line[:-1]
                    if self.split != "":
                        characters = line.split(self.split)
                    else:
                        characters = list(line)
                    characters = list(filter(lambda x: x != "", characters))
                    chars = np.array(characters, dtype='U1')
                    all_chars = np.concatenate((all_chars, chars))
        sample_chars = np.random.choice(all_chars, self.dataset_size)
        for s in sample_chars:
            sample_chars = np.concatenate((sample_chars, self.get_form_character(s)))

        sample_chars = np.unique(sample_chars)
        return np.random.choice(sample_chars, self.dataset_size, replace=False)
    
    @property
    def all_characters(self) -> list[str]:
        """获取所有汉字

        Returns:
            list[str]: 所有汉字
        """
        all_chars = []
        with open(self.file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line != "":
                    if line[-1] == "，":
                        line = line[:-1]
                    if self.split != "":
                        characters = line.split(self.split)
                    else:
                        characters = list(line)
                    characters = list(filter(lambda x: x != "", characters))
                    all_chars.extend(characters)
        return all_chars
    
    @property
    def count(self) -> int:
        """匹配组数量

        Returns:
            int: 数量
        """
        return self.len * self.len

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

# 示例用法
if __name__ == "__main__":
    file_path = './ai/character_match/data/data_1.txt'
    font_path = './ai/character_match/fonts/simkai.ttf'
    dp = DataPreprocesser(file_path, dataset_size=64, split="")
    # image = get_image(("你", "二"), font_path)
    # np.set_printoptions(threshold=np.inf)
    # print(image)
    print(dp.data)
    
    # input_character = input('请输入要查找的汉字：')
    # result = dp.get_similar_character(input_character)

    # if result:
    #     print(result)
    # else:
    #     print('未找到匹配的行。')
