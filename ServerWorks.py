import requests
from colorama import Fore, Back, Style

class ServerManager():
    def __init__(self, BASE_IP="http://127.0.0.1:5000"):
        self.BASE_IP = BASE_IP

    def login(self,email:str,password:str) -> str:
        MainRequest = requests.get(self.BASE_IP + f"/login/{email}/{password}")
        return MainRequest.text
    
    def sign_up(self,email:str,password:str,username:str) -> str:
        return requests.get(self.BASE_IP + f"/sign_up/{email}/{password}/{username}").text
    
    def load_own_trail(self,trail_name,email,distance,date,start_lat,start_lon,description,password,file):
        try:
            main_req = requests.post(url=str(self.BASE_IP + f"/add_trail/{trail_name}/{distance}/{date}/{start_lat}/{start_lon}/{description}/{email}/{password}"),files={"file" : file}).text
            return main_req
        except:
            pass
    
    def get_all_trails(self,sort_type,location,page):
        try:
            MainRequest = requests.get(self.BASE_IP + f"/get_all_trails/{sort_type}/{location}/{page}").json()
        except:
            MainRequest = {"data" : []}
        print(Fore.RED +  str(MainRequest["data"]))
        return MainRequest["data"]
        
    
TestManager = ServerManager()


    
        

