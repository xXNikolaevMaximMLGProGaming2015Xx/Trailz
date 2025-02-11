import kivy
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.app import App
from kivy.properties import StringProperty
from kivy.clock import mainthread
from kivy.utils import platform
import time
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from FileWork import FileManager
from ServerWorks import ServerManager
if platform == "android":
    from plyer import gps

Builder.load_file(filename='main.kv')

#миксин для классов, работающих с жипиэс
class Wp(Widget):
    pass

class SavedTrail(Wp):
    pass
        
    
class LoginSignUpScreen(Screen):
    pass

class LoginScreen(Screen):
    pass

class SignUpScreen(Screen):
    pass

class GpsStartRecordingScreen(Screen):
    pass

class GpsStopRecordingScreen(Screen):
    pass

class GpsInfoScreen(Screen):
    pass


class MenuScreen(Screen):
    pass


class TestScreen(Screen):
    pass


class SavedTrailzScreen0(Screen):
    pass

MainFileManager = FileManager()
MainScreenManager = ScreenManager()
MainServerManager = ServerManager()

class Trailz(App):
    
    gps_location = StringProperty()
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._GPSJsonDict = {'GPSData':{}}
        self._jsonTrailPath = "saved_trails/"
        self._MinDistancePar = 1
        self._config = {}
    
    def login(self) -> None:
        email = MainScreenManager.get_screen("LoginScreen").ids.email.text
        password = MainScreenManager.get_screen("LoginScreen").ids.password.text
        #добавить поп ап
        if str(MainServerManager.login(email=email,password=password)) == "False":
            pass
        else:
            self.switch_toSTR("MenuScreen")
            MainFileManager.configure(email=email,password=password)
        
    def sign_up(self):
        email = MainScreenManager.get_screen("SignUpScreen").ids.email.text
        password = MainScreenManager.get_screen("SignUpScreen").ids.password.text
        username = MainScreenManager.get_screen("SignUpScreen").ids.username.text
        #добавить поп ап
        if str(MainServerManager.sign_up(email=email,password=password,username=username)) != "success":
            pass
        else:
            self.switch_toSTR("MenuScreen")
            MainFileManager.configure(email=email,password=password)
            
    def send_own_trail(self,trail_name):
        print(trail_name)
        #добавить поп ап
        #метод у файл менеджера, тк файл должен быть открыт во время загрузки
        MainFileManager.load_own_trail(trail_name, self._config["email"],self._config["password"])
        
        
    def saved_trails_forward_backward(self,oper_type:str, screen_num:int,lim:int)-> None: 
        if screen_num <= 0 or screen_num == lim:
            return None
        else:
            if oper_type == "f":
                self.switch_toSTR(f"SavedTrailzScreen{screen_num+1}")
            else:
                self.switch_toSTR(f"SavedTrailzScreen{screen_num-1}")
            print(MainScreenManager.get_screen(f"SavedTrailzScreen{screen_num-1}").ids)
                
    def creat_own_saved_trails_screen(self):
        
        trails_on_screen = 5
        position = 0
        saved_trails = MainFileManager.get_own_saved_trails_info()
        print(saved_trails)
        for i in range(int(len(saved_trails) /trails_on_screen) + 1):
            Grid = GridLayout(cols = 1)
            MainScreenManager.add_widget(Screen(name=f"SavedTrailzScreen{i}"))
            MainScreenManager.get_screen(f"SavedTrailzScreen{i}").ids["MainLayout"] = Grid
            MainScreenManager.get_screen(f"SavedTrailzScreen{i}").add_widget(Grid)
            MenuBtn = Button(text="В меню")
            MenuBtn.bind(on_press=lambda x:self.switch_toSTR("MenuScreen"))
            MainScreenManager.get_screen(f"SavedTrailzScreen{i}").ids.MainLayout.ids["ToMenuButton"] = MenuBtn
            MainScreenManager.get_screen(f"SavedTrailzScreen{i}").ids.MainLayout.add_widget(MenuBtn)
            if len(saved_trails) - i * trails_on_screen < trails_on_screen:
                for i1 in range(i*trails_on_screen,int(len(saved_trails)-i*5)%5):
                    trail = SavedTrail()
                    MainScreenManager.get_screen(f"SavedTrailzScreen{i}").ids.MainLayout.ids[f"trail{i1}"] = trail
                    MainScreenManager.get_screen(f"SavedTrailzScreen{i}").ids.MainLayout.ids[f"trail{i1}"].name = saved_trails[i1]["name"]
                    MainScreenManager.get_screen(f"SavedTrailzScreen{i}").ids.MainLayout.ids[f"trail{i1}"].discription = saved_trails[i1]["discription"]    
                    MainScreenManager.get_screen(f"SavedTrailzScreen{i}").ids.MainLayout.add_widget(trail)
            else:
                for i1 in range(i*trails_on_screen,(i+1)*trails_on_screen):
                    trail = SavedTrail()
                    MainScreenManager.get_screen(f"SavedTrailzScreen{i}").ids.MainLayout.ids[f"trail{i1}"] = trail
                    MainScreenManager.get_screen(f"SavedTrailzScreen{i}").ids.MainLayout.ids[f"trail{i1}"].name = saved_trails[i1]["name"]
                    MainScreenManager.get_screen(f"SavedTrailzScreen{i}").ids.MainLayout.ids[f"trail{i1}"].discription = saved_trails[i1]["discription"]
                    MainScreenManager.get_screen(f"SavedTrailzScreen{i}").ids.MainLayout.add_widget(trail)
            print(MainScreenManager.get_screen(f"SavedTrailzScreen{0}").ids.MainLayout.ids.trail0.name)
            ForwardBtn = Button(text="->",on_press=lambda x:self.saved_trails_forward_backward("f",i,((len(saved_trails) // trails_on_screen) + 1)))
            MainScreenManager.get_screen(f"SavedTrailzScreen{i}").ids.MainLayout.ids["NextButton"] = ForwardBtn
            MainScreenManager.get_screen(f"SavedTrailzScreen{i}").ids.MainLayout.add_widget(ForwardBtn)
            PrivBtn = Button(text="<-",on_press=lambda x:self.saved_trails_forward_backward("b",i,((len(saved_trails) // trails_on_screen) + 1)))
            MainScreenManager.get_screen(f"SavedTrailzScreen{i}").ids.MainLayout.ids["PrivButton"] = PrivBtn
            MainScreenManager.get_screen(f"SavedTrailzScreen{i}").ids.MainLayout.add_widget(PrivBtn)
        
    def switch_toSTR(self, screenSTR : str) -> None:
        MainScreenManager.current = screenSTR

    @mainthread   
    def on_location(self, **kwargs) -> None:
        self._GPSJsonDict['GPSData'][int(time.time()) % 2592000] = kwargs
        self.gps_location = '\n'.join(['{}={}'.format(k, v) for k, v in kwargs.items()])   
    
    def request_android_permissions(self):
        from android.permissions import request_permissions, Permission,check_permission
        PermissionList = [Permission.ACCESS_COARSE_LOCATION,Permission.ACCESS_FINE_LOCATION,Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE]
        def callback(permissions, results):
            if all([res for res in results]):
                print("callback. All permissions granted.")
            else:
                print("callback. Some permissions refused.")
        if not all(check_permission(permission) for permission in PermissionList): 
            request_permissions(PermissionList, callback)

    def build(self):
        global MainScreenManager
        print(MainScreenManager.screen_names)
        MainScreenManager.add_widget(LoginSignUpScreen(name="LoginSignUpScreen"))
        MainScreenManager.add_widget(LoginScreen(name="LoginScreen"))
        MainScreenManager.add_widget(SignUpScreen(name="SignUpScreen"))
        MainScreenManager.add_widget(MenuScreen(name='MenuScreen'))
        MainScreenManager.add_widget(GpsInfoScreen(name='GpsInfoScreen'))
        self.creat_own_saved_trails_screen()
        MainScreenManager.add_widget(GpsStartRecordingScreen(name='GpsStartRecordingScreen'))
        MainScreenManager.add_widget(GpsStopRecordingScreen(name='GpsStopRecordingScreen'))
        MainScreenManager.add_widget(TestScreen(name='TestScreen'))
        self._config = MainFileManager.load_config()
        if self._config == False:
            self.switch_toSTR("LoginSignUpScreen")
        if self._config != False:
            self.switch_toSTR('MenuScreen')
        
        if platform == "android":
            try:
                gps.configure(on_location=self.on_location)
            except NotImplementedError:
                import traceback
                traceback.print_exc()
            self.request_android_permissions()
        MainFileManager.MakeDirs()
        print(MainScreenManager.get_screen("SignUpScreen").ids)
        return MainScreenManager
    
    
    @staticmethod
    def start_gps():
        gps.start(0,1)
        
    @staticmethod
    def stop_gps():
        gps.stop()
    
    def open_gps_recording(self) -> None:
        if platform == "ios" or platform == "android":
            MainScreenManager.current = 'GpsStartRecordingScreen'
        else:
            #не открывается и может выводить ошибку
            pass 
        
    def Save_GPS_to_json(self) -> None:
        if MainScreenManager.get_screen('GpsInfoScreen').ids.GPSNameInput.text != "" and MainScreenManager.get_screen('GpsInfoScreen').ids.GPSDescriptionInput.text != "" and MainScreenManager.get_screen('GpsInfoScreen').ids.GPSMinDistanceInput.text != "":
            self._GPSJsonDict['name'] = MainScreenManager.get_screen('GpsInfoScreen').ids.GPSNameInput.text
            self._GPSJsonDict['discription'] = MainScreenManager.get_screen('GpsInfoScreen').ids.GPSDescriptionInput.text
            self._GPSJsonDict['MinDistance'] = MainScreenManager.get_screen('GpsInfoScreen').ids.GPSMinDistanceInput.text
            MainFileManager.save_trail(FileName=self._GPSJsonDict['name'], JsonDict=self._GPSJsonDict)
            MainScreenManager.get_screen('TestScreen').ids.TestLabel.text = str(self._GPSJsonDict)
            MainScreenManager.current = 'TestScreen'
    @property
    def MinDistanceSetting(self) -> int:
        return self._MinDistancePar
    
    @property
    def GPSJsonDict(self) -> dict:
        return self._GPSJsonDict
    
    def Pass(self):
        pass
    
if __name__ == '__main__':
    Trailz().run()
    
