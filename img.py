import os
import shutil
import sys
import time

# --- فحص مكتبة colorama ---
try:
    from colorama import init, Fore, Style
    colorama_available = True
except ImportError:
    colorama_available = False

# تهيئة colorama إذا كانت متوفرة
if colorama_available:
    init(autoreset=True)

def print_animated_banner():
    banner_lines = [
        "                     ______                            ___     ",
        "                    (______)                          / __)    ",
        "                     _     _ ____ ____  ____  _____ _| |__     ",
        "                    | |   | / ___)    \\|  _ \\| ___ (_   __)    ",
        "                    | |__/ / |   | | | | | | | ____| | |       ",
        "                    |_____/|_|   |_|_|_|_| |_|_____) |_|       ",
        "                                                                "
    ]
    
    if colorama_available:
        colors = [Fore.CYAN, Fore.BLUE, Fore.CYAN, Fore.BLUE, Fore.CYAN, Fore.BLUE, Fore.CYAN]
        
        for line, color in zip(banner_lines, colors):
            for char in line:
                sys.stdout.write(color + Style.BRIGHT + char)
                sys.stdout.flush()
                time.sleep(0.005)
            sys.stdout.write("\n")
            time.sleep(0.1)
    else:
        # بدون colorama، طباعة البنر بدون ألوان ولكن مع تأثير الحركة
        for line in banner_lines:
            for char in line:
                sys.stdout.write(char)
                sys.stdout.flush()
                time.sleep(0.005)
            sys.stdout.write("\n")
            time.sleep(0.1)

# طباعة البنر المتحرك
print_animated_banner()

if colorama_available:
    print(Fore.YELLOW + Style.BRIGHT + "🔧 سكربت إنشاء نسخ الصور لـ Kali Linux")
    print(Fore.GREEN + "📁 هذا السكربت ينشئ نسخاً من الصورة بأسماء مختلفة مطلوبة لتخصيص Kali\n")
else:
    print("🔧 سكربت إنشاء نسخ الصور لـ Kali Linux")
    print("📁 هذا السكربت ينشئ نسخاً من الصورة بأسماء مختلفة مطلوبة لتخصيص Kali\n")

# قائمة الأسماء التي تريد إنشاء نسخ الصور بها
images = [
    "grub-16x9.png",
    "grub-4x3.png",
    "desktop-grub.png",
    "desktop-background.png",
    "default.png",
    "kali-tiles-16x9.jpg",
    "login-blurred",
    "login-background.svg",
    "login.svg"
]

# التحقق من وجود وسيط في سطر الأوامر
if len(sys.argv) < 2:
    if colorama_available:
        print(Fore.RED + "❌ يجب تحديد اسم الصورة كوسيط في سطر الأوامر")
        print(Fore.CYAN + "📌 مثال: python3 img.py my-image.png")
    else:
        print("❌ يجب تحديد اسم الصورة كوسيط في سطر الأوامر")
        print("📌 مثال: python3 img.py my-image.png")
    sys.exit(1)

# الحصول على اسم الصورة من الوسيط الأول
original_image_name = sys.argv[1]

# مسار المجلد الحالي (سيتم استخدامه افتراضياً)
folder_path = os.getcwd()

# إذا تم تحديد مسار آخر كوسيط ثاني
if len(sys.argv) > 2:
    folder_path = sys.argv[2]

# تحديد المسار الكامل للصورة الأصلية
original_image_path = os.path.join(folder_path, original_image_name)

# تحقق من وجود الصورة الأصلية
if os.path.exists(original_image_path):
    if colorama_available:
        print(Fore.GREEN + f"✅ جاري إنشاء نسخ من الصورة: {original_image_name}")
    else:
        print(f"✅ جاري إنشاء نسخ من الصورة: {original_image_name}")
    
    # إنشاء نسخ الصور بالأسماء المحددة
    for new_name in images:
        new_image_path = os.path.join(folder_path, new_name)
        
        # نسخ الصورة الأصلية إلى الاسم الجديد
        shutil.copy2(original_image_path, new_image_path)
        
        if colorama_available:
            print(Fore.GREEN + f"✅ تم إنشاء النسخة: {new_name}")
        else:
            print(f"✅ تم إنشاء النسخة: {new_name}")
        
    if colorama_available:
        print(Fore.MAGENTA + "\n🎉 تم إنشاء جميع النسخ بنجاح!")
        print(Fore.CYAN + "📝 الآن يمكنك استخدام kali-grub-background.py لتثبيت الصور")
    else:
        print("\n🎉 تم إنشاء جميع النسخ بنجاح!")
        print("📝 الآن يمكنك استخدام kali-grub-background.py لتثبيت الصور")
else:
    if colorama_available:
        print(Fore.RED + f"❌ الصورة الأصلية {original_image_name} غير موجودة في المسار: {folder_path}")
        print(Fore.YELLOW + "📌 تأكد من كتابة اسم الصورة بشكل صحيح ومن وجودها في المجلد")
    else:
        print(f"❌ الصورة الأصلية {original_image_name} غير موجودة في المسار: {folder_path}")
        print("📌 تأكد من كتابة اسم الصورة بشكل صحيح ومن وجودها في المجلد")
