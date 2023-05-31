from concurrent.futures import ThreadPoolExecutor
import os
from paddleocr import PaddleOCR
from typing import List, Dict, Tuple, Any
from config import config
from utils import logger

class OCRer:
    """OCR 文字识别器"""
    def __init__(self, input_path: str, use_gpu: bool, thread_count: int=1) -> None:
        """构造函数

        Args:
            input_path (str): 待识别的图片所在目录
            use_gpu (bool): 是否使用 GPU
            thread_count (int, optional): 线程数. Defaults to 1.
        """
        self.input_path = input_path
        self.use_gpu = use_gpu
        self.thread_count = thread_count

    def __get_image_files(self, input_path: str) -> List[str]:
        """获取目录下的所有图片文件

        Args:
            input_path (str): 图片文件目录

        Returns:
            list[str]: 文件
        """
        file_list = []
        for root, _, files in os.walk(input_path):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    file_path = os.path.join(root, file)
                    file_list.append(file_path)
        return file_list
    
    def __process_image(self, img_path: str) -> Tuple:
        """对单个文件进行 OCR 识别

        Args:
            img_path (str): 图像路径

        Returns:
            tuple: 识别结果
        """
        ocr = PaddleOCR(use_angle_cls=True, lang="ch", use_gpu=self.use_gpu, show_log=False)
        result = ocr.ocr(img_path, cls=True)
        return (img_path, result)
    
    def __ocr(self, imgs: List[str]) -> Dict[str, Any]:
        """多线程识别

        Args:
            imgs (list[str]): 图片路径

        Returns:
            dict[str]: 识别结果
        """
        results = {}
        with ThreadPoolExecutor(max_workers=self.thread_count) as executor:
            futures = [executor.submit(self.__process_image, img) for img in imgs]
            for future in futures:
                result = future.result()
                if len(result[1]) > 0 and len(result[1][0]) > 0:
                    file_name = os.path.splitext(os.path.basename(result[0]))[0]
                    results[int(file_name)] = result[1]
                    print(f"Finish [ocr: {int(file_name)}]")
        return results

    @logger
    def run_ocr(self) -> Dict[str, Any]:
        """执行 OCR 识别
        """
        files = self.__get_image_files(self.input_path)
        return self.__ocr(files)
    
if __name__ == "__main__":
    ocrer = OCRer(input_path=config['output_path'], thread_count=config['ocr_thread_count'])
    res = ocrer.run_ocr()
    print(res)