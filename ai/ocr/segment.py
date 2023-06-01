from __future__ import annotations
import os
import cv2
import numpy as np
import shutil
from sklearn.cluster import DBSCAN
from typing import Tuple, List, Optional, Dict, Any
from utils import logger

class Segmenter:
    """图像切割器
    """
    def __init__(self, input_path: str, output_path: str, img_clip: Tuple[slice], img_scale: float, angle_point: Optional[List], min_height_rate: float, eps: float, distance: float) -> None:
        """构造函数

        Args:
            input_path (str): 原始图片路径
            output_path (str): 切割后图片输出地址
            img_clip (tuple[slice]): 图像裁切索引
            img_scale (float): 图像缩放大小
            angle_point (list | optional): 角点位置
            min_height_rate (float): 分割直线的最小长度与高度之比
            eps (float): 聚类直线的最小距离
            distance (float): 分割直线的最小距离
        """
        self.input_path = input_path
        self.output_path = output_path
        self.img_clip = img_clip
        self.img_scale = img_scale
        self.angle_point = angle_point
        self.min_height_rate = min_height_rate
        self.eps = eps
        self.distance = distance
        self.clean()

    @staticmethod
    def builder(config: Dict[str, Any]) -> Segmenter:
        """分割器构造器

        Args:
            config (Dict[str, Any]): 配置

        Returns:
            Segmenter: 分割器
        """
        return Segmenter(input_path=config["input_path"], output_path=config["output_path"], img_clip=config["img_clip"], img_scale=config["img_scale"], angle_point=config["angle_point"], min_height_rate=config["min_height_rate"], eps=config["eps"], distance=config["distance"])
    
    def clean(self):
        """清理 temp 文件夹
        """
        if not os.path.exists(self.output_path):
            os.mkdir(self.output_path)
        else:
            shutil.rmtree(self.output_path)
            os.mkdir(self.output_path)
    
    @logger
    def segment(self, img_name: str) -> None:
        """图像切割
        
        Args:
            img_name (str): 原始图片名称
        """
        img = cv2.imread(f"{self.input_path}/{img_name}", 1)
        img = img[self.img_clip]
        img = cv2.resize(img, None, fx=self.img_scale, fy=self.img_scale, interpolation = cv2.INTER_CUBIC)
        
        # 角点定位
        if self.angle_point is not None:
            src_pts = np.array(self.angle_point, dtype=np.float32)
            dst_pts = np.array([[0, 0], [img.shape[1], 0], [img.shape[1], img.shape[0]], [0, img.shape[0]]], dtype=np.float32)
            M = cv2.getPerspectiveTransform(src_pts, dst_pts)
            img = cv2.warpPerspective(img, M, (img.shape[1], img.shape[0]))
        
        # 预处理
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.equalizeHist(gray)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(gray)
        blurred = cv2.GaussianBlur(enhanced, (3, 3), 0)
        edge = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 13, -2)

        # 形态学处理
        rect_1 = cv2.getStructuringElement(cv2.MORPH_RECT, (edge.shape[0] // 50, 1))
        rect_2 = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 1))
        rect_3 = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 1))
        rect_4 = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 1))
        hough = cv2.morphologyEx(edge, cv2.MORPH_OPEN, rect_1.reshape(-1))
        hough = cv2.morphologyEx(hough, cv2.MORPH_CLOSE, rect_2.reshape(-1))
        hough = cv2.morphologyEx(hough, cv2.MORPH_OPEN, rect_3.reshape(-1), iterations=3)
        hough = cv2.morphologyEx(hough, cv2.MORPH_OPEN, rect_4.reshape(-1), iterations=30)

        # 概率霍夫线变换
        lines = cv2.HoughLinesP(hough, 1, 1 * np.pi / 180, 100, minLineLength=150, maxLineGap=10)
        lines = lines.reshape(-1, 4)
        
        # 聚类
        lines = cluster(lines=lines, min_height=self.min_height_rate * gray.shape[0], eps=self.eps)
        
        # for line in lines:
        #     x1, y1 ,x2, y2 = line
        #     cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
            
        # cv2.imshow("1", img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        
        # 区域切割
        self.clean()
        regions, self.coorinate = crop_regions(img, sort_lines(lines), self.distance)
        count = 0        
        for region in regions:
            if region.shape[0] <= self.distance or region.shape[1] <= 15:
                continue
            cv2.imwrite(f'{self.output_path}/{count}.jpg', region)
            count += 1
        self.count = count

# 聚类
def cluster(lines, min_height, eps):
    X = np.array([(line[2] * line[1] - line[0] * line[3]) / (line[3] - line[1]) for line in lines]).reshape(-1, 1)
    clustering = DBSCAN(eps=eps, min_samples=2).fit(X)
    
    # 合并直线
    merged_lines = []
    for i in range(max(clustering.labels_)+1):
        indices = np.where(clustering.labels_ == i)[0]
        if len(indices) > 1:
            x1 = lines[indices, 0][0]
            y1 = lines[indices, 1][0]
            x2 = lines[indices, 2][0]
            y2 = lines[indices, 3][0]
            merged_lines.append([x1, y1, x2, y2])

    # 过滤直线
    filtered_lines = []
    for line in merged_lines:
        x1, y1, x2, y2 = line
        length = np.sqrt((x2-x1)**2 + (y2-y1)**2)
        if length > min_height:
            filtered_lines.append(line)
    
    return filtered_lines

# 将直线按照从上到下的顺序排序
def sort_lines(lines):
    midpoints = [(line[0] + line[2]) / 2 for line in lines]
    return [line for _, line in sorted(zip(midpoints, lines), key=lambda x: x[0])]

# 计算分割区域
def crop_regions(img, lines, distance):
    regions = []
    coorinate = {}
    i = 0
    while i < len(lines) - 1: 
        (pt1, pt2, delta_index) = judge_width(i, lines, 1, distance)
        i += delta_index
        region = img[pt1[1]:pt2[1], pt1[0]:pt2[0]]
        regions.append(region)
        coorinate[len(regions) - 1] = (pt1[0] + pt2[0]) / 2
    return regions, coorinate

# 计算切割区域宽度
def judge_width(i, sorted_lines, delta_index, distance):
    line1 = sorted_lines[i]
    if i + delta_index < len(sorted_lines):
        line2 = sorted_lines[i + delta_index]
    else:
        x1, _, x2, _ = line1
        pt1 = (min(x1, x2), 0)
        pt2 = (max(x1, x2), 1000)
        return (pt1, pt2, delta_index)
    x1, _, x2, _ = line1
    x3, _, x4,_ = line2
    pt1 = (min(x1, x2), 0)
    pt2 = (max(x3, x4), 1000)
    if pt2[0] - pt1[0] <= distance:
        if i + delta_index < len(sorted_lines):
            delta_index += 1
            return judge_width(i, sorted_lines, delta_index, distance)
        else:
            return (pt1, pt2, delta_index)
    else:
        return (pt1, pt2, delta_index)

        
if __name__ == "__main__":
    config = {
        'input_path': './pic',
        'output_path': './ai/ocr/temp',
        'img_clip': (slice(700, 2800), slice(0, 5000)),
        'img_scale': 0.3,
        'angle_point': [[50, 0], [1332, 0], [1382, 630], [0, 630]],
        'min_height_rate': 0.5,
        'eps': 2,
        'distance': 10
    }
    
    segmenter = Segmenter.builder(config)
    segmenter.segment('4.jpg')
    print(segmenter.coorinate)
    