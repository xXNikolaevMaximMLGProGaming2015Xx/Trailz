import math
def sqr(value):
    return value*value

def get_gps_info(gpsDict:dict):
    distance = 0
    radius =  6369427
    pi = 3.1415
    MainList = []
    for i in list(gpsDict["GPSData"].items()):
        MainList.append([i[1]["lat"],i[1]["lon"]])
    for i in range(len(MainList) - 1):
        distance += math.sqrt(sqr(2*pi*radius*((MainList[i][1] - MainList[i+1][1])/360)) + sqr(2*pi*radius*((MainList[i][0] - MainList[i+1][0])/360)) )
    distance = round(distance / 1000, 3)
    avg_speed = distance / ((max([int(i) for i in list(gpsDict["GPSData"].keys())]) - min([int(i) for i in list(gpsDict["GPSData"].keys())]))/3600)
    avg_speed = round(avg_speed, 1)
    return {"avg_speed": avg_speed, "distance": distance}


