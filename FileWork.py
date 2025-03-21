from kivy import platform
import json
import os
from os import listdir
from os.path import isfile, join
from ServerWorks import ServerManager

MainServerManager = ServerManager()

if platform == "android":
    from android.storage import primary_external_storage_path
    from android import mActivity
    from android.permissions import Permission, check_permission
    from androidstorage4kivy import SharedStorage, Chooser, ShareSheet
    
class FileManager():
    def __init__(self,cache_dir: str = ""):
        if platform == "android":
            cache_dir = SharedStorage().get_cache_dir()
        else:
            cache_dir = os.getcwd()
            
        self.own_saved_trails_dir = "own_saved_trails"
        self.cache_dir = cache_dir
        
    def MakeDirs(self):
        if self.own_saved_trails_dir not in os.listdir(self.cache_dir):
            path = os.path.join(self.cache_dir, self.own_saved_trails_dir)
            os.makedirs(path)
    
    def load_config(self):
        if "config.json" not in os.listdir(self.cache_dir):
            return False
        else:
            with open(os.path.join(self.cache_dir,"config.json"), "r") as file:
                return json.load(file)
    
    def configure(self, **kwargs):
        with open(os.path.join(self.cache_dir,"config.json"), "w") as file:
            json.dump(kwargs,file,ensure_ascii=True)

    def save_trail(self,JsonDict, FileName):
        FileName = os.path.join(self.cache_dir,self.own_saved_trails_dir,f"{FileName}.json")
        with open(str(FileName), "w") as file:
            json.dump(JsonDict, file)
        if platform == "android":
            SharedStorage().copy_to_shared(private_file=FileName)
            
    def get_own_saved_trails_info(self):
        trail_info_list = []
        for file_name in os.listdir(self.own_saved_trails_dir):
            with open(str(self.own_saved_trails_dir + "/" + file_name), "r") as file:
                json_dict = json.load(file)
                trail_info_list.append({"name":json_dict["name"], "description" : json_dict["description"]})
        return trail_info_list
    
    def load_own_trail(self,trail_name,email,password):
        if f"{trail_name}.json" in os.listdir(self.own_saved_trails_dir):       
            with open(os.path.join(self.cache_dir, self.own_saved_trails_dir, trail_name + ".json"), "r") as file:
                JSON_dict = json.load(file)
                distance = JSON_dict["distance"]
                date = JSON_dict["date"]
                description = JSON_dict["description"]
                sec_dict = JSON_dict["GPSData"][min(list(JSON_dict["GPSData"].keys()))]
                
            file = open(os.path.join(self.cache_dir, self.own_saved_trails_dir, trail_name + ".json"), "r")
            MainServerManager.load_own_trail(trail_name,email,distance,date,sec_dict["lat"],sec_dict["lon"],description,password,file)
            file.close()
            return True
    
    def save_public_trail(self,JsonDict,trail_id):
        FileName = "PublicTrail"
        FileName = os.path.join(self.cache_dir,f"{FileName}.json")
        config = self.configure()
        email = config["email"]
        password = config["password"]
        with open(str(FileName), "w") as file:
            json.dump(JsonDict, file)
        if platform == "android":
            SharedStorage().copy_to_shared(private_file=FileName)
        file = open(str(FileName), "r")
        req = MainServerManager.load_public_trail(trail_id,email,password,file)
        file.close()
        return req
        
        
