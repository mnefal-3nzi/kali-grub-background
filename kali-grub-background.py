#!/usr/bin/env python3

import os
import shutil
import subprocess
import time
import sys

# --- فحص مكتبة colorama ---
try:
    from colorama import init, Fore, Style
except ImportError:
    print("❌ مكتبة 'colorama' غير مثبتة!")
    print("👉 لتثبيتها، نفذ الأمر التالي:\n")
    print("    sudo pip3 install colorama\n")
    exit(1)

# --- فحص وجود أوامر مهمة ---
def check_command(cmd):
    return shutil.which(cmd) is not None

needed_tools = {
    "xdg-open": "sudo apt install xdg-utils",
    "gsettings": "sudo apt install dconf-cli",
    "update-grub": "sudo apt install grub2-common",
    "dconf": "sudo apt install dconf-cli",
}

for tool, install_cmd in needed_tools.items():
    if not check_command(tool):
        print(f"❌ الأداة '{tool}' غير موجودة على النظام.")
        print(f"👉 لتثبيتها، نفذ الأمر التالي:\n    {install_cmd}\n")
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

print_animated_banner()

print(Fore.YELLOW + Style.BRIGHT + "🔧 سكربت تعديل صور Kali - Python Version")
print(Fore.GREEN + "📁 تأكد من أن الصور موجودة في نفس مجلد السكربت.\n")

files = {
    "grub-16x9.png": "/boot/grub/themes/kali/grub-16x9.png",
    "grub-4x3.png": "/boot/grub/themes/kali/grub-4x3.png",
    "desktop-grub.png": "/usr/share/images/desktop-base/desktop-grub.png",
    "desktop-background": "/usr/share/images/desktop-base/desktop-background",
    "default": "/usr/share/images/desktop-base/default",
    "kali-tiles-16x9.jpg": "/usr/share/backgrounds/kali/kali-tiles-16x9.jpg",
    "login-background.svg": "/usr/share/images/desktop-base",
    "login-background": "/usr/share/backgrounds/kali",
    "login.svg": "/usr/share/backgrounds/kali"
}

print(Fore.CYAN + "📷 الصور المستهدفة:")
for img_name in files.keys():
    print(Fore.CYAN + f"  - {img_name}")

if os.geteuid() != 0:
    print(Fore.RED + "❌ يجب تشغيل السكربت باستخدام sudo أو كـ root.")
    exit(1)

script_dir = os.path.dirname(os.path.realpath(__file__))

show_images = input(Fore.CYAN + "\n❓ هل تريد عرض الصور الآن؟ (y/n): ").strip().lower()

if show_images == 'y':
    print(Fore.MAGENTA + "\n🖼️ عرض الصور للمعاينة...\n")
    for src_name in files:
        src_path = os.path.join(script_dir, src_name)
        if os.path.isfile(src_path):
            print(Fore.BLUE + f"📷 فتح: {src_name}")
            subprocess.Popen(["xdg-open", src_path])
            time.sleep(1.5)
        else:
            print(Fore.RED + f"⚠️ لم يتم العثور على: {src_name}")
else:
    print(Fore.YELLOW + "⏭️ تخطي عرض الصور.")

confirm = input(Fore.CYAN + "\n❓ هل تريد نسخ جميع هذه الصور الآن؟ (y/n): ").strip().lower()
if confirm != 'y':
    print(Fore.RED + "⏹️ تم الإلغاء بناءً على طلبك.")
    exit(0)

print(Fore.GREEN + "\n🔄 جاري نسخ الصور...")

for src_name, dest_path in files.items():
    src_path = os.path.join(script_dir, src_name)
    if not os.path.isfile(src_path):
        print(Fore.YELLOW + f"⏭️ تخطي {src_name} (غير موجود)")
        continue

    try:
        if os.path.exists(dest_path) and not os.path.exists(dest_path + ".bak"):
            shutil.copy2(dest_path, dest_path + ".bak")
            print(Fore.BLUE + f"🗃️ نسخة احتياطية محفوظة: {dest_path}.bak")

        shutil.copy2(src_path, dest_path)
        print(Fore.GREEN + f"✅ تم نسخ {src_name} إلى {dest_path}")
    except Exception as e:
        print(Fore.RED + f"❌ خطأ أثناء نسخ {src_name}: {e}")

print(Fore.MAGENTA + "\n🎨 تغيير خلفية سطح المكتب...")

user = os.getenv("SUDO_USER")
if user:
    try:
        uid = subprocess.check_output(["id", "-u", user]).decode().strip()
        dbus_path = f"/run/user/{uid}/bus"
        background_uri = "file:///usr/share/backgrounds/kali/kali-tiles-16x9.jpg"
        env = os.environ.copy()
        env["DBUS_SESSION_BUS_ADDRESS"] = f"unix:path={dbus_path}"
        subprocess.run(
            ["sudo", "-u", user, "gsettings", "set", "org.gnome.desktop.background", "picture-uri", background_uri],
            check=True, env=env
        )
        print(Fore.GREEN + "✅ تم تعيين الخلفية الجديدة.")
    except Exception as e:
        print(Fore.RED + f"⚠️ تعذر تعيين الخلفية: {e}")
else:
    print(Fore.YELLOW + "⚠️ لم يتم تحديد المستخدم لتحديث الخلفية.")

print(Fore.MAGENTA + "\n⚙️ تحديث grub و GDM...")
subprocess.run(["update-grub"], check=False)
subprocess.run(["dconf", "update"], check=False)

print(Fore.GREEN + "\n✅ كل شيء جاهز! أعد تشغيل النظام لرؤية التغييرات.\n")

