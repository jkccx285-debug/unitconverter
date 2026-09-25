[app]
title = مبدل واحد
package.name = unitconverter
package.domain = org.me

source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

requirements = python3,kivy==2.3.0

orientation = portrait
fullscreen = 0

android.permissions = 
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a

android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1