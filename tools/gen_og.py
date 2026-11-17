"""Generate src/og.png (1200x630 share image). Run again if BRAND/phone/domain change:
python3 tools/gen_og.py  (needs playwright + Chrome)"""
import sys, pathlib
from playwright.sync_api import sync_playwright
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from build import BRAND, CONFIG, ICONS
domain = CONFIG["site_url"].split("//")[1]
key = ICONS["key"]
html = f"""<html><body style="margin:0;width:1200px;height:630px;background:radial-gradient(ellipse at 80% 20%,#24384a 0,#14202b 62%);font-family:'PingFang TC','Noto Sans CJK TC','Noto Sans TC','Microsoft JhengHei',sans-serif;color:#efe6d4;position:relative;overflow:hidden">
<svg viewBox="0 0 64 64" style="position:absolute;right:70px;top:120px;width:380px;height:380px;transform:rotate(-35deg);fill:none;stroke:#e0ac4a;stroke-width:5;stroke-linecap:round;stroke-linejoin:round;opacity:.95">{key}</svg>
<div style="position:absolute;left:80px;top:110px;width:700px">
<div style="font-size:28px;letter-spacing:6px;color:#e0ac4a;font-weight:700">開鎖・換鎖・配鑰匙</div>
<div style="font-size:84px;font-weight:800;line-height:1.15;margin-top:22px;color:#fff">{BRAND}</div>
<div style="font-size:42px;font-weight:700;line-height:1.35;margin-top:18px">美國華人開鎖服務<br><span style="color:#e0ac4a">國語・粵語 24小時</span></div>
<div style="font-size:30px;margin-top:40px;color:#cfc4ae">{domain}{"　" + CONFIG["phone"] if CONFIG["phone"] else ""}</div>
</div></body></html>"""
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome")
    pg = b.new_page(viewport={"width": 1200, "height": 630})
    pg.set_content(html); pg.wait_for_timeout(300)
    pg.screenshot(path=str(ROOT / "src" / "og.png")); b.close()
print("src/og.png written")
