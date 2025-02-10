import kivy
from kivy.lang import Builder
from kivy.app import App
from kivy.properties import StringProperty
from kivy.clock import mainthread
from kivy.utils import platform
import time
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from FileWork import FileManager

if platform == "android":
    from plyer import gps
    
    
Builder.load_file(filename='main.kv')

#миксин для классов, работающих с жипиэс
    
    
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


MainFileManager = FileManager()
MainScreenManager = ScreenManager()


class Trailz(App):
    
    gps_location = StringProperty()
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._GPSJsonDict = {'GPSData':{}}
        self._jsonTrailPath = "saved_trails/"
        self._MinDistancePar = 1

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
        MainScreenManager.add_widget(MenuScreen(name='MenuScreen'))
        MainScreenManager.add_widget(GpsInfoScreen(name='GpsInfoScreen'))
        MainScreenManager.add_widget(GpsStartRecordingScreen(name='GpsStartRecordingScreen'))
        MainScreenManager.add_widget(GpsStopRecordingScreen(name='GpsStopRecordingScreen'))
        MainScreenManager.add_widget(TestScreen(name='TestScreen'))
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
    
