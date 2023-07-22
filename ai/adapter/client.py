from __future__ import annotations
import requests
import json
from pprint import pprint
import time
from typing import Dict, List

def timer(func: callable):
    """计时器装饰器

    Args:
        func (callable): 待测量运行时间的函数
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"[{func.__name__}] exec time: {elapsed_time:.2f} s")
        return result
    return wrapper

class DataItem:
    def __init__(self, points: List, ocr_result: str, confidence: float):
        self.points = points
        self.ocr_result = ocr_result
        self.confidence = confidence
        
    def __str__(self) -> str:
        s = ""
        s += f'  Points: {self.points}\n'
        s += f'  OCR Result: {self.ocr_result}\n'
        s += f'  Confidence: {self.confidence}\n'
        s += '  ---\n'
        return s
    
    @property
    def area(self) -> float:
        x1, y1 = self.points[0]
        x2, y2 = self.points[1]
        x3, y3 = self.points[2]
        x4, y4 = self.points[3]

        area_triangle1 = 0.5 * abs((x1*y2 + x2*y3 + x3*y1) - (y1*x2 + y2*x3 + y3*x1))
        area_triangle2 = 0.5 * abs((x1*y3 + x3*y4 + x4*y1) - (y1*x3 + y3*x4 + y4*x1))

        total_area = area_triangle1 + area_triangle2

        return total_area
    
    @property
    def char_len(self) -> int:
        return len(self.ocr_result)

class DataSet:
    def __init__(self, data_list: List, file_name: str, coorinate: float):
        self.data_list = data_list
        self.file_name = file_name
        self.coorinate = coorinate
    
    def __str__(self):
        s = ""
        s += f"File Name: {self.file_name}\n"
        s += f"Coorinate: {self.coorinate}\n"
        for i, d in enumerate(self.data_list):
            s += f"  index: {i}\n"
            s += str(d)
        return s
            
    def __len__(self):
        return len(self.data_list)

    @staticmethod
    def DataSetbuilder(raw_data: Dict[str, List]) -> List[DataSet]:
        data_sets = []
        try:
            for key, value in raw_data.items():
                data_list = []
                for raw_data_item in value[1][0]:
                    data_list.append(DataItem(points=raw_data_item[0], ocr_result=raw_data_item[1][0], confidence=raw_data_item[1][1]))
                data_set = DataSet(file_name=key, coorinate=value[0], data_list=data_list)
                data_sets.append(data_set)
        finally:
            return data_sets
    
    @property
    def connected_result(self) -> str:
        s = [x.ocr_result for x in self.data_list]
        s = ' '.join(s)
        return s

@timer
def post(url: str, file_path: str) -> Dict[str, List]:
    """发起 OCR 请求

    Args:
        url (str): 服务器地址
        file_path (str): 文件路径
        
    Returns:
        dict[str, list]: 识别结果
    """
    files = {'file': open(file_path, 'rb')}
    
    print("start post")
    response = requests.post(url, files=files)
    response.encoding = 'utf-8'

    if response.status_code == 200:
        result = json.loads(response.text)
        return result

if __name__ == "__main__":
    url = 'http://localhost:8080/ocr'
    file_path = "./pic/4.jpg"
    
    res = post(url=url, file_path=file_path)
    data_sets = DataSet.DataSetbuilder(res)
    for e in data_sets:
        print(e.connected_result)
        