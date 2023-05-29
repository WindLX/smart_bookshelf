import requests
import json
import os

class DataItem:
    def __init__(self, points, ocr_result, confidence):
        self.points = points
        self.ocr_result = ocr_result
        self.confidence = confidence
        
    def __str__(self) -> str:
        s = ""
        s += f'Points: {self.points}\n'
        s += f'OCR Result: {self.ocr_result}\n'
        s += f'Confidence: {self.confidence}\n'
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
    def __init__(self, data_list, file_name):
        self.data_list = data_list
        self.file_name = file_name
    
    def __str__(self):
        s = ""
        s += f"File Name: {self.file_name}\n"
        for d in self.data_list:
            s += str(d)
        return s
            
    def __len__(self):
        return len(self.data_list)

url = 'http://localhost:8080/ocr'

folder_path = "./segment/temp"

file_list = []

for root, dirs, files in os.walk(folder_path):
    for file in files:
        file_path = os.path.join(root, file)
        file_list.append(file_path)

results = []

for file_path in file_list:
    print(file_path)
    files = {'file': open(file_path, 'rb')}
    response = requests.post(url, files=files)
    response.encoding = 'utf-8'

    if response.status_code == 200:
        result = json.loads(response.text)
        class_objects = []
        for item in result[0]:
            points = item[0]
            ocr_result = item[1][0]
            confidence = item[1][1]
            data_item = DataItem(points, ocr_result, confidence)
            class_objects.append(data_item)
        if len(class_objects) > 0:
            results.append(DataSet(class_objects, file_path))
    else:
        print('File upload failed:', response.text)

print(len(results))
for e in results:
    if len(e) > 0:
        # ee = max(e, key=lambda x: x.area)
        print(e)
    print("------------")