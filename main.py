from colorama import Fore, Back, Style
import datetime
import kivy
import GpsProcess
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
from kivy.uix.label import Label
if platform == "android":
    from plyer import gps

Builder.load_file(filename='main.kv')

#миксин для классов, работающих с жипиэс
class Wp(Widget):
    pass

class SavedTrail(Wp):
    pass

class PublicTrail(Wp):
    pass


class TrailInfoScreen(Screen):
    pass

class SavedTrailsScreen(Screen):
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
        #добавить поп ап
        #метод у файл менеджера, тк файл должен быть открыт во время загрузки
        MainFileManager.load_own_trail(trail_name, self._config["email"],self._config["password"])    
          
    def creat_own_saved_trails_screen(self):
        MainScreenManager.get_screen('SavedTrailsScreen').ids.MainLayout.clear_widgets()
        saved_trails = MainFileManager.get_own_saved_trails_info()
        MainScreen = MainScreenManager.get_screen('SavedTrailsScreen')
        for i in range(len(saved_trails)):
            trail = SavedTrail()
            MainScreen.ids.MainLayout.ids[f"trail_{i}"] = trail
            MainScreen.ids.MainLayout.ids[f"trail_{i}"].name = saved_trails[i]["name"]
            MainScreen.ids.MainLayout.ids[f"trail_{i}"].description = saved_trails[i]["description"]    
            MainScreen.ids.MainLayout.add_widget(trail)
        
    def create_public_trails_screen(self,page=0):
        sort_type = "default"
        location = " "
        MainScreen = MainScreenManager.get_screen('MenuScreen')
        MainScreen.ids.MainLayout.clear_widgets()
        trail_list = MainServerManager.get_all_trails(sort_type,location,page)
        if page != 0 and trail_list == []:
            page -= 2
        i = 0
        for trail_data in trail_list:
            trail = PublicTrail()
            MainScreen.ids.MainLayout.ids[f"trail_{i}"] = trail
            MainScreen.ids.MainLayout.ids[f"trail_{i}"].trail_name = trail_data[0]
            MainScreen.ids.MainLayout.ids[f"trail_{i}"].username = trail_data[1]
            MainScreen.ids.MainLayout.ids[f"trail_{i}"].distance = str(trail_data[2]) + " km"
            MainScreen.ids.MainLayout.ids[f"trail_{i}"].date = trail_data[3]
            MainScreen.ids.MainLayout.ids[f"trail_{i}"].trail_id = trail_data[6]
            MainScreen.ids.MainLayout.ids[f"trail_{i}"].description = trail_data[7]
            MainScreen.ids.MainLayout.add_widget(trail)
            i+=1
        MainScreen.ids.MainLayout.amount = i + 1
        MainButton = Button(text="загрузить ещё",size_hint_y=None)
        MainButton.bind(on_press=lambda x:self.create_public_trails_screen(page+1))
        MainScreen.ids.MainLayout.add_widget(MainButton)
        
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
        MainScreenManager.add_widget(LoginSignUpScreen(name="LoginSignUpScreen"))
        MainScreenManager.add_widget(LoginScreen(name="LoginScreen"))
        MainScreenManager.add_widget(SignUpScreen(name="SignUpScreen"))
        MainScreenManager.add_widget(TrailInfoScreen(name="TrailInfoScreen"))
        MainScreenManager.add_widget(MenuScreen(name='MenuScreen'))
        MainScreenManager.add_widget(GpsInfoScreen(name='GpsInfoScreen'))
        MainScreenManager.add_widget(SavedTrailsScreen(name='SavedTrailsScreen'))
        self.creat_own_saved_trails_screen()
        self.create_public_trails_screen()
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
            self._GPSJsonDict['description'] = MainScreenManager.get_screen('GpsInfoScreen').ids.GPSDescriptionInput.text
            self._GPSJsonDict['MinDistance'] = MainScreenManager.get_screen('GpsInfoScreen').ids.GPSMinDistanceInput.text
            SecDict = GpsProcess.get_gps_info(self._GPSJsonDict)
            self._GPSJsonDict["avg_speed"] = SecDict["avg_speed"]
            self._GPSJsonDict["distance"] = SecDict["distance"]
            self._GPSJsonDict["date"] = datetime.today().strftime('%Y-%m-%d')
            MainFileManager.save_trail(FileName=self._GPSJsonDict['name'], JsonDict=self._GPSJsonDict)
            MainScreenManager.get_screen('TestScreen').ids.TestLabel.text = str(self._GPSJsonDict)
            self.creat_own_saved_trails_screen()
            MainScreenManager.current = 'TestScreen'
    def open_gps_info_screen(self,name,username,date,distance,description,trail_id):
        
        MainScreen = MainScreenManager.get_screen("TrailInfoScreen")
        MainScreen.trail_name = name
        MainScreen.username = username
        MainScreen.date = date
        MainScreen.distance = distance
        MainScreen.description = description
        MainScreen.trail_id = trail_id
        print(Fore.RED + str(MainScreenManager.screens))
        MainScreenManager.current = "TrailInfoScreen"
        
        
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
    
