#!/usr/bin/env python3

import os
import shutil
import subprocess
import time
import sys

# --- فحص مكتبة colorama ---
try:
    from colorama import init, Fore, Style
    colorama_available = True
except ImportError:
    print("❌ مكتبة 'colorama' غير مثبتة!")
    print("👉 لتثبيتها، نفذ الأمر التالي:\n")
    print("    sudo pip3 install colorama\n")
    colorama_available = False
    exit(1)

# تهيئة colorama بعد التأكد من وجودها
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
    
    colors = [Fore.CYAN, Fore.BLUE, Fore.CYAN, Fore.BLUE, Fore.CYAN, Fore.BLUE, Fore.CYAN]
    
    for line, color in zip(banner_lines, colors):
        for char in line:
            sys.stdout.write(color + Style.BRIGHT + char)
            sys.stdout.flush()
            time.sleep(0.005)
        sys.stdout.write("\n")
        time.sleep(0.1)

def check_command(cmd):
    """فحص وجود أمر في النظام"""
    return shutil.which(cmd) is not None

def check_required_tools():
    """فحص الأدوات المطلوبة"""
    needed_tools = {
        "update-grub": "sudo apt install grub2-common",
        "dconf": "sudo apt install dconf-cli",
    }
    
    missing_tools = []
    
    for tool, install_cmd in needed_tools.items():
        if not check_command(tool):
            missing_tools.append((tool, install_cmd))
    
    if missing_tools:
        print(Fore.RED + "❌ الأدوات التالية غير موجودة على النظام:")
        for tool, install_cmd in missing_tools:
            print(Fore.RED + f"   - {tool}")
            print(Fore.YELLOW + f"     للتثبيت: {install_cmd}")
        return False
    
    return True

def create_image_copies():
    """الوظيفة الأولى: إنشاء نسخ من الصورة بأسماء مختلفة"""
    print(Fore.YELLOW + Style.BRIGHT + "\n🔧 الوظيفة 1: إنشاء نسخ الصور")
    print(Fore.GREEN + "📁 هذه الوظيفة تنشئ نسخاً من الصورة بأسماء مختلفة مطلوبة لتخصيص Kali\n")
    
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
    
    # طلب اسم الصورة من المستخدم
    original_image_name = input(Fore.CYAN + "📷 أدخل اسم الصورة الأصلية (مثال: my-image.jpg): ").strip()
    
    if not original_image_name:
        print(Fore.RED + "❌ يجب إدخال اسم الصورة")
        return False
    
    # مسار المجلد الحالي
    folder_path = os.getcwd()
    
    # سؤال عن المسار إذا أراد المستخدم تغييره
    change_path = input(Fore.CYAN + f"📂 المسار الحالي: {folder_path} - هل تريد تغييره؟ (y/n): ").strip().lower()
    if change_path == 'y':
        new_path = input(Fore.CYAN + "🔧 أدخل المسار الجديد: ").strip()
        if os.path.exists(new_path):
            folder_path = new_path
        else:
            print(Fore.RED + f"❌ المسار {new_path} غير موجود")
            return False
    
    # تحديد المسار الكامل للصورة الأصلية
    original_image_path = os.path.join(folder_path, original_image_name)
    
    # تحقق من وجود الصورة الأصلية
    if not os.path.exists(original_image_path):
        print(Fore.RED + f"❌ الصورة الأصلية {original_image_name} غير موجودة في المسار: {folder_path}")
        print(Fore.YELLOW + "📌 تأكد من كتابة اسم الصورة بشكل صحيح ومن وجودها في المجلد")
        return False
    
    print(Fore.GREEN + f"✅ جاري إنشاء نسخ من الصورة: {original_image_name}")
    
    # إنشاء نسخ الصور بالأسماء المحددة
    success_count = 0
    for new_name in images:
        new_image_path = os.path.join(folder_path, new_name)
        
        try:
            # نسخ الصورة الأصلية إلى الاسم الجديد
            shutil.copy2(original_image_path, new_image_path)
            print(Fore.GREEN + f"✅ تم إنشاء النسخة: {new_name}")
            success_count += 1
        except Exception as e:
            print(Fore.RED + f"❌ خطأ في إنشاء {new_name}: {e}")
    
    print(Fore.MAGENTA + f"\n🎉 تم إنشاء {success_count} من أصل {len(images)} نسخة بنجاح!")
    if success_count > 0:
        print(Fore.CYAN + "📝 الآن يمكنك استخدام الوظيفة الثانية (تثبيت الصور) لتطبيق التغييرات")
    return True

def install_images():
    """الوظيفة الثانية: تثبيت الصور في النظام"""
    print(Fore.YELLOW + Style.BRIGHT + "\n🔧 الوظيفة 2: تثبيت الصور في النظام")
    print(Fore.GREEN + "📁 تأكد من أن الصور موجودة في نفس مجلد السكربت.\n")
    
    # فحص الأدوات المطلوبة
    if not check_required_tools():
        return False
    
    # فحص صلاحيات root
    if os.geteuid() != 0:
        print(Fore.RED + "❌ يجب تشغيل هذه الوظيفة باستخدام sudo أو كـ root.")
        print(Fore.CYAN + "📌 أعد تشغيل السكربت باستخدام: sudo python3 kali-script.py")
        return False
    
    files = {
        "grub-16x9.png": "/boot/grub/themes/kali/grub-16x9.png",
        "grub-4x3.png": "/boot/grub/themes/kali/grub-4x3.png",
        "desktop-grub.png": "/usr/share/images/desktop-base/desktop-grub.png",
        "desktop-background.png": "/usr/share/images/desktop-base/desktop-background",
        "default.png": "/usr/share/images/desktop-base/default",
        "kali-tiles-16x9.jpg": "/usr/share/backgrounds/kali/kali-tiles-16x9.jpg",
        "login-blurred": "/usr/share/backgrounds/kali/login-blurred",
        "login-background.svg": "/usr/share/images/desktop-base/login-background.svg",
        "login.svg": "/usr/share/backgrounds/kali/login.svg"
    }
    
    print(Fore.CYAN + "📷 الصور المستهدفة:")
    for img_name in files.keys():
        print(Fore.CYAN + f"  - {img_name}")
    
    script_dir = os.path.dirname(os.path.realpath(__file__))
    
    # التحقق من وجود الصور المطلوبة
    missing_images = []
    available_images = []
    
    for src_name in files:
        src_path = os.path.join(script_dir, src_name)
        if os.path.isfile(src_path):
            available_images.append(src_name)
        else:
            missing_images.append(src_name)
    
    if missing_images:
        print(Fore.YELLOW + f"⚠️  {len(missing_images)} صورة غير موجودة في مجلد السكربت:")
        for img in missing_images:
            print(Fore.YELLOW + f"   - {img}")
        
        if not available_images:
            print(Fore.RED + "❌ لا توجد أي صور متاحة للتثبيت!")
            print(Fore.YELLOW + "📌 استخدم الوظيفة الأولى (إنشاء نسخ الصور) لإنشاء هذه الصور أولاً")
            return False
        
        continue_anyway = input(Fore.CYAN + f"\n❓ هل تريد المتابعة مع {len(available_images)} صورة متاحة فقط؟ (y/n): ").strip().lower()
        if continue_anyway != 'y':
            print(Fore.RED + "⏹️ تم الإلغاء بناءً على طلبك.")
            return False
    
    show_images = input(Fore.CYAN + "\n❓ هل تريد عرض الصور الآن؟ (y/n): ").strip().lower()
    
    if show_images == 'y':
        print(Fore.MAGENTA + "\n🖼️ عرض الصور للمعاينة...\n")
        # محاولة استخدام xdg-open إذا كان متاحاً
        if check_command("xdg-open"):
            for src_name in available_images:
                src_path = os.path.join(script_dir, src_name)
                print(Fore.BLUE + f"📷 فتح: {src_name}")
                try:
                    subprocess.Popen(["xdg-open", src_path])
                    time.sleep(1.5)
                except:
                    print(Fore.YELLOW + f"⚠️ تعذر فتح: {src_name}")
        else:
            print(Fore.YELLOW + "⚠️ xdg-open غير متوفر، لا يمكن عرض الصور")
    
    print(Fore.RED + "\n⚠️  تحذير: هذا الإجراء سيستبدل الصور الحالية في النظام!")
    confirm = input(Fore.CYAN + "❓ هل أنت متأكد أنك تريد متابعة التثبيت؟ (y/n): ").strip().lower()
    if confirm != 'y':
        print(Fore.RED + "⏹️ تم الإلغاء بناءً على طلبك.")
        return False
    
    print(Fore.GREEN + "\n🔄 جاري نسخ الصور...")
    
    success_count = 0
    for src_name in available_images:
        src_path = os.path.join(script_dir, src_name)
        dest_path = files[src_name]
        
        try:
            # إنشاء نسخة احتياطية إذا لم تكن موجودة
            if os.path.exists(dest_path) and not os.path.exists(dest_path + ".bak"):
                shutil.copy2(dest_path, dest_path + ".bak")
                print(Fore.BLUE + f"🗃️ نسخة احتياطية محفوظة: {dest_path}.bak")
            
            # نسخ الملف الجديد
            shutil.copy2(src_path, dest_path)
            print(Fore.GREEN + f"✅ تم نسخ {src_name} إلى {dest_path}")
            success_count += 1
        except Exception as e:
            print(Fore.RED + f"❌ خطأ أثناء نسخ {src_name}: {e}")
    
    if success_count > 0:
        print(Fore.MAGENTA + "\n🎨 تغيير خلفية سطح المكتب...")
        
        user = os.getenv("SUDO_USER")
        if user:
            try:
                uid = subprocess.check_output(["id", "-u", user]).decode().strip()
                dbus_path = f"/run/user/{uid}/bus"
                background_uri = "file:///usr/share/backgrounds/kali/kali-tiles-16x9.jpg"
                env = os.environ.copy()
                env["DBUS_SESSION_BUS_ADDRESS"] = f"unix:path={dbus_path}"
                
                # محاولة استخدام gsettings إذا كان متاحاً
                if check_command("gsettings"):
                    subprocess.run(
                        ["sudo", "-u", user, "gsettings", "set", "org.gnome.desktop.background", "picture-uri", background_uri],
                        check=True, env=env
                    )
                    print(Fore.GREEN + "✅ تم تعيين الخلفية الجديدة.")
                else:
                    print(Fore.YELLOW + "⚠️ gsettings غير متوفر، سيتم تحديث الخلفية بعد إعادة التشغيل")
            except Exception as e:
                print(Fore.YELLOW + f"⚠️ تعذر تعيين الخلفية: {e}")
        else:
            print(Fore.YELLOW + "⚠️ لم يتم تحديد المستخدم لتحديث الخلفية.")
        
        print(Fore.MAGENTA + "\n⚙️ تحديث grub و GDM...")
        subprocess.run(["update-grub"], check=False)
        subprocess.run(["dconf", "update"], check=False)
        
        print(Fore.GREEN + f"\n✅ تم تثبيت {success_count} صورة بنجاح!")
        print(Fore.CYAN + "🔄 أعد تشغيل النظام لرؤية جميع التغييرات.\n")
    else:
        print(Fore.RED + "❌ لم يتم تثبيت أي صورة!")
    
    return success_count > 0

def show_help():
    """عرض رسالة المساعدة"""
    print(Fore.CYAN + "\n📖 شرح الوظائف:")
    print(Fore.WHITE + "  1. إنشاء نسخ الصور")
    print(Fore.WHITE + "     - ينشئ نسخاً من صورتك بأسماء مختلفة مطلوبة لنظام Kali")
    print(Fore.WHITE + "  2. تثبيت الصور في النظام")
    print(Fore.WHITE + "     - ينسخ الصور إلى مواقعها في النظام (يتطلب صلاحيات root)")
    print(Fore.WHITE + "  3. عرض المساعدة")
    print(Fore.WHITE + "     - يعرض هذه الرسالة")
    print(Fore.WHITE + "  4. الخروج")
    print(Fore.WHITE + "     - إنهاء البرنامج\n")
    
    print(Fore.YELLOW + "📌 نصائح الاستخدام:")
    print(Fore.WHITE + "  - أولاً: استخدم الوظيفة 1 لإنشاء نسخ الصور من صورتك")
    print(Fore.WHITE + "  - ثانياً: استخدم الوظيفة 2 لتثبيت الصور (باستخدام sudo)")
    print(Fore.WHITE + "  - أخيراً: أعد تشغيل النظام لرؤية التغييرات")

def main_menu():
    """عرض القائمة الرئيسية"""
    while True:
        print(Fore.CYAN + "\n" + "="*50)
        print(Fore.YELLOW + Style.BRIGHT + "🏠 القائمة الرئيسية")
        print(Fore.CYAN + "="*50)
        print(Fore.WHITE + "1. إنشاء نسخ الصور")
        print(Fore.WHITE + "2. تثبيت الصور في النظام")
        print(Fore.WHITE + "3. عرض المساعدة")
        print(Fore.WHITE + "4. الخروج")
        print(Fore.CYAN + "="*50)
        
        choice = input(Fore.CYAN + "\n🔢 اختر رقم الوظيفة (1-4): ").strip()
        
        if choice == "1":
            create_image_copies()
        elif choice == "2":
            install_images()
        elif choice == "3":
            show_help()
        elif choice == "4":
            print(Fore.GREEN + "👋 تم إنهاء البرنامج. إلى اللقاء!")
            break
        else:
            print(Fore.RED + "❌ اختيار غير صحيح! الرجاء اختيار رقم بين 1 و 4")

def main():
    """الدالة الرئيسية"""
    print_animated_banner()
    
    print(Fore.YELLOW + Style.BRIGHT + "🔧 سكربت تخصيص Kali Linux - النسخة التفاعلية")
    print(Fore.GREEN + "📁 سكربت متكامل لإنشاء وتثبيت صور الخلفية لـ Kali Linux\n")
    
    # إذا كانت هناك وسائط في سطر الأوامر، استخدام الوضع القديم
    if len(sys.argv) > 1:
        print(Fore.YELLOW + "⚠️  هذه النسخة تعمل بشكل تفاعلي")
        print(Fore.CYAN + "📝 تشغيل بدون وسائط للدخول إلى الوضع التفاعلي\n")
    
    # الدخول إلى القائمة الرئيسية
    main_menu()

if __name__ == "__main__":
    main()
