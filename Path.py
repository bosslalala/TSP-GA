import numpy as np

# 路径类
class Path:
    def __init__(self):
        self.hard = 50
        self.path = []
        self.distance = 1000000
        self.path = np.arange(self.hard)
        np.random.shuffle(self.path)

    # 打印路径信息
    def get_path_info(self):
        print(self.path)