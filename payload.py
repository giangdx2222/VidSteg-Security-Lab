import ctypes
import subprocess
import time

def demo_attack():
    # 1. Hiện thông báo "Xâm chiếm"
    ctypes.windll.user32.MessageBoxW(0, "Máy tính đã bị xâm chiếm!", "Cảnh báo bảo mật - Trường Giang", 0x30 | 0x0)
    
    # 2. Bật máy tính (Calculator)
    subprocess.Popen('calc.exe')

if __name__ == "__main__":
    demo_attack()