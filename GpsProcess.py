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
    return {"vag_speed": avg_speed, "distance": distance}


print(get_gps_info({"GPSData": {"981014": {"lat": 55.7182066, "lon": 37.4647445, "speed": 0.0, "bearing": 0.0, "altitude": 178.10000610351562, "accuracy": 13.890999794006348}, "981021": {"lat": 55.7182205, "lon": 37.4647281, "speed": 0.19930143654346466, "bearing": 326.3775329589844, "altitude": 178.10000610351562, "accuracy": 12.26200008392334}, "981024": {"lat": 55.7182284, "lon": 37.4646426, "speed": 1.6179509162902832, "bearing": 276.3631896972656, "altitude": 178.10000610351562, "accuracy": 30.131000518798828}, "981025": {"lat": 55.7182244, "lon": 37.46463, "speed": 1.4691193103790283, "bearing": 270.9803161621094, "altitude": 178.10000610351562, "accuracy": 36.08700180053711}, "981026": {"lat": 55.718230685792726, "lon": 37.46463717380033, "speed": 0.7486554384231567, "bearing": 282.5982360839844, "altitude": 166.55747703232325, "accuracy": 48.0}, "981027": {"lat": 55.7182306, "lon": 37.4646378, "speed": 0.46457797288894653, "bearing": 296.6636657714844, "altitude": 178.10000610351562, "accuracy": 50.61000061035156}}, "name": "class", "discription": "\u0445\u043e\u0436\u0443  \u043f\u043e \u043a\u043b\u0430\u0441\u0441\u0443 ", "MinDistance": "20"}))