#!/usr/bin/env python3
"""
voz_native_host.py — Native Messaging Host Bridge
Nhận JSON từ Chrome extension qua stdin, chạy scrape_voz.py, trả kết quả qua stdout.

Đặt file này ở: F:\Projects\Antigravity\Scrape-Voz\voz_native_host.py
"""

import sys
import json
import struct
import subprocess
import os

# ===================== CẤU HÌNH =====================
SCRAPER_DIR  = r"F:\Projects\Antigravity\Scrape-Voz"
SCRAPER_FILE = "scrape_voz.py"
PYTHON_EXE   = "python"   # Hoặc đường dẫn đầy đủ: r"C:\Python311\python.exe"
# ====================================================


def read_message() -> dict:
    """Đọc message từ Chrome (4-byte length prefix + JSON)."""
    raw_length = sys.stdin.buffer.read(4)
    if not raw_length:
        sys.exit(0)
    length = struct.unpack('<I', raw_length)[0]
    raw_msg = sys.stdin.buffer.read(length)
    return json.loads(raw_msg.decode('utf-8'))


def send_message(data: dict):
    """Gửi response về Chrome."""
    encoded = json.dumps(data).encode('utf-8')
    sys.stdout.buffer.write(struct.pack('<I', len(encoded)))
    sys.stdout.buffer.write(encoded)
    sys.stdout.buffer.flush()


def main():
    msg = read_message()

    url            = msg.get('url', '')
    download_imgs  = msg.get('downloadImages', False)
    show_window    = msg.get('showWindow', False)

    if not url:
        send_message({'success': False, 'error': 'URL rỗng'})
        return

    # Dựng lệnh
    cmd = [PYTHON_EXE, SCRAPER_FILE, '--url', url]
    if download_imgs:
        cmd.append('--download-images')

    # Cờ creationflags để hiện/ẩn cửa sổ CMD trên Windows
    import platform
    if platform.system() == 'Windows':
        import ctypes
        CREATE_NEW_CONSOLE = 0x00000010
        CREATE_NO_WINDOW   = 0x08000000
        flags = CREATE_NEW_CONSOLE if show_window else CREATE_NO_WINDOW
        proc = subprocess.Popen(
            cmd,
            cwd=SCRAPER_DIR,
            creationflags=flags
        )
    else:
        # macOS / Linux fallback
        proc = subprocess.Popen(cmd, cwd=SCRAPER_DIR)

    send_message({
        'success': True,
        'pid': proc.pid,
        'cmd': ' '.join(cmd)
    })


if __name__ == '__main__':
    main()
