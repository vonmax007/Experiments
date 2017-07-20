# -*- coding:utf-8 -*-

import numpy as np
from numpy import linalg as LA
from Global_variable import *

def get_result(coordinates,city_capacity_table,service_time_windows,distance_table,city_num):
    
    eta=1.0/(distance_table+np.diag([1e10]*city_num))       #启发函数矩阵，表示蚂蚁从城市i转移到矩阵j的期望程度
    pheromone_table=np.ones((city_num,city_num))            #信息素矩阵
    tabu=np.zeros((ant_num,city_num*2)).astype(int)         #路径记录表即tabu表
    costbest=np.zeros(NC_MAX)                               #各代及其之前遇到的最佳代价
    #each_costbest=np.zeros((NC_MAX,4))                        #各代及其之前遇到的最佳代价的各小项开销
    pathbest = np.zeros((NC_MAX,city_num*2)).astype(int)    #各代及其之前遇到的最佳路径长度,考虑到中间会插入原点，矩阵的列数开大一倍
    iter_pathbest=np.zeros(city_num*2)                      #迭代最优解
    vehicle_need_table=np.ones(NC_MAX)                      #各代需要派遣的车辆数量

    current_capacity=0
    current_time=0

    NC=0
    while NC<NC_MAX:
        length=np.zeros(ant_num)            #计算各个蚂蚁的路径距离
        capacity=np.zeros(ant_num)          #计算各个蚂蚁路过城市的载重量
        cost=np.zeros(ant_num)              #计算各个蚂蚁的开销
        #each_cost=np.zeros((ant_num,4))       #保存各个蚂蚁的各项开销
        vehicle_need=np.ones(ant_num)       #计算各个蚂蚁回配送中心的次数，即车辆需要的数量
        punishment=np.zeros(ant_num)        #计算各个蚂蚁的惩罚值
        wastage=np.zeros(ant_num)           #计算各个蚂蚁的冷链损耗
        current_time=TRANS_START_TIME
        tabu=np.zeros((ant_num,city_num*2)).astype(int)         #路径记录表即tabu表
        for i in range(ant_num):
            visiting=tabu[i,0]              #当前所在的城市
            unvisited=set(range(city_num))  #未访问的城市
            unvisited_bank=set()
            unvisited.remove(visiting)      #删除当前所在城市元素
        
            current_capacity=0              #当前载货量
            tabu_b=1                        #tabu表第二个维度的下标
            j=1
            while(j<city_num):#循环city_num-1次，访问剩余的city_num-1个城市
                if(len(unvisited)==0):
                    unvisited|=unvisited_bank       #回到配送中心，取并集求出未访问的城市
                    unvisited_bank =set()
                    vehicle_need[i]+=1
                    tabu_b+=1
                    current_capacity=0
                    length[i]+=distance_table[visiting][0]
                    visiting=0
                    current_time=TRANS_START_TIME

                #每次用轮盘法选择下一个要访问的城市
                listunvisited=list(unvisited)
                probtrans=np.zeros(len(listunvisited))

                for k in range(len(listunvisited)):
                    probtrans[k]=np.power(pheromone_table[visiting][listunvisited[k]],ALPHA)\
                                  *np.power(eta[visiting][listunvisited[k]],BETA)

                cumsumprobtrans=(probtrans/sum(probtrans)).cumsum()
                cumsumprobtrans-=np.random.rand()

                k=listunvisited[np.where(cumsumprobtrans>0)[0][0]]#下一个将要访问的城市
                current_capacity+=city_capacity_table[k]

                #判断下一个将要访问的城市是否满足约束条件
                if(current_capacity>VEHICLE_CAPACITY):      #超过容量约束了
                    current_capacity-=city_capacity_table[k]
                    unvisited.remove(k)
                    unvisited_bank.add(k)
                    j-=1
                else:
                    tabu[i,tabu_b]=k
                    unvisited.remove(k)
                    length[i]+=distance_table[visiting][k]
                    current_time+=distance_table[visiting][k]/RUN_SPEED
                    punishment[i]+=get_punishment(current_time,service_time_windows[k][0],\
                                                  service_time_windows[k][1],service_time_windows[k][2],service_time_windows[k][3])
                    wastage[i]+=C0*RHO1*(current_time-TRANS_START_TIME)*city_capacity_table[k]
                    visiting=k
                    tabu_b+=1
                j+=1

            length[i]+=distance_table[visiting][tabu[i,0]]      #蚂蚁的路径距离包括最后一个城市和第一个城市之间的距离
            #each_cost[i]=FIXED_COST*vehicle_need[i],length[i]*TRANS_COST,punishment[i],wastage[i]
            #cost[i]=sum(each_cost[i])
            cost[i]=0.1*FIXED_COST*vehicle_need[i]+0.7*length[i]*TRANS_COST+0.1*punishment[i]+0.1*wastage[i]

        if NC==0:
            costbest[NC]=cost.min()
            #each_costbest[NC]=each_cost[cost.argmin()].copy()
            pathbest[NC]=tabu[cost.argmin()].copy()           #拷贝出最佳路径
            vehicle_need_table[NC]=vehicle_need[cost.argmin()].copy()
        else:
            if cost.min()>costbest[NC-1]:
                costbest[NC] = costbest[NC-1]
                #each_costbest[NC] = each_costbest[NC-1]
                pathbest[NC] = pathbest[NC-1].copy()
                vehicle_need_table[NC]=vehicle_need_table[NC-1]
            else:
                costbest[NC]=cost.min()
                #each_costbest[NC]=each_cost[cost.argmin()].copy()
                pathbest[NC]=tabu[cost.argmin()].copy()           #拷贝出最佳路径
                vehicle_need_table[NC]=vehicle_need[cost.argmin()].copy()

        #更新信息素
        change_pheromone_table=np.zeros((city_num,city_num))
        for i in range(ant_num):
            for j in range(tabu_b):
                change_pheromone_table[tabu[i,j]][tabu[i,j+1]]+=Q/distance_table[tabu[i,j]][tabu[i,j+1]]

        pheromone_table=(1-RHO)*pheromone_table+change_pheromone_table
        
        NC+=1   #迭代次数加1

    return costbest[-1],pathbest[-1],vehicle_need_table[-1]
