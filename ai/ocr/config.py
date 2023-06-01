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
