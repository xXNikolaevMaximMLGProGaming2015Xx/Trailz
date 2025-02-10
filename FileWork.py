from kivy import platform
import json
import os

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

    def save_trail(self,JsonDict, FileName):
        JsonStr = json.dumps(JsonDict)
        FileName = os.path.join(self.cache_dir,self.own_saved_trails_dir,f"{FileName}.json")
        with open(str(FileName), "w") as file:
            json.dump(JsonDict, file)
        if platform == "android":
            SharedStorage().copy_to_shared(private_file=FileName)

