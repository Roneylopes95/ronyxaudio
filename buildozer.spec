[app]
title = PC Ronyx Download Audio
package.name = ronyxaudio
package.domain = com.pcronyx
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy,yt-dlp,certifi,openssl,requests,urllib3,idna,pyjnius,android
orientation = portrait
fullscreen = 0
icon.filename = %(source.dir)s/logo.png
presplash.filename = %(source.dir)s/logo.png
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,READ_MEDIA_AUDIO
android.api = 33
android.minapi = 24
android.archs = arm64-v8a
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 0
