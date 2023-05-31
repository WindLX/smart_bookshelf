import os
import cv2
import numpy as np
import shutil
from typing import Tuple, List, Optional
from utils import logger

class Segmenter:
    """图像切割器
    """
    def __init__(self, input_path: str, output_path: str, img_clip: Tuple[slice], img_scale: float, angle_point: Optional[List]) -> None:
        """构造函数

        Args:
            input_path (str): 原始图片路径
            output_path (str): 切割后图片输出地址
            img_clip (tuple[slice]): 图像裁切索引
            img_scale (float): 图像缩放大小
            angle_point (list | optional): 角点位置
        """
        self.input_path = input_path
        self.output_path = output_path
        self.img_clip = img_clip
        self.img_scale = img_scale
        self.angle_point = angle_point
        
        self.clean()
            
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
        
        if self.angle_point is not None:
            src_pts = np.array(self.angle_point, dtype=np.float32)
            dst_pts = np.array([[0, 0], [img.shape[1], 0], [img.shape[1], img.shape[0]], [0, img.shape[0]]], dtype=np.float32)
            M = cv2.getPerspectiveTransform(src_pts, dst_pts)
            img = cv2.warpPerspective(img, M, (img.shape[1], img.shape[0]))
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        cv2.equalizeHist(gray)
        
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(gray)
        
        blurred = cv2.GaussianBlur(enhanced, (3, 3), 0)
        
        edge = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 13, -2)

        rect_1 = cv2.getStructuringElement(cv2.MORPH_RECT, (edge.shape[0] // 50, 1))
        rect_2 = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 1))
        rect_3 = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 1))
        rect_4 = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 1))

        hough = cv2.morphologyEx(edge, cv2.MORPH_OPEN, rect_1.reshape(-1))
        hough = cv2.morphologyEx(hough, cv2.MORPH_CLOSE, rect_2.reshape(-1))
        hough = cv2.morphologyEx(hough, cv2.MORPH_OPEN, rect_3.reshape(-1), iterations=3)
        hough = cv2.morphologyEx(hough, cv2.MORPH_OPEN, rect_4.reshape(-1), iterations=30)

        lines = cv2.HoughLinesP(hough, 1, 1 * np.pi / 180, 100, minLineLength=150, maxLineGap=10)

        # for line in lines:
        #     x1, y1 ,x2, y2 = line[0]
        #     cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 1)
            
        # cv2.imshow("1", blurred)
        cv2.imshow("1", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        # 将直线按照从上到下的顺序排序
        def sort_lines(lines):
            midpoints = [(line[0][0] + line[0][2]) / 2 for line in lines]
            return [line for _, line in sorted(zip(midpoints, lines), key=lambda x: x[0])]

        # 计算分割区域
        def crop_regions(img, lines):
            sorted_lines = sort_lines(lines)
            regions = []
            coorinate = {}
            i = 0
            while i < len(sorted_lines) - 1: 
                (pt1, pt2, delta_index) = judge_width(i, sorted_lines, 1)
                i += delta_index
                region = img[pt1[1]:pt2[1], pt1[0]:pt2[0]]
                regions.append(region)
                coorinate[len(regions) - 1] = (pt1[0] + pt2[0]) / 2
            return regions, coorinate

        # 计算切割区域宽度
        def judge_width(i, sorted_lines, delta_index):
            line1 = sorted_lines[i]
            if i + delta_index < len(sorted_lines):
                line2 = sorted_lines[i + delta_index]
            else:
                x1, _, x2, _ = line1[0]
                pt1 = (min(x1, x2), 0)
                pt2 = (max(x1, x2), 1000)
                return (pt1, pt2, delta_index)
            x1, _, x2, _ = line1[0]
            x3, _, x4,_ = line2[0]
            pt1 = (min(x1, x2), 0)
            pt2 = (max(x3, x4), 1000)
            if pt2[0] - pt1[0] <= 15:
                if i + delta_index < len(sorted_lines):
                    delta_index += 1
                    return judge_width(i, sorted_lines, delta_index)
                else:
                    return (pt1, pt2, delta_index)
            else:
                return (pt1, pt2, delta_index)

        regions, self.coorinate = crop_regions(img, lines)

        count = 0
        
        self.clean()
        
        for region in regions:
            if region.shape[0] <= 10 or region.shape[1] <= 15:
                continue
            # print(region.shape)
            cv2.imwrite(f'{self.output_path}/{count}.jpg', region)
            count += 1
        self.count = count
        
        
if __name__ == "__main__":
    input_path = './pic'
    output_path = './ai/ocr/temp'
    img_clip = (slice(700, 2800), slice(0, 5000))
    img_scale = 0.3
    angle_point = [[50, 0], [1332, 0], [1382, 630], [0, 630]]
    
    segmenter = Segmenter(input_path=input_path, output_path=output_path, img_clip=img_clip, img_scale=img_scale, angle_point=angle_point)
    segmenter.segment('4.jpg')
    print(segmenter.coorinate)
    