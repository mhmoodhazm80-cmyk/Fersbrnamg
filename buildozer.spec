[app]

# اسم التطبيق
title = العقارات

# اسم الحزمة (package)
package.name = realestate
package.domain = com

# الإصدار
version = 1.0

# متطلبات بايثون
requirements = python3,kivy,android,plyer,requests

# اتجاه الشاشة
orientation = portrait

# ملء الشاشة
fullscreen = 0

# الصلاحيات
android.permissions = READ_CONTACTS,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,INTERNET

# إصدار SDK
android.api = 30
android.minapi = 21

# إصدار NDK (الأهم: يجب أن يكون 28c)
android.ndk = 28c

# إصدار SDK (يُستخدم مع NDK)
android.sdk = 30

# ملف المصدر
source.dir = .

# إعدادات Buildozer
[buildozer]
log_level = 2
warn_on_root = 1