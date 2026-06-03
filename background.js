// background.js — Service Worker
// Nhận message từ popup, gọi native messaging host để chạy Python

const NATIVE_HOST = 'com.antigravity.voz_scraper';

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action !== 'scrape') return;

  const { url, downloadImages, showWindow } = message.payload;

  chrome.runtime.sendNativeMessage(
    NATIVE_HOST,
    { url, downloadImages, showWindow },
    (response) => {
      if (chrome.runtime.lastError) {
        console.error('[VOZ Scraper] Native messaging error:', chrome.runtime.lastError);
        sendResponse({
          success: false,
          error: chrome.runtime.lastError.message
        });
        return;
      }
      console.log('[VOZ Scraper] Native response:', response);
      sendResponse({ success: true, response });
    }
  );

  // Cần return true để sendResponse hoạt động async
  return true;
});
