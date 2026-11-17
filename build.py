#!/usr/bin/env python3
"""靜態網站產生器。用法：python3 build.py
讀取 content/pages/*.md（YAML front matter + Markdown），輸出到 public/。
"""
import hashlib, html, json, re, shutil, sys
from pathlib import Path
import markdown, yaml
from icons import ICONS

# ---------------------------------------------------------------------------
# CONFIG：公司資料。尚未提供前保持空白，空白欄位不會顯示在網站上。
# ---------------------------------------------------------------------------
CONFIG = {
    "site_name": "",        # 網站名稱
    "phone": "(212) 539-0164",            # 顯示用
    "phone_href": "+12125390164",
    "wechat": "",           # 微信號
    "email": "huarenkaisuo@gmail.com",
    "address": "",          # 刻意留空：網站不顯示實體地址
    "site_url": "https://huarenkaisuo.com",
    "google_verification": "S1JULRL4brwBCXUiI4YZrvPy853_5z00UDD4ziCooNc",  # Google Search Console
    "indexable": True,      # True = 開放搜尋引擎與AI爬蟲索引；False = noindex 封鎖
}
BRAND = CONFIG["site_name"] or "中文鎖匠"
LANG = "zh-Hant-US"
LASTMOD = "2026-11-17"

ROOT = Path(__file__).parent
OUT = ROOT / "public"
PAGES_DIR = ROOT / "content" / "pages"

CATEGORIES = [
    ("residential", "住宅門鎖", "被鎖在門外、換鎖、換鎖芯、智能門鎖與配鑰匙。"),
    ("auto", "汽車鑰匙", "車門打不開、配車鑰匙、遙控鑰匙與鑰匙遺失。"),
    ("commercial", "商業與門禁", "餐館、商鋪、辦公室換鎖與門禁系統。"),
    ("urgent", "緊急與保險箱", "24小時緊急開鎖與保險箱開鎖。"),
]

BANNED = [
    "值得注意的是", "需要注意的是", "總而言之", "綜上所述", "總的來說", "簡而言之", "在當今",
    "深入探討", "至關重要", "不可或缺", "舉足輕重", "賦能", "助力", "打造", "一站式", "全方位",
    "無縫", "讓我們", "毋庸置疑", "另一方面", "接住", "安心無憂", "專業團隊", "優質服務", "竭誠",
    "首要任務", "卓越", "極致", "完美解決", "好問題", "進行開鎖", "進行更換", "作為一名", "扮演著",
]

warnings, errors = [], []
CJK = re.compile(r"[一-鿿]")


def esc(s):
    return html.escape(str(s), quote=True)


def cjk_len(s):
    return len(CJK.findall(s))


def load_pages():
    pages = []
    for f in sorted(PAGES_DIR.glob("*.md")):
        raw = f.read_text(encoding="utf-8")
        m = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.S)
        if not m:
            errors.append(f"{f.name}: 缺少 front matter")
            continue
        fm = re.sub(r'^(\s*(?:- )?[a-z_]+): (?!["\'\[])(.*: .*)$',
                    lambda g: g.group(1) + ": " + json.dumps(g.group(2), ensure_ascii=False),
                    m.group(1), flags=re.M)
        meta = yaml.safe_load(fm)
        meta["body_md"] = m.group(2).strip()
        meta["file"] = f.name
        meta["raw"] = raw
        pages.append(meta)
    return pages


def plate_svg(seed, icon, label="服務示意圖"):
    """頁首插圖：銅色刻度盤、圖示，以及每頁不同齒形的鑰匙。"""
    h = hashlib.md5(seed.encode()).digest()
    cuts = [3 + (b % 5) * 3 for b in h[:8]]
    x, pts = 96, ["96,250"]
    for c in cuts:
        pts += [f"{x + 4},{250 + c}", f"{x + 12},{250 + c}", f"{x + 16},250"]
        x += 18
    pts += [f"{x},250", f"{x + 14},258", f"{x},266", "96,266"]
    ticks = "".join(
        f'<line x1="160" y1="22" x2="160" y2="{32 if i % 5 else 40}" transform="rotate({i * 6} 160 150)"/>'
        for i in range(60))
    rot = h[9] % 40 - 20
    return f'''<svg class="plate" viewBox="0 0 320 300" role="img" aria-label="{esc(label)}" xmlns="http://www.w3.org/2000/svg">
<circle cx="160" cy="150" r="128" class="pl-disc"/>
<g class="pl-ticks">{ticks}</g>
<circle cx="160" cy="150" r="96" class="pl-ring"/>
<g transform="rotate({rot} 160 150)"><circle cx="160" cy="54" r="5" class="pl-dot"/></g>
<g class="pl-icon" transform="translate(99 89) scale(1.9)">{ICONS[icon]}</g>
<g class="pl-keyg"><circle cx="74" cy="258" r="24" class="pl-key"/><circle cx="66" cy="258" r="7" class="pl-hole"/><polygon points="{' '.join(pts)}" class="pl-key"/></g>
</svg>'''


def icon_svg(icon, cls="ico"):
    return f'<svg class="{cls}" viewBox="0 0 64 64" aria-hidden="true" xmlns="http://www.w3.org/2000/svg">{ICONS[icon]}</svg>'


CSS = (ROOT / "src" / "style.css").read_text(encoding="utf-8")
CSS = re.sub(r"/\*.*?\*/", "", CSS, flags=re.S)
CSS = re.sub(r"\s+", " ", CSS)
CSS = re.sub(r"\s*([{};:,>])\s*", r"\1", CSS).replace(";}", "}")


def abs_url(path):
    return CONFIG["site_url"].rstrip("/") + path


def phone_cta(cls="btn btn-rust"):
    if CONFIG["phone"]:
        return f'<a class="{cls}" href="tel:{esc(CONFIG["phone_href"])}">致電 {esc(CONFIG["phone"])}</a>'
    return f'<a class="{cls}" href="/contact/">立即聯繫鎖匠</a>'


def business_ld():
    d = {"@context": "https://schema.org", "@type": "Locksmith", "@id": abs_url("/#business"), "name": BRAND, "url": abs_url("/"),
         "logo": abs_url("/icon-512.png"), "image": abs_url("/og.png"), "priceRange": "$$",
         "areaServed": {"@type": "Country", "name": "United States"},
         "availableLanguage": ["zh-Hant", "zh-Hans", "Mandarin Chinese", "Cantonese", "English"],
         "openingHours": "Mo-Su 00:00-23:59"}
    if CONFIG["phone"]:
        d["telephone"] = CONFIG["phone_href"] or CONFIG["phone"]
    if CONFIG["email"]:
        d["email"] = CONFIG["email"]
    if CONFIG["address"]:
        d["address"] = CONFIG["address"]
    return d


def head(title, desc, path, schema, noindex=False):
    url = abs_url(path)
    schema = [business_ld()] + schema
    ld = "".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schema)
    gsv = f'\n<meta name="google-site-verification" content="{esc(CONFIG["google_verification"])}" />' if CONFIG.get("google_verification") else ""
    robots = "noindex,nofollow" if (noindex or not CONFIG["indexable"]) else "index,follow,max-image-preview:large,max-snippet:-1"
    return f'''<!doctype html>
<html lang="{LANG}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="zh-Hant-US" href="{url}">
<link rel="alternate" hreflang="x-default" href="{url}">
<meta name="robots" content="{robots}">{gsv}
<meta property="og:type" content="website">
<meta property="og:locale" content="zh_TW">
<meta property="og:site_name" content="{esc(BRAND)}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{abs_url("/og.png")}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{esc(BRAND)}：美國華人開鎖服務，國語粵語24小時">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{abs_url("/og.png")}">
<meta name="theme-color" content="#14202b">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-96.png" type="image/png" sizes="96x96">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preload" href="/fonts/fraunces-600.woff2" as="font" type="font/woff2" crossorigin>
<style>{CSS}</style>
{ld}
</head>
<body>
<a class="skip" href="#contenu">跳到主要內容</a>'''


NAV = {}


def header():
    menu = ""
    for key, label, _ in CATEGORIES:
        items = "".join(f'<li><a href="{p["url"]}">{esc(p["name"])}</a></li>' for p in NAV[key])
        menu += f'<div class="mcol"><p class="mcat">{esc(label)}</p><ul>{items}</ul></div>'
    menu += '<div class="mlinks"><a href="/services/">全部服務</a><a href="/pricing/">收費標準</a><a href="/blog/">開鎖知識</a><a href="/faq/">常見問題</a><a href="/about/">關於我們</a><a href="/contact/">聯繫我們</a></div>'
    return f'''<div class="strip"><div class="wrap">全美華人開鎖服務・國語、粵語都可以溝通・24小時</div></div>
<header class="site-head"><div class="wrap hd">
<a class="logo" href="/" aria-label="{esc(BRAND)}首頁">{icon_svg("key", "logo-ico")}<span>{esc(BRAND)}</span></a>
<details class="nav"><summary>服務項目</summary><div class="mega">{menu}</div></details>
{phone_cta("btn btn-rust hd-cta")}
</div></header>
<main id="contenu">'''


def footer():
    cols = ""
    for key, label, _ in CATEGORIES:
        items = "".join(f'<li><a href="{p["url"]}">{esc(p["name"])}</a></li>' for p in NAV[key])
        cols += f'<div><p class="fcat">{esc(label)}</p><ul>{items}</ul></div>'
    contact = ""
    for k, lab in (("phone", "電話"), ("wechat", "微信"), ("email", "電郵"), ("address", "地址")):
        if CONFIG[k]:
            contact += f"<p><strong>{lab}</strong> {esc(CONFIG[k])}</p>"
    return f'''</main>
<footer class="site-foot"><div class="wrap">
<div class="fbrand"><a class="logo logo-light" href="/">{icon_svg("key", "logo-ico")}<span>{esc(BRAND)}</span></a>
<p>我們是在美國服務華人的鎖匠，國語、粵語都能溝通。動手之前，先把做法和價錢跟您講清楚。</p>{contact}</div>
<div class="fcols">{cols}</div>
</div><div class="wrap fbot"><span>{esc(BRAND)}</span><span class="flinks"><a href="/pricing/">收費標準</a><a href="/blog/">開鎖知識</a><a href="/faq/">常見問題</a><a href="/about/">關於我們</a><a href="/contact/">聯繫我們</a></span></div></footer>
<nav class="mbar" aria-label="快速聯繫">{phone_cta("btn btn-rust")}</nav>
<!--Start of Tawk.to Script-->
<script type="text/javascript">
var Tawk_API=Tawk_API||{{}}, Tawk_LoadStart=new Date();
(function(){{
var s1=document.createElement("script"),s0=document.getElementsByTagName("script")[0];
s1.async=true;
s1.src='https://embed.tawk.to/67189f2a4304e3196ad650c1/1ias2rfo5';
s1.charset='UTF-8';
s1.setAttribute('crossorigin','*');
s0.parentNode.insertBefore(s1,s0);
}})();
</script>
<!--End of Tawk.to Script-->
</body></html>'''


def breadcrumb_ld(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": abs_url(u)} for i, (n, u) in enumerate(items)]}


def crumbs_html(items):
    parts = []
    for i, (n, u) in enumerate(items):
        if i == len(items) - 1:
            parts.append(f'<span aria-current="page">{esc(n)}</span>')
        else:
            parts.append(f'<a href="{u}">{esc(n)}</a>')
    return '<nav class="crumbs" aria-label="導覽路徑">' + "<span>/</span>".join(parts) + "</nav>"


def faq_html(faq, title="常見問題"):
    if not faq:
        return ""
    items = "".join(f'<details class="qa"><summary><h3>{esc(f["q"])}</h3></summary><p>{esc(f["a"])}</p></details>' for f in faq)
    return f'<section class="faq"><div class="wrap narrow"><h2>{title}</h2>{items}</div></section>'


def faq_ld(faq):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": f["q"], "acceptedAnswer": {"@type": "Answer", "text": f["a"]}} for f in faq]}


CUTS = '<svg class="cuts" viewBox="0 0 1200 24" preserveAspectRatio="none" aria-hidden="true"><path d="M0 24V10L60 10L72 18L120 18L132 6L192 6L204 16L276 16L288 10L348 10L360 18L408 18L420 6L480 6L492 16L564 16L576 10L636 10L648 18L696 18L708 6L768 6L780 16L852 16L864 10L924 10L936 18L984 18L996 6L1056 6L1068 16L1140 16L1152 10L1200 10V24z"/></svg>'


def check_links(p, body, by_url):
    links = re.findall(r'href="(/[^"#]*)"', body)
    if p["type"] in ("service", "blog") and not 2 <= len(links) <= 3:
        warnings.append(f'{p["url"]}: 正文內部連結 {len(links)} 個（應為2到3個）')
    if len(set(links)) != len(links):
        warnings.append(f'{p["url"]}: 內部連結重複')
    for l in links:
        if l == p["url"]:
            errors.append(f'{p["url"]}: 連結到自己')
        elif l not in by_url:
            errors.append(f'{p["url"]}: 連結失效 {l}')
    if p["type"] == "blog" and "/pricing/" not in links:
        warnings.append(f'{p["url"]}: 文章必須連結到收費標準')


def aka_html(p):
    if not p.get("aka"):
        return ""
    chips = "".join(f"<li>{esc(a)}</li>" for a in p["aka"])
    return f'<div class="aka"><p>也有人搜尋</p><ul>{chips}</ul></div>'


RELATED = {}


def related_html(items, title):
    if not items:
        return ""
    lis = "".join(f'<li><a class="hub-card" href="{q["url"]}">{icon_svg(q["icon"])}<span><strong>{esc(q["h1"])}</strong><em>{esc(q["lead"])}</em></span></a></li>' for q in items)
    return f'<section class="related"><div class="wrap"><h2>{title}</h2><ul class="hub-l">{lis}</ul></div></section>'


def render_service(p, by_url):
    body = markdown.Markdown(extensions=["sane_lists", "tables"]).convert(p["body_md"])
    check_links(p, body, by_url)
    cat = next(c for c in CATEGORIES if c[0] == p["category"])
    quick = "".join(f'<div><dt>{esc(q["label"])}</dt><dd>{esc(q["value"])}</dd></div>' for q in p["quick"])
    steps = "".join(f'<li><span class="sn">{i + 1:02d}</span><h3>{esc(s["t"])}</h3><p>{esc(s["d"])}</p></li>'
                    for i, s in enumerate(p["steps"]))
    crumbs = [("首頁", "/"), ("服務項目", "/services/"), (p["name"], p["url"])]
    schema = [
        {"@context": "https://schema.org", "@type": "WebPage", "name": p["title"], "description": p["description"],
         "inLanguage": LANG, "url": abs_url(p["url"])},
        {"@context": "https://schema.org", "@type": "Service", "name": p["h1"], "serviceType": p["keyword"],
         "description": p["description"], "provider": {"@id": abs_url("/#business")},
         "areaServed": {"@type": "Country", "name": "United States"}, "availableLanguage": ["zh", "yue"]},
        breadcrumb_ld(crumbs), faq_ld(p["faq"]),
    ]
    p["chars"] = cjk_len(body + json.dumps(p["steps"], ensure_ascii=False) + json.dumps(p["faq"], ensure_ascii=False))
    if p["chars"] < 850:
        warnings.append(f'{p["url"]}: 只有 {p["chars"]} 個中文字（至少850）')
    return head(p["title"], p["description"], p["url"], schema) + header() + f'''
<section class="svc-hero"><div class="wrap sh">
<div class="sh-txt">{crumbs_html(crumbs)}
<p class="kicker">{esc(p["kicker"])}</p>
<h1>{esc(p["h1"])}</h1>
<p class="lead">{esc(p["lead"])}</p>
<div class="ctas">{phone_cta()}<a class="btn btn-ghost" href="#steps">服務流程</a></div>
</div>
<div class="sh-art">{plate_svg(p["url"], p["icon"], p["name"] + "示意圖")}</div>
</div>{CUTS}</section>
<div class="wrap svc-grid">
<article class="prose">{body}</article>
<aside class="side"><div class="tag"><span class="hole" aria-hidden="true"></span><p class="tag-t">重點速覽</p><dl>{quick}</dl>{aka_html(p)}</div>
<div class="side-cta"><p>被鎖在外面，或者想先問問價錢？用國語或粵語打給我們都可以。</p>{phone_cta()}</div></aside>
</div>
<section class="steps" id="steps"><div class="wrap"><h2>服務流程</h2><ol>{steps}</ol></div></section>
{faq_html(p["faq"])}
{related_html(RELATED.get(p["url"], []), "延伸閱讀與相關服務")}
<section class="band"><div class="wrap band-in"><p>先講清楚做法和價錢，您同意了我們才動手。</p>{phone_cta("btn btn-brass")}</div></section>''' + footer()


def render_blog(p, by_url):
    body = markdown.Markdown(extensions=["sane_lists", "tables"]).convert(p["body_md"])
    check_links(p, body, by_url)
    crumbs = [("首頁", "/"), ("開鎖知識", "/blog/"), (p["name"], p["url"])]
    schema = [
        {"@context": "https://schema.org", "@type": "BlogPosting", "headline": p["h1"], "description": p["description"],
         "inLanguage": LANG, "datePublished": str(p.get("date", "2026-11-17")), "dateModified": str(p.get("date", "2026-11-17")),
         "mainEntityOfPage": abs_url(p["url"]), "author": {"@id": abs_url("/#business")}, "publisher": {"@id": abs_url("/#business")},
         "image": abs_url("/og.png")},
        breadcrumb_ld(crumbs),
    ]
    if p.get("faq"):
        schema.append(faq_ld(p["faq"]))
    p["chars"] = cjk_len(body + json.dumps(p.get("faq", []), ensure_ascii=False))
    if p["chars"] < 900:
        warnings.append(f'{p["url"]}: 只有 {p["chars"]} 個中文字（至少900）')
    return head(p["title"], p["description"], p["url"], schema) + header() + f'''
<section class="svc-hero"><div class="wrap sh">
<div class="sh-txt">{crumbs_html(crumbs)}
<p class="kicker">{esc(p["kicker"])}</p>
<h1>{esc(p["h1"])}</h1>
<p class="lead">{esc(p["lead"])}</p>
<p class="meta">{esc(BRAND)}・更新日期 <time datetime="{p.get("date", LASTMOD)}">{p.get("date", LASTMOD)}</time></p>
</div>
<div class="sh-art">{plate_svg(p["url"], p["icon"], p["name"] + "示意圖")}</div>
</div>{CUTS}</section>
<div class="wrap svc-grid">
<article class="prose">{body}</article>
<aside class="side">{('<div class="tag"><span class="hole" aria-hidden="true"></span><p class="tag-t">重點速覽</p><dl>' + "".join(f'<div><dt>{esc(q["label"])}</dt><dd>{esc(q["value"])}</dd></div>' for q in p["quick"]) + "</dl>" + aka_html(p) + "</div>") if p.get("quick") else ""}
<div class="side-cta"><p>文章沒寫到您的情況？直接問我們，國語、粵語都可以。</p>{phone_cta()}</div></aside>
</div>
{faq_html(p.get("faq"))}
{related_html(RELATED.get(p["url"], []), "相關服務與其他文章")}
<section class="band"><div class="wrap band-in"><p>需要鎖匠上門？先問價錢，不收冤枉錢。</p>{phone_cta("btn btn-brass")}</div></section>''' + footer()


def contact_block():
    rows = []
    if CONFIG["phone"]:
        rows.append(f'<li><strong>電話</strong><a href="tel:{esc(CONFIG["phone_href"])}">{esc(CONFIG["phone"])}</a></li>')
        rows.append(f'<li><strong>短訊</strong><a href="sms:{esc(CONFIG["phone_href"])}">{esc(CONFIG["phone"])}</a></li>')
    if CONFIG["wechat"]:
        rows.append(f'<li><strong>微信</strong><span>{esc(CONFIG["wechat"])}</span></li>')
    if CONFIG["email"]:
        rows.append(f'<li><strong>電郵</strong><a href="mailto:{esc(CONFIG["email"])}">{esc(CONFIG["email"])}</a></li>')
    if CONFIG["address"]:
        rows.append(f'<li><strong>地址</strong><span>{esc(CONFIG["address"])}</span></li>')
    if not rows:
        return '<div class="cbox"><p>電話、微信和電郵即將公布。</p></div>'
    return '<ul class="cbox">' + "".join(rows) + "</ul>"


def render_page(p, by_url):
    body_md = p["body_md"].replace("{{CONTACT}}", "<!--CONTACT-->")
    body = markdown.Markdown(extensions=["sane_lists", "tables"]).convert(body_md)
    body = body.replace("<p><!--CONTACT--></p>", contact_block()).replace("<!--CONTACT-->", contact_block())
    check_links(p, body, by_url)
    crumbs = [("首頁", "/"), (p["name"], p["url"])]
    schema = [{"@context": "https://schema.org", "@type": "WebPage", "name": p["title"], "description": p["description"],
               "inLanguage": LANG, "url": abs_url(p["url"])}, breadcrumb_ld(crumbs)]
    if p.get("faq"):
        schema.append(faq_ld(p["faq"]))
    return head(p["title"], p["description"], p["url"], schema) + header() + f'''
<section class="svc-hero"><div class="wrap sh">
<div class="sh-txt">{crumbs_html(crumbs)}
<p class="kicker">{esc(p["kicker"])}</p>
<h1>{esc(p["h1"])}</h1>
<p class="lead">{esc(p["lead"])}</p>
</div>
<div class="sh-art">{plate_svg(p["url"], p["icon"], p["name"] + "示意圖")}</div>
</div>{CUTS}</section>
<div class="wrap narrow page-body prose">{body}</div>
{faq_html(p.get("faq"), p.get("faq_title", "常見問題"))}
<section class="band"><div class="wrap band-in"><p>還有問題？打給我們，國語、粵語都可以。</p>{phone_cta("btn btn-brass")}</div></section>''' + footer()


def render_home(services, posts):
    cats = ""
    for key, label, blurb in CATEGORIES:
        items = "".join(f'<li><a href="{p["url"]}">{icon_svg(p["icon"])}<span>{esc(p["name"])}</span></a></li>' for p in NAV[key])
        cats += f'<div class="cat"><h3>{esc(label)}</h3><p>{esc(blurb)}</p><ul>{items}</ul></div>'
    top_posts = [p for p in posts if p.get("priority") in ("P1", "P2")][:4]
    blog = "".join(f'<li><a class="hub-card" href="{p["url"]}">{icon_svg(p["icon"])}<span><strong>{esc(p["h1"])}</strong><em>{esc(p["lead"])}</em></span></a></li>' for p in top_posts)
    faq = [
        {"q": "你們在美國哪些地方提供開鎖服務？", "a": "我們在全美各地提供服務。打電話時告訴我們地址，我們會先確認多久能到，再決定要不要出發。"},
        {"q": "可以用國語或粵語溝通嗎？", "a": "可以。電話裡和到現場都能用國語、粵語溝通，價錢、做法和注意事項都用中文講清楚，不用擔心英文說不好。"},
        {"q": "開鎖多少錢？會不會到了現場才加價？", "a": "我們在電話裡就報價。到了現場如果發現跟描述不一樣，例如是高安全鎖芯，會先跟您說明，您同意了才繼續。"},
        {"q": "开锁需要出示什么证件？", "a": "需要。開門前我們會核對身分證件，以及能證明您住在這裡或車是您的文件，例如租約、水電帳單或車輛登記。這是為了保護您。"},
    ]
    schema = [{"@context": "https://schema.org", "@type": "WebSite", "name": BRAND, "inLanguage": LANG, "url": abs_url("/")}, faq_ld(faq)]
    title = "開鎖｜美國華人開鎖服務・24小時中文鎖匠"
    desc = "在美國被鎖在門外、要換鎖或配車鑰匙？我們是會說國語、粵語的華人鎖匠，24小時上門開鎖，先報價再動手。"
    pins = "".join(f'<span class="pin" style="--i:{i}"></span>' for i in range(5))
    return head(title, desc, "/", schema) + header() + f'''
<section class="hero"><div class="wrap hero-in">
<div class="hero-txt">
<p class="kicker kicker-light">開鎖・換鎖・配鑰匙・國語粵語服務</p>
<h1>美國華人開鎖服務<span class="vh"> - </span><em>24小時中文鎖匠</em></h1>
<p class="lead">在美國被鎖在門外，最怕的就是講不清楚、聽不懂報價。我們是說中文的鎖匠，房子、汽車、店鋪、保險箱都能開，到場之前先把做法和價錢講明白。</p>
<div class="ctas">{phone_cta()}<a class="btn btn-ghost-light" href="/services/">查看所有開鎖服務</a></div>
</div>
<div class="hero-art" aria-hidden="true"><div class="cyl"><div class="plug"></div>{pins}<div class="hkey"></div></div><p class="cyl-cap">五顆彈子，只有一把對的鑰匙。</p></div>
</div></section>
<section class="intro"><div class="wrap narrow prose">
<h2>為什麼找會說中文的開鎖師傅？</h2>
<p>開鎖這件事，常常發生在最不方便的時候：半夜下班回家、帶著小孩、手機快沒電。這時候還要用英文解釋「鎖芯」「鎖舌」，或者聽懂對方報的各種費用，真的很累。</p>
<p>所以我們用國語和粵語接電話，到了現場也用中文跟您溝通。能不破壞就不破壞，能修就不換，換鎖、<a href="/services/rekey/">換鎖芯</a>、<a href="/services/car-keys/">配車鑰匙</a>都在一次上門裡解決。</p>
<p>有時候您其實不需要我們。門只是關緊了、鑰匙只是有點卡，我們也會照實說，教您自己調整。</p>
</div></section>
<section class="cats"><div class="wrap"><h2 class="sec-t">我們的開鎖服務</h2><div class="cat-grid">{cats}</div><p class="more"><a href="/services/">全部開鎖服務項目</a>・<a href="/pricing/">開鎖收費標準</a></p></div></section>
<section class="how"><div class="wrap"><h2 class="sec-t">找我們開鎖的流程</h2><ol class="how-l">
<li><span class="sn">01</span><h3>告訴我們狀況</h3><p>門的種類、鎖的牌子、車的年份型號，能拍張照片最好。</p></li>
<li><span class="sn">02</span><h3>電話裡先報價</h3><p>出發前就說清楚價錢和大概到達時間，不是到了才開價。</p></li>
<li><span class="sn">03</span><h3>核對身分再開門</h3><p>先看證件和地址證明，然後選最不傷鎖的方法。</p></li>
<li><span class="sn">04</span><h3>當面測試</h3><p>每把鑰匙、每道鎖都當著您的面試過，您確認沒問題我們才走。</p></li>
</ol></div></section>
<section class="cats"><div class="wrap"><h2 class="sec-t">開鎖知識</h2><ul class="hub-l">{blog}</ul><p class="more"><a href="/blog/">看更多開鎖與防盜知識</a></p></div></section>
{faq_html(faq)}
<section class="band"><div class="wrap band-in"><p>現在就被鎖在門外？先從這裡開始。</p><a class="btn btn-brass" href="/services/24-hour-emergency-locksmith/">24小時緊急開鎖</a></div></section>''' + footer()


def render_services_hub():
    blocks = ""
    for key, label, blurb in CATEGORIES:
        items = "".join(f'<li><a class="hub-card" href="{p["url"]}">{icon_svg(p["icon"])}<span><strong>{esc(p["h1"])}</strong><em>{esc(p["lead"])}</em></span></a></li>' for p in NAV[key])
        blocks += f'<section class="hub-sec"><h2>{esc(label)}</h2><p>{esc(blurb)}</p><ul class="hub-l">{items}</ul></section>'
    crumbs = [("首頁", "/"), ("服務項目", "/services/")]
    return head("開鎖服務項目｜住宅、汽車、商業開鎖與換鎖", "我們在美國提供的全部開鎖服務：住宅開鎖、換鎖、換鎖芯、智能門鎖、汽車開鎖、配車鑰匙、保險箱開鎖與商業換鎖，國語粵語服務。", "/services/", [breadcrumb_ld(crumbs)]) + header() + f'''
<section class="svc-hero hub-hero"><div class="wrap">{crumbs_html(crumbs)}<h1>開鎖服務項目</h1><p class="lead">以下是我們每週都在做的開鎖服務，依照您被鎖住的地方分類。不確定屬於哪一項？打電話描述狀況就好，我們幫您判斷。</p></div></section>
<div class="wrap hub">{blocks}<p class="more"><a href="/pricing/">各項服務的參考價格請看收費標準</a></p></div>''' + footer()


def render_blog_hub(posts):
    items = "".join(f'<li><a class="hub-card" href="{p["url"]}">{icon_svg(p["icon"])}<span><strong>{esc(p["h1"])}</strong><em>{esc(p["lead"])}</em></span></a></li>' for p in posts)
    crumbs = [("首頁", "/"), ("開鎖知識", "/blog/")]
    schema = [breadcrumb_ld(crumbs), {"@context": "https://schema.org", "@type": "Blog", "name": "開鎖知識與防盜指南", "inLanguage": LANG, "url": abs_url("/blog/")}]
    return head("開鎖知識與防盜指南｜美國華人鎖匠經驗分享", "在美國開鎖、換鎖要多少錢？鑰匙鎖在車裡怎麼辦？租房可以換鎖嗎？鎖匠用中文整理的實用知識與防盜建議。", "/blog/", schema) + header() + f'''
<section class="svc-hero hub-hero"><div class="wrap">{crumbs_html(crumbs)}<h1>開鎖知識與防盜指南</h1><p class="lead">這些都是客人在電話裡最常問我們的問題。我們把答案寫下來，希望您下次遇到時心裡有底。</p></div></section>
<div class="wrap hub"><ul class="hub-l">{items}</ul></div>''' + footer()


def render_404():
    return head("找不到這個頁面", "這個頁面不存在或已經移動。", "/404", [], noindex=True) + header() + '''
<section class="svc-hero"><div class="wrap narrow"><p class="kicker">404</p><h1>這扇門後面什麼都沒有</h1><p class="lead">您要找的頁面不存在，或者換了地址。別擔心，從這裡繼續。</p><div class="ctas"><a class="btn btn-rust" href="/services/">查看開鎖服務</a><a class="btn btn-ghost" href="/">回到首頁</a></div></div></section>''' + footer()


# ---------------------------------------------------------------------------
def lint(p):
    raw = p["raw"]
    if "—" in raw or "–" in raw:
        errors.append(f'{p["url"]}: 禁止使用破折號')
    for b in BANNED:
        if b in raw:
            warnings.append(f'{p["url"]}: 避免使用「{b}」')
    if raw.count("此外") > 1:
        warnings.append(f'{p["url"]}: 「此外」出現超過一次')
    if re.search(r"不僅.{0,25}(而且|更)", raw):
        warnings.append(f'{p["url"]}: 「不僅……而且/更」句型')
    body = p["body_md"]
    if re.search(r"[一-鿿] [A-Za-z0-9]|[A-Za-z0-9] [一-鿿]", body):
        m = re.search(r".{0,6}([一-鿿] [A-Za-z0-9]|[A-Za-z0-9] [一-鿿]).{0,6}", body)
        warnings.append(f'{p["url"]}: 中文與英數之間有半形空格「{m.group(0)}」')
    if re.search(r"[一-鿿][,.;:!?]", body):
        m = re.search(r".{0,6}[一-鿿][,.;:!?].{0,3}", body)
        warnings.append(f'{p["url"]}: 中文後面用了半形標點「{m.group(0)}」')
    if len(p["title"]) > 34:
        warnings.append(f'{p["url"]}: title 太長（{len(p["title"])}）')
    if not 50 <= len(p["description"]) <= 100:
        warnings.append(f'{p["url"]}: description {len(p["description"])} 字')


def main():
    pages = load_pages()
    by_url = {p["url"]: p for p in pages}
    for u in ("/", "/services/", "/blog/"):
        by_url[u] = {"url": u}
    services = [p for p in pages if p["type"] == "service"]
    posts = sorted([p for p in pages if p["type"] == "blog"], key=lambda p: p.get("order", 99))
    others = [p for p in pages if p["type"] == "page"]
    for key, *_ in CATEGORIES:
        NAV[key] = sorted([p for p in services if p["category"] == key], key=lambda p: p.get("order", 99))
    def links_of(q):
        return re.findall(r'\]\((/[^)]+)\)', q["body_md"])
    for s in services:
        rel = [b for b in posts if s["url"] in links_of(b)]
        sibs = [x for x in NAV[s["category"]] if x["url"] != s["url"] and x["url"] not in links_of(s)]
        RELATED[s["url"]] = (rel + sibs)[:3]
    for i, b in enumerate(posts):
        svc = [by_url[u] for u in links_of(b) if u.startswith("/services/")]
        more_posts = [posts[(i + k) % len(posts)] for k in range(1, len(posts)) if posts[(i + k) % len(posts)]["url"] not in links_of(b)]
        RELATED[b["url"]] = (svc[:1] + more_posts)[:3]
    for p in pages:
        if p["icon"] not in ICONS:
            errors.append(f'{p["url"]}: 未知圖示 {p["icon"]}')
        lint(p)
    if errors:
        print("錯誤：\n  " + "\n  ".join(errors))
        sys.exit(1)

    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "fonts").mkdir(parents=True)
    shutil.copy(ROOT / "src" / "fraunces-600.woff2", OUT / "fonts" / "fraunces-600.woff2")
    for icon in ("og.png", "favicon.svg", "favicon.ico", "favicon-48.png", "favicon-96.png", "apple-touch-icon.png", "icon-192.png", "icon-512.png"):
        shutil.copy(ROOT / "src" / icon, OUT / icon)
    (OUT / "site.webmanifest").write_text(json.dumps({
        "name": BRAND, "short_name": BRAND, "lang": "zh-Hant", "start_url": "/", "display": "standalone",
        "background_color": "#f5f0e6", "theme_color": "#14202b",
        "icons": [{"src": "/icon-192.png", "sizes": "192x192", "type": "image/png"},
                  {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png"},
                  {"src": "/favicon.svg", "sizes": "any", "type": "image/svg+xml"}]}, ensure_ascii=False, indent=2), encoding="utf-8")

    def write(url, content):
        path = OUT / url.strip("/") / "index.html" if url != "/404" else OUT / "404.html"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    write("/", render_home(services, posts))
    write("/services/", render_services_hub())
    write("/blog/", render_blog_hub(posts))
    write("/404", render_404())
    for p in services:
        write(p["url"], render_service(p, by_url))
    for p in posts:
        write(p["url"], render_blog(p, by_url))
    for p in others:
        write(p["url"], render_page(p, by_url))
    if errors:
        print("錯誤：\n  " + "\n  ".join(errors))
        sys.exit(1)

    base = CONFIG["site_url"].rstrip("/")
    urls = ["/", "/services/", "/blog/"] + [p["url"] for p in services + posts + others]
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"<url><loc>{base}{u}</loc><lastmod>{LASTMOD}</lastmod></url>\n" for u in urls) + "</urlset>\n", encoding="utf-8")
    if CONFIG["indexable"]:
        bots = ["Googlebot", "Bingbot", "Google-Extended", "GPTBot", "OAI-SearchBot", "ChatGPT-User",
                "ClaudeBot", "Claude-SearchBot", "Claude-User", "PerplexityBot", "Perplexity-User",
                "Applebot", "Applebot-Extended", "DuckDuckBot", "CCBot"]
        txt = "".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots)
        txt += f"User-agent: *\nAllow: /\n\nSitemap: {base}/sitemap.xml\n"
        (OUT / "robots.txt").write_text(txt, encoding="utf-8")
    else:
        # 不用 Disallow：讓搜尋引擎能讀到每頁的 noindex
        (OUT / "robots.txt").write_text("User-agent: *\nAllow: /\n", encoding="utf-8")
    import json as _j
    vc = _j.loads((ROOT / "vercel.json").read_text(encoding="utf-8"))
    hdrs = next(h for h in vc["headers"] if h["source"] == "/(.*)")["headers"]
    hdrs[:] = [h for h in hdrs if h["key"] != "X-Robots-Tag"]
    if not CONFIG["indexable"]:
        hdrs.append({"key": "X-Robots-Tag", "value": "noindex, nofollow"})
    (ROOT / "vercel.json").write_text(_j.dumps(vc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    llms = [f"# {BRAND}", "", "> 在美國服務華人的鎖匠，國語、粵語都能溝通，24小時上門：住宅開鎖、換鎖、換鎖芯、智能門鎖、汽車開鎖、配車鑰匙、保險箱開鎖、商業換鎖。網站內容為繁體中文。", ""]
    for key, label, _ in CATEGORIES:
        llms.append(f"## {label}")
        llms += [f'- [{p["h1"]}]({base}{p["url"]}): {p["description"]}' for p in NAV[key]]
        llms.append("")
    llms.append("## 開鎖知識")
    llms += [f'- [{p["h1"]}]({base}{p["url"]}): {p["description"]}' for p in posts]
    llms.append("")
    llms.append("## 其他")
    llms += [f'- [{p["h1"]}]({base}{p["url"]}): {p["description"]}' for p in others]
    (OUT / "llms.txt").write_text("\n".join(llms) + "\n", encoding="utf-8")

    total = sum(p.get("chars", 0) for p in services + posts)
    print(f"完成：{len(services)} 個服務頁、{len(posts)} 篇文章、{len(others)} 個其他頁面，共 {total} 個中文字。")
    if warnings:
        print("警告：\n  " + "\n  ".join(warnings))


if __name__ == "__main__":
    main()
