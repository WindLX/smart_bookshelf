# config = {
#     'segment_config': {
#         'input_path': './pic',
#         'output_path': './temp',
#         'img_clip': (slice(700, 2800), slice(0, 5000)),
#         'img_scale': 0.3,
#         'angle_point': [[50, 0], [1332, 0], [1382, 630], [0, 630]],
#         'min_height_rate': 0.5,
#         'eps': 2,
#         'distance': 10
#     },
#     'ocr_config': {
#         'input_path': './temp',
#         'use_gpu': True,
#         'ocr_thread_count': 4
#     }
# }

import json
from typing import Dict, Any

class Configer:
    def __init__(self, file_path: str) -> None:
        """配置器

        Args:
            file_path (str): 配置文件的路径
        """
        self.file_path = file_path
        self.config = self.load_config(file_path)
    
    def load_config(self, file_path) -> Dict[str, Any]:
        """加载配置

        Args:
            file_path (str): 配置文件的路径

        Returns:
            Dict[str, Any]: 配置
        """
        with open(file_path, 'r') as file:
            json_data = file.read()
            config = json.loads(json_data)
            config['segment_config']['img_clip'] = (slice(config['segment_config']['img_clip'][0][0], config['segment_config']['img_clip'][0][1]), slice(config['segment_config']['img_clip'][1][0], config['segment_config']['img_clip'][1][1]))
            return config
    
    def __getitem__(self, key: str) -> Any:
        """获取键值

        Args:
            key (str): 键名

        Returns:
            Any: 键值
        """
        return self.config[key]
    
    def __setitem__(self, key: str, value: Any):
        """设置键值

        Args:
            key (str): 键名
            value (Any): 键值
        """
        self.config[key] = value
    
    def update_config(self):
        """更新配置
        """
        self.config = self.load_config(self.file_path)

if __name__ == "__main__":
    configer = Configer('./ai/ocr/config.json')
    config = configer.config
    print(config)
