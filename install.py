r"""
install.py — Chạy script này 1 lần để cài đặt Native Messaging Host.
Yêu cầu: Python 3.x, chạy với quyền User thường (không cần Admin).

Cách dùng:
  cd F:\Projects\Antigravity\Scrape-Voz
  python install.py --extension-id EXTENSION_ID_CUA_BAN

Extension ID lấy từ: chrome://extensions → bật Developer Mode → xem ID bên dưới tên extension.
"""

import os
import sys
import json
import argparse
import platform
import shutil

SCRAPER_DIR = os.path.dirname(os.path.abspath(__file__))
HOST_NAME   = "com.antigravity.voz_scraper"
HOST_SCRIPT = os.path.join(SCRAPER_DIR, "voz_native_host.py")
MANIFEST_FILE = os.path.join(SCRAPER_DIR, f"{HOST_NAME}.json")


def get_python_exe():
    """Trả về đường dẫn đầy đủ đến python.exe đang chạy."""
    return sys.executable


def build_manifest(extension_id: str, python_exe: str) -> dict:
    # Chrome chạy native host bằng cách gọi trực tiếp file .py nếu có shebang
    # trên Windows cần wrap bằng cmd /c python script.py
    if platform.system() == 'Windows':
        # Tạo wrapper .bat để Chrome có thể gọi mà không cần biết Python path
        bat_path = os.path.join(SCRAPER_DIR, "voz_native_host.bat")
        with open(bat_path, 'w') as f:
            f.write(f'@echo off\n"{python_exe}" "{HOST_SCRIPT}"\n')
        host_path = bat_path
        print(f"[+] Tạo wrapper: {bat_path}")
    else:
        host_path = HOST_SCRIPT
        os.chmod(HOST_SCRIPT, 0o755)

    return {
        "name": HOST_NAME,
        "description": "Native host for VOZ Scraper Chrome Extension",
        "path": host_path,
        "type": "stdio",
        "allowed_origins": [
            f"chrome-extension://{extension_id}/"
        ]
    }


def install_windows(manifest: dict):
    """Ghi manifest vào AppData và đăng ký registry key."""
    import winreg

    # Lưu manifest JSON
    appdata = os.environ.get('LOCALAPPDATA', os.path.expanduser('~'))
    manifest_dir = os.path.join(appdata, 'VOZScraper', 'NativeMessaging')
    os.makedirs(manifest_dir, exist_ok=True)
    manifest_path = os.path.join(manifest_dir, f"{HOST_NAME}.json")

    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print(f"[+] Manifest saved: {manifest_path}")

    # Chrome registry key
    reg_key_path = rf"Software\Google\Chrome\NativeMessagingHosts\{HOST_NAME}"
    try:
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, reg_key_path) as key:
            winreg.SetValueEx(key, '', 0, winreg.REG_SZ, manifest_path)
        print(f"[+] Chrome registry key đã đăng ký.")
    except Exception as e:
        print(f"[!] Lỗi đăng ký Chrome registry: {e}")

    # Opera cũng dùng Chromium registry key — thêm cả key này
    opera_key_path = rf"Software\Opera Software\Opera Stable\NativeMessagingHosts\{HOST_NAME}"
    try:
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, opera_key_path) as key:
            winreg.SetValueEx(key, '', 0, winreg.REG_SZ, manifest_path)
        print(f"[+] Opera registry key đã đăng ký.")
    except Exception as e:
        print(f"[!] Lỗi đăng ký Opera registry (bỏ qua nếu không dùng Opera): {e}")

    # Chromium-based browsers chung (Edge, Brave, etc.)
    chromium_key = rf"Software\Chromium\NativeMessagingHosts\{HOST_NAME}"
    try:
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, chromium_key) as key:
            winreg.SetValueEx(key, '', 0, winreg.REG_SZ, manifest_path)
        print(f"[+] Chromium generic registry key đã đăng ký.")
    except Exception as e:
        pass  # Không sao nếu key này không tồn tại


def install_macos(manifest: dict):
    manifest_dir = os.path.expanduser(
        f'~/Library/Application Support/Google/Chrome/NativeMessagingHosts'
    )
    os.makedirs(manifest_dir, exist_ok=True)
    path = os.path.join(manifest_dir, f"{HOST_NAME}.json")
    with open(path, 'w') as f:
        json.dump(manifest, f, indent=2)
    print(f"[+] Manifest saved: {path}")


def install_linux(manifest: dict):
    manifest_dir = os.path.expanduser(
        f'~/.config/google-chrome/NativeMessagingHosts'
    )
    os.makedirs(manifest_dir, exist_ok=True)
    path = os.path.join(manifest_dir, f"{HOST_NAME}.json")
    with open(path, 'w') as f:
        json.dump(manifest, f, indent=2)
    print(f"[+] Manifest saved: {path}")


def main():
    parser = argparse.ArgumentParser(description='Cài đặt VOZ Scraper Native Messaging Host')
    parser.add_argument('--extension-id', required=True,
                        help='Extension ID từ chrome://extensions (32 ký tự)')
    args = parser.parse_args()

    ext_id = args.extension_id.strip()
    if len(ext_id) != 32 or not ext_id.isalpha():
        print(f"[!] Extension ID không hợp lệ: '{ext_id}'")
        print("    Lấy từ chrome://extensions hoặc opera://extensions → bật Developer Mode → copy ID (trên Opera nhấn vào 'Details' / 'Chi tiết' để xem ID)")
        sys.exit(1)

    python_exe = get_python_exe()
    print(f"[i] Python: {python_exe}")
    print(f"[i] Script: {HOST_SCRIPT}")
    print(f"[i] Extension ID: {ext_id}")

    manifest = build_manifest(ext_id, python_exe)

    # Cập nhật manifest gốc trong thư mục extension (để tham khảo)
    with open(MANIFEST_FILE, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    plat = platform.system()
    if plat == 'Windows':
        install_windows(manifest)
    elif plat == 'Darwin':
        install_macos(manifest)
    else:
        install_linux(manifest)

    print("\n✅ Cài đặt xong!")
    print("   → Load extension vào Chrome/Opera → bật Developer Mode → Load unpacked")
    print("   → Mở trang voz.vn thread bất kỳ → click icon extension → Scrape!")


if __name__ == '__main__':
    main()
