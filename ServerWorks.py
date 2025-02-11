import requests

class ServerManager():
    def __init__(self, BASE_IP="http://127.0.0.1:5000"):
        self.BASE_IP = BASE_IP

    def login(self,email:str,password:str) -> str:
        MainRequest = requests.get(self.BASE_IP + f"/login/{email}/{password}")
        return MainRequest.text
    
    def sign_up(self,email:str,password:str,username:str) -> str:
        return requests.get(self.BASE_IP + f"/sign_up/{email}/{password}/{username}").text
    
    def load_own_trail(self,trail_name,email,password,file):
        main_req = requests.post(url=str(self.BASE_IP + f"/add_trail/{trail_name}/{email}/{password}"),files={"file" : file}).text
        return main_req
    

TestManager = ServerManager()


    
        

