#!/usr/bin/env python3
r"""
voz_native_host.py — Native Messaging Host Bridge
Nhận JSON từ Chrome extension qua stdin, chạy scrape_voz.py, trả kết quả qua stdout.

Đặt file này ở: F:\Projects\Antigravity\Scrape-Voz\voz_native_host.py
"""

import sys
import json
import struct
import subprocess
import os
import hashlib
import tempfile
import platform

# ===================== CẤU HÌNH =====================
SCRAPER_DIR  = r"F:\Projects\Antigravity\Scrape-Voz"
SCRAPER_FILE = "scrape_voz.py"
PYTHON_EXE   = "python"   # Hoặc đường dẫn đầy đủ: r"C:\Python311\python.exe"
# ====================================================


def is_pid_running(pid: int) -> bool:
    """Kiểm tra PID có đang hoạt động trên hệ thống hay không."""
    if pid <= 0:
        return False
    if platform.system() == 'Windows':
        # Dùng Windows API OpenProcess để kiểm tra — không bị treo như os.kill()
        import ctypes
        PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
        handle = ctypes.windll.kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
        if not handle:
            return False
        # Kiểm tra xem process có còn alive hay đã exit
        exit_code = ctypes.c_ulong()
        ctypes.windll.kernel32.GetExitCodeProcess(handle, ctypes.byref(exit_code))
        ctypes.windll.kernel32.CloseHandle(handle)
        STILL_ACTIVE = 259
        return exit_code.value == STILL_ACTIVE
    else:
        # Unix: dùng os.kill signal 0
        import errno
        try:
            os.kill(pid, 0)
            return True
        except OSError as err:
            if err.errno == errno.ESRCH:
                return False
            return True


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

    if not url:
        send_message({'success': False, 'error': 'URL rỗng'})
        return

    # Kiểm tra File Lock (Option B) để ngăn chặn chạy trùng URL
    url_hash = hashlib.md5(url.encode('utf-8')).hexdigest()
    lock_file = os.path.join(tempfile.gettempdir(), f"com.antigravity.voz_scraper_{url_hash}.lock")

    if os.path.exists(lock_file):
        try:
            with open(lock_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                old_pid = data.get('pid')
                if old_pid and is_pid_running(old_pid):
                    send_message({
                        'success': False,
                        'error': f'URL này đang được scrape ở một tiến trình khác (PID: {old_pid}). Vui lòng chờ hoàn thành!'
                    })
                    return
        except Exception:
            pass

    # Thiết lập lệnh chạy và khởi chạy tiến trình
    run_cmd = f'"{PYTHON_EXE}" "{SCRAPER_FILE}" --url "{url}"'
    if download_imgs:
        run_cmd += ' --download-images'

    if platform.system() == 'Windows':
        # Luôn mở cửa sổ CMD mới và giữ lại (/k) khi chạy xong
        cmd = ['cmd.exe', '/k', run_cmd]
        CREATE_NEW_CONSOLE = 0x00000010
        proc = subprocess.Popen(
            cmd,
            cwd=SCRAPER_DIR,
            creationflags=CREATE_NEW_CONSOLE
        )
    else:
        # macOS / Linux fallback (không giữ CMD mở do sự khác biệt môi trường)
        cmd = [PYTHON_EXE, SCRAPER_FILE, '--url', url]
        if download_imgs:
            cmd.append('--download-images')
        proc = subprocess.Popen(cmd, cwd=SCRAPER_DIR)

    # Ghi PID vào file lock
    try:
        with open(lock_file, 'w', encoding='utf-8') as f:
            json.dump({'pid': proc.pid, 'url': url}, f)
    except Exception:
        pass

    send_message({
        'success': True,
        'pid': proc.pid,
        'cmd': ' '.join(cmd) if isinstance(cmd, list) else cmd
    })


if __name__ == '__main__':
    main()
