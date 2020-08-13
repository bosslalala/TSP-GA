import random
# 城市类，有三个参数，城市id，x坐标，y坐标
class City:
    def __init__(self, id):
        self.id = id
        self.x = random.randrange(100)
        self.y = random.randrange(100)

    # 打印城市信息
    def get_info(self):
        print("id:%2d, %2d, %2d" % (self.id, self.x, self.y))
        # print(str(self.x) + ", " + str(self.y) + ", " + str(self.id))