const VOZ_THREAD_RE = /^https:\/\/voz\.vn\/t\/[^/]+\.\d+\/?/;

const urlDisplay = document.getElementById('url-display');
const scrapeBtn  = document.getElementById('scrape-btn');
const statusEl   = document.getElementById('status');
const optImages  = document.getElementById('opt-images');

let currentUrl = '';

function showStatus(msg, type) {
  statusEl.textContent = msg;
  statusEl.className = 'status ' + type;
}

chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
  const url = tabs[0]?.url || '';
  if (VOZ_THREAD_RE.test(url)) {
    currentUrl = url.match(VOZ_THREAD_RE)[0];
    urlDisplay.textContent = currentUrl;
    urlDisplay.className = 'url-box valid';
    scrapeBtn.disabled = false;
  } else {
    urlDisplay.textContent = url
      ? 'Không phải thread VOZ\n(' + url.slice(0, 60) + '...)'
      : 'Không đọc được URL tab hiện tại';
    urlDisplay.className = 'url-box invalid';
  }
});

scrapeBtn.addEventListener('click', () => {
  if (!currentUrl) return;

  scrapeBtn.disabled = true;
  showStatus('⏳ Đang gửi lệnh tới native host...', 'running');

  const payload = {
    url: currentUrl,
    downloadImages: optImages.checked
  };

  chrome.runtime.sendMessage({ action: 'scrape', payload }, (response) => {
    if (chrome.runtime.lastError) {
      showStatus('❌ Lỗi: ' + chrome.runtime.lastError.message, 'error');
      scrapeBtn.disabled = false;
      return;
    }
    if (response?.success) {
      showStatus('✅ Đã launch scraper! Kiểm tra CMD/output.', 'ok');
    } else {
      showStatus('❌ ' + (response?.error || 'Lỗi không xác định'), 'error');
    }
    scrapeBtn.disabled = false;
  });
});
