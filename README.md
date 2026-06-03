# VOZ Scraper — Chrome/Opera/Chromium Extension

[Tiếng Việt](#tiếng-viet) | [English](#english)

---

<a name="tiếng-viet"></a>
# 🇻🇳 Tiếng Việt

**VOZ Scraper** là tiện ích mở rộng giúp bạn tải toàn bộ thread từ diễn đàn **voz.vn** về máy tính chỉ với **1 cú click**. Không cần sao chép URL thủ công, không cần mở CMD tự gõ lệnh.

> [!NOTE]
> Tiện ích này hoạt động thông qua cơ chế **Native Messaging** của Chrome để giao tiếp và gọi script Python (`scrape_voz.py`) ở máy tính của bạn.

---

## 📂 Cấu trúc thư mục

```text
voz-scraper-extension/
├── manifest.json              ← Cấu hình extension (manifest v3)
├── popup.html / popup.js      ← Giao diện & logic popup của extension
├── background.js              ← Service worker điều phối native messaging
├── content.js                 ← Content script (dự phòng nâng cấp)
├── voz_native_host.py         ← ⭐ Script cầu nối (copy vào thư mục scraper)
├── com.antigravity.voz_scraper.json  ← Manifest của Native Host (tự động cấu hình)
├── install.py                 ← Script cài đặt / đăng ký Registry tự động
├── make_icons.py              ← Script sinh icon tự động (sử dụng Pillow)
└── .gitignore                 ← Các file loại trừ khi commit
```

---

## ⚙️ Hướng dẫn cài đặt (Windows / macOS / Linux)

### Bước 1: Sao chép file cầu nối
Copy file `voz_native_host.py` và `install.py` vào thư mục chứa project scraper chính của bạn (nơi có file `scrape_voz.py`). Ví dụ:
```bash
copy voz_native_host.py F:\Projects\Antigravity\Scrape-Voz\
copy install.py         F:\Projects\Antigravity\Scrape-Voz\
```

### Bước 2: Tải Extension lên Browser
1. Mở trang quản lý extension của trình duyệt:
   - Chrome: `chrome://extensions/`
   - Opera: `opera://extensions/`
   - Edge: `edge://extensions/`
2. Kích hoạt **Developer mode** (Chế độ nhà phát triển) ở góc trên bên phải.
3. Click **Load unpacked** (Tải tiện ích đã giải nén) và chọn thư mục `voz-scraper-extension` này.
4. Copy lại **Extension ID** vừa được tạo (chuỗi 32 ký tự ngẫu nhiên, ví dụ: `feijklcbaiaobmgbcihhkgijmmejeefp`).

### Bước 3: Đăng ký Native Messaging Host
Chạy script cài đặt để đăng ký extension ID của bạn với hệ điều hành:
```bash
cd F:\Projects\Antigravity\Scrape-Voz
python install.py --extension-id <EXTENSION_ID_CUA_BAN>
```

> [!IMPORTANT]
> Script `install.py` sẽ tự động:
> - Tạo file wrapper `voz_native_host.bat` để chạy ngầm Python.
> - Đăng ký registry keys tương ứng cho Chrome, Opera và Chromium.
> - Lưu manifest định danh native host vào thư mục AppData cục bộ.

### Bước 4: Tạo Icons (Tuỳ chọn)
Để extension có biểu tượng đẹp mắt trên thanh công cụ:
```bash
pip install Pillow
python make_icons.py
```
*Hoặc đơn giản là copy 2 file hình ảnh PNG bất kỳ đặt tên là `icon16.png` và `icon48.png` bỏ vào thư mục extension.*

---

## 🚀 Hướng dẫn sử dụng

1. Truy cập vào một thread bất kỳ trên diễn đàn **voz.vn** (URL có dạng `/t/ten-thread.123456/`).
2. Click vào biểu tượng **V** màu đỏ của extension trên thanh công cụ.
3. Kiểm tra hiển thị URL (nếu viền **màu xanh** là URL hợp lệ).
4. Lựa chọn cấu hình mong muốn:
   - Tích chọn `--download-images` nếu muốn tải cả hình ảnh trong thread.
   - Tích chọn **Hiện cửa sổ CMD** nếu muốn mở cửa sổ console hiển thị tiến trình scrape thời gian thực.
5. Click **🕷 Scrape thread này** để bắt đầu.

---

## 🛠 Giải quyết lỗi thường gặp

| Hiện tượng | Nguyên nhân | Cách khắc phục |
| :--- | :--- | :--- |
| `Specified native messaging host not found` | Chưa chạy `install.py` hoặc truyền sai Extension ID. | Chạy lại `install.py` với Extension ID chính xác. |
| `Access to the specified native messaging host is forbidden` | Extension ID trong file cấu hình native host không khớp với ID thực tế. | Đăng ký lại bằng cách chạy lại `install.py`. |
| Popup báo "Không phải thread VOZ" | Bạn đang ở trang chủ, chuyên mục, hoặc URL không khớp pattern `/t/...` | Chỉ click scrape khi đang ở trang xem chi tiết bài viết (thread). |
| Script Python không chạy | Trình duyệt không tìm thấy Python hoặc đường dẫn trong file bat sai. | Sửa dòng `PYTHON_EXE` trong `voz_native_host.py` thành đường dẫn tuyệt đối (ví dụ: `C:\Python311\python.exe`). |

---

<a name="english"></a>
# 🇺🇸 English

**VOZ Scraper** is a browser extension that allows you to download and scrape entire threads from **voz.vn** with a **single click**. No more manual URL copying, no more command prompt typing.

> [!NOTE]
> This extension uses Chrome's **Native Messaging API** to communicate with and launch the local Python script (`scrape_voz.py`) on your system.

---

## 📂 File Structure

```text
voz-scraper-extension/
├── manifest.json              ← Extension manifest configuration (v3)
├── popup.html / popup.js      ← UI and interaction logic for the extension popup
├── background.js              ← Service worker handling Native Messaging calls
├── content.js                 ← Content script (reserved for future updates)
├── voz_native_host.py         ← ⭐ Native Messaging host script (copy to scraper folder)
├── com.antigravity.voz_scraper.json  ← Native host manifest template
├── install.py                 ← Installer & registry registration script
├── make_icons.py              ← Generates placeholder extension icons using Pillow
└── .gitignore                 ← Git exclusion patterns
```

---

## ⚙️ Installation Guide

### Step 1: Copy Host Bridge Files
Copy `voz_native_host.py` and `install.py` into your primary scraper project directory (where `scrape_voz.py` resides). E.g.:
```bash
copy voz_native_host.py F:\Projects\Antigravity\Scrape-Voz\
copy install.py         F:\Projects\Antigravity\Scrape-Voz\
```

### Step 2: Load Extension into Browser
1. Open your browser's extension management page:
   - Chrome: `chrome://extensions/`
   - Opera: `opera://extensions/`
   - Edge: `edge://extensions/`
2. Enable **Developer mode** in the top-right corner.
3. Click **Load unpacked** and select this `voz-scraper-extension` folder.
4. Copy the newly generated **Extension ID** (e.g., `feijklcbaiaobmgbcihhkgijmmejeefp`).

### Step 3: Register Native Messaging Host
Run the installation script to register your extension with the operating system:
```bash
cd F:\Projects\Antigravity\Scrape-Voz
python install.py --extension-id <YOUR_EXTENSION_ID>
```

### Step 4: Generate Icons (Optional)
To create icons for the toolbar:
```bash
pip install Pillow
python make_icons.py
```
*Alternatively, place any custom PNGs named `icon16.png` and `icon48.png` directly into the extension directory.*

---

## 🚀 How to Use

1. Browse to any thread on **voz.vn** (URLs matching `/t/some-thread-title.123456/`).
2. Click the red **V** extension icon on your browser toolbar.
3. Verify the URL field (a **green border** indicates a valid thread URL).
4. Configure your preferences:
   - Check `--download-images` to download all embedded media.
   - Check **Show CMD window** to open a visible console showing live scraping progress.
5. Click **🕷 Scrape thread này** (Scrape this thread) to execute.
