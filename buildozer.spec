[app]

# اسم التطبيق
title = العقارات

# اسم الحزمة (package)
package.name = realestate
package.domain = com

# الإصدار
version = 1.0

# متطلبات بايثون (تم تحديد إصدار بايثون المستقر وإزالة android)
requirements = python3==3.10.12,kivy,plyer,requests

# اتجاه الشاشة
orientation = portrait

# ملء الشاشة
fullscreen = 0

# الصلاحيات
android.permissions = READ_CONTACTS,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,INTERNET

# إصدار SDK و NDK المستقرين جداً
android.api = 31
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True

# ملف المصدر
source.dir = .

# إعدادات Buildozer
[buildozer]
log_level = 2
warn_on_root = 1
