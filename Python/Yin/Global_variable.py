# -*- coding: utf-8 -*-
import numpy as np
from numpy import linalg as LA
import readdata

ant_num=15                          #蚂蚁的数量
ALPHA=1.0                           #信息素启发式因子
BETA=3.0                            #期望值启发式因子
RHO=0.1                             #信息素的挥发因子
NC_MAX=500                          #轮询的次数
Q=100                               #信息素强度
VEHICLE_CAPACITY=50                 #配送车辆的最大装载量
FIXED_COST=50                       #每辆车的固定成本50元/次
TRANS_COST=4                        #单位里程的运输费用为4元/km
RUN_SPEED=2                         #车辆行驶速度为2km/min
TRANS_START_TIME=0                  #车辆凌晨0点从配送中心出发,以分钟计数
M1=30                               #单个配送点早到最大惩罚系数
M2=60                               #单个配送点迟到最大惩罚系数
C0=20                               #货物的单位价格
RHO1=0.001                          #运输途中的货损因子


list_r=['R101', 'R102', 'R103', 'R104', 'R105', 'R106', 'R107', 'R108', 'R109', 'R110', 'R111', 'R112']
list_c=['C101', 'C102', 'C103', 'C104', 'C105', 'C106', 'C107', 'C108', 'C109']
list_rc=['RC101', 'RC102', 'RC103', 'RC104', 'RC105', 'RC106', 'RC107', 'RC108']
list_all=list_r+list_c+list_rc

#list_all=['R101','C101','RC101']

#CATALOG="..\\input\\"
CATALOG="//home//fan//Projects//Python//Yin//input//"

#惩罚函数
def get_punishment(ti,ta,tb,tc,td):
    if(ti<ta):
        return M1
    elif(ta<=ti<tb):
        return M1*(tb-ti)/(tb-ta)
    elif(tb<=ti<=tc):
        return 0
    elif(tc<ti<=td):
        return M2*(ti-tc)/(td-tc)
    else:
        return M2

#获取各个城市之间的距离矩阵
def get_distance_table(coordinates):
    num=coordinates.shape[0]
    distance_table=np.zeros((num,num))
    for i in range(num):
        for j in range(i,num):
            distance_table[i][j]=distance_table[j][i]=LA.norm(coordinates[i]-coordinates[j])
    return distance_table

def get_data(filename):
    #数据集文件名
    FILENAME = CATALOG+filename + '.txt'
    #读取数据存储为float类型的list数组
    data_table_float = readdata.readData(FILENAME)
    #解析出coordinates暂存为list格式
    coordinates_list = readdata.readCoords(data_table_float)
    #解析出demand暂存为list格式
    demand_list = readdata.readDemand(data_table_float)
    #解析出time_windows暂存为list格式
    time_windows_list = readdata.readTime(data_table_float)
    
    #将list格式的coordinates转为np对象
    coordinates = np.array(coordinates_list)
    #将list格式的demand转为np对象
    city_capacity_table = np.array(demand_list)
    #将list格式的time_windows转为np对象
    service_time_windows = np.array(time_windows_list)
    return coordinates,city_capacity_table,service_time_windows
