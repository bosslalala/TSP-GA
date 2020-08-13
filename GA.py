#用遗传算法求解TSP
import random
import time
import numpy as np
import math
import copy
from City import City
from Path import Path
import csv

class GA:

    #def __init__(self):
    #    self.init_state()
    def __init__(self):
        self.init_state()
        self.init_city()
        with open("city.csv",'w') as f:
            csv_write = csv.writer(f, lineterminator='\n')
            for i in range(self.hard):
                csv_write.writerow([i, self.cities[i].x, self.cities[i].y])
    #构建矩形城市点
    def init_city(self):
        for i in range(13):
            self.cities[i].x = 50 + i * 10
            self.cities[i].y = 50
        for i in range(12):
            self.cities[13+i].x = 170
            self.cities[13+i].y = 50 + (i+1)*10
        for i in range(13):
            self.cities[25+i].x = 170 - (i+1)*10
            self.cities[25+i].y = 170
        for i in range(12):
            self.cities[38+i].x = 50
            self.cities[38+i].y = 170 - (i+1)*10
    #初始化参数
    def init_state(self):
        self.size = 100
        self.hard = 50
        self.cities = [City(i) for i in range(self.hard)]
        self.original = [Path() for i in range(self.size)]
        self.tempPaths = []
        self.minDistance = 10000
        self.bestPath = self.original[0]
        self.file = "bestPath.csv"


    # 计算两点间距离
    def pointDistance(self, a, b):
        square = np.square(a.x - b.x) + np.square(a.y - b.y)
        distance = np.sqrt(square)
        return distance

    # 计算路径距离
    def pathDistance(self, path):
        distance = 0
        temp = 0
        for i in range(self.hard-1):
            temp = self.pointDistance(self.cities[path.path[i]], self.cities[path.path[i + 1]])
            distance = distance + temp
        #distance = distance + self.pointDistance(self.cities[path.path[self.hard-1]], self.cities[path.path[0]])
        path.distance = distance

    # 更新全局最小值
    def renewDistance(self):
        for i in range(self.size):
            self.pathDistance(self.original[i])
            # print(original[i].distance)
            if (self.original[i].distance < self.minDistance):
                self.minDistance = self.original[i].distance
                self.bestPath = self.original[i]

    # 有放回随机竞争策略选择下一代母体
    def select(self):
        lucky_one = random.randrange(self.size)
        lucky_two = random.randrange(self.size)
        if (self.original[lucky_one].distance < self.original[lucky_two].distance):
            return self.original[lucky_one]
        else:
            return self.original[lucky_two]

    # 染色体交叉
    def cross(self, a, b):
        # 以80%的概率发生交叉
        if random.randrange(10) < 8:
            cross_loaction = random.randrange(self.hard)
            temp1 = a.path[cross_loaction]
            temp2 = a.path[(cross_loaction + 1) % self.hard]
            temp3 = b.path[cross_loaction]
            temp4 = b.path[(cross_loaction + 1) % self.hard]
            if (temp1 != temp3 and temp1 != temp4 and temp2 != temp3 and temp2 != temp4):
                for i in range(self.hard):
                    if (a.path[i] == temp3):
                        a.path[i] = temp1
                    if (a.path[i] == temp4):
                        a.path[i] = temp2
                a.path[cross_loaction] = temp3
                a.path[(cross_loaction + 1) % self.hard] = temp4

                for i in range(self.hard):
                    if (b.path[i] == temp1):
                        b.path[i] = temp3
                    if (b.path[i] == temp2):
                        b.path[i] = temp4
                b.path[cross_loaction] = temp1
                b.path[(cross_loaction + 1) % self.hard] = temp2

    # 基因变异
    def mutation(self, a):
        # 以5%的概率变异
        if (random.randrange(100) <= 5):
            mutation_loc1 = random.randrange(self.hard)
            mutation_loc2 = random.randrange(self.hard)
            temp = a.path[mutation_loc1]
            a.path[mutation_loc1] = a.path[mutation_loc2]
            a.path[mutation_loc2] = temp

    # 构建新种群
    def newPopulation(self):
        for i in range(self.size//2-10):
            father = self.select()
            mother = self.select()
            son = copy.deepcopy(father)
            doughter = copy.deepcopy(mother)
            # 交叉
            self.cross(son, doughter)
            self.cross(son, doughter)
            self.cross(son, doughter)
            self.cross(son, doughter)
            self.cross(son, doughter)
            self.cross(son, doughter)

            # 变异
            self.mutation(son)
            self.mutation(son)
            self.mutation(doughter)
            self.mutation(doughter)
            # 加入新种群中
            self.tempPaths.append(son)
            self.tempPaths.append(doughter)
        for i in range(19):
            self.tempPaths.append(Path())
        self.tempPaths.append((self.bestPath))
        self.original = self.tempPaths
        #self.original.append(Path())
        #self.original.append(self.bestPath)

    # 进化迭代
    def iteration(self, n, m):
        with open(self.file,'w') as f:
            csv_write = csv.writer(f,lineterminator='\n')
            j = 0
            for i in range(n):
                self.tempPaths = []
                self.renewDistance()
                self.newPopulation()
                j = j + 1
                if (j == m):
                    data = list(self.bestPath.path)
                    data.append(self.minDistance)
                    csv_write.writerow(data)
                    print("%d, mindistance = %d" % (i, self.minDistance))
                    j = 0