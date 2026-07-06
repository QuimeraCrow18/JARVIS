[app]
title = Josamick Core AI
package.name = josamick
package.domain = org.josamick
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 2.0.0
requirements = python3, kivy, cryptography, requests, sqlite3, numpy
orientation = portrait
osx.python_version = 3
osx.kivy_version = 2.1.0
fullscreen = 0

android.permissions = INTERNET, ACCESS_WIFI_STATE, CHANGE_WIFI_STATE, ACCESS_NETWORK_STATE, CAMERA
android.api = 31
android.minapi = 21
android.sdk = 34
android.ndk = 25b
android.gradle_dependencies = 'androidx.core:core:1.9.0'
android.enable_androidx = True

ios.codesign.allowed = False

[buildozer]
log_level = 2
warn_on_root = 1
