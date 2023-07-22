import torch
from torch.utils.data import Dataset, DataLoader
from utils.data_preprocess import DataPreprocesser, get_image

class SimCharDataSet(Dataset):
    """形近汉字匹配数据加载器
    """
    def __init__(self, file_path: str, font_path: str, dataset_size: int, split: str, size: int=32, prop: float=0.0) -> None:
        """构造函数

        Args:
            file_path (str): 数据文件路径
            font_path (str): 字体文件路径
            dataset_size (int, optional): 数据集的大小.
            split (str): 分隔符
            size (int, optional): 图片大小. Defaults to 32.
            prop (float, optional): 相似容限. Defaults to 0.0 .
        """
        self.data_preprocesser = DataPreprocesser(file_path=file_path, dataset_size=dataset_size, prop=prop, split=split)
        self.font_path = font_path
        self.size = size
        
    def __getitem__(self, index) -> tuple[str]:
        """按索引获取两个汉字的匹配组

        Args:
            index (int): 索引

        Returns:
            tuple(str): 两个汉字构成的元组
        """
        return (torch.from_numpy(get_image(self.data_preprocesser[index], font_path=self.font_path, size=self.size)).unsqueeze(0).float(), torch.tensor(self.data_preprocesser.get_label(index)).unsqueeze(0).float())
    
    def __len__(self) -> int:
        """获取匹配组的数量

        Returns:
            int: 数量
        """
        return self.data_preprocesser.count
    
if __name__ == "__main__":
    file_path = './ai/character_match/data/data_0.txt'
    font_path = './ai/character_match/fonts/simkai.ttf'
    dataset = SimCharDataSet(file_path=file_path, font_path=font_path, dataset_size=50, split="")

    batch_size = 8
    shuffle = True
    num_workers = 4
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=shuffle, num_workers=num_workers)
    
    for batch in dataloader:
        inputs, labels = batch
        print(f"inputs: {inputs}")
        print(f"labels: {labels}")