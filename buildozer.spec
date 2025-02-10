[app]

title = Trailz
package.name = trailz
package.domain = org.trailz
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,jpeg
version = 0.1
requirements = python3, kivy, android, androidstorage4kivy, https://github.com/HyTurtle/plyer/archive/master.zip
orientation = portrait
osx.python_version = 3
osx.kivy_version = 1.9.1
fullscreen = 0
android.permissions = INTERNET,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAG
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.10.0
ios.codesign.allowed = false
[buildozer]
log_level = 2
warn_on_root = 1