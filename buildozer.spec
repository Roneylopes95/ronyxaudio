[app]
android.accept_sdk_license = True
android.build_tools_version = 33.0.2
android.ndk = 25b
title = Ronyx Audio
package.name = ronyxaudio
package.domain = org.ronyxaudio
source.include_exts = py,png,jpg,kv,atlas
source.dir = .
version = 1.0
requirements = python3,https://github.com/kivy/kivy/archive/master.zip,yt-dlp,certifi,openssl,requests,urllib3,charset-normalizer,idna
orientation = portrait
fullscreen = 0
android.permissions = INTERNET
android.api = 33
android.minapi = 24
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 0
