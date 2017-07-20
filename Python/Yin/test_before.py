#-*- coding: UTF-8 -*- 
from circulation_before_improve import *
from copy import deepcopy
import readdata
import time

fw_result = open("resulf_before.txt",'w')

for filename in list_all:
    coordinates,city_capacity_table,service_time_windows = get_data(filename)

    city_num=coordinates.shape[0]                               #城市的数量
    distance_table=get_distance_table(coordinates)              #距离矩阵
    

    times_result = []
    cost_best_result = []
    vehicle_result = []
    
    print('filename: ' + filename)
    fw_result.write('\n' + filename + ':\n')
    times=0
    while(times<10):
        start=time.clock() 
        costbest,pathbest,vehicle_need=get_result(coordinates,city_capacity_table,service_time_windows,distance_table,city_num)
        end=time.clock()
        times_result.append(str(end-start)+'\t')
        cost_best_result.append(str(costbest)+'\t')
        vehicle_result.append(str(vehicle_need)+'\t')
        print "%f s"%(end-start)
        print costbest
        print pathbest
        print vehicle_need
        times+=1
    fw_result.writelines(times_result)
    fw_result.write('\n')
    fw_result.writelines(cost_best_result)
    fw_result.write('\n')
    fw_result.writelines(vehicle_result)
    fw_result.write('\n')

fw_result.close()

        

        
