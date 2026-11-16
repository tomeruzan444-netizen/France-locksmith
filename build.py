#!/usr/bin/env python3
"""Générateur du site statique. Usage : python3 build.py
Lit content/pages/*.md (front matter YAML + Markdown) et écrit le site HTML dans public/.
"""
import hashlib, html, json, re, shutil, sys
from pathlib import Path
import markdown, yaml
from icons import ICONS

# ---------------------------------------------------------------------------
# CONFIG : coordonnées de l'entreprise. Laisser vide tant qu'elles ne sont pas fournies.
# ---------------------------------------------------------------------------
CONFIG = {
    "site_name": "",          # ex. "Serrurier Express"
    "phone": "",              # ex. "+1 555 123 4567" (affiché)
    "phone_href": "",         # ex. "+15551234567"
    "email": "",
    "address": "",            # adresse complète
    "site_url": "https://france-locksmith.vercel.app",
}
BRAND = CONFIG["site_name"] or "Serrurier en français"

ROOT = Path(__file__).parent
OUT = ROOT / "public"
PAGES_DIR = ROOT / "content" / "pages"

CATEGORIES = [
    ("residentiel", "Maison et appartement", "Ouvertures, serrures, clés et sécurité chez vous."),
    ("auto", "Voiture", "Portières, coffre, clés codées et télécommandes."),
    ("commercial", "Commerces et bureaux", "Portes de magasin, contrôle d'accès, conformité des issues."),
    ("coffres", "Coffres-forts et urgences", "Ouverture, pose de coffre et intervention de nuit."),
]

BANNED = [
    "plonger dans", "plongeons", "il est essentiel de noter", "il est important de souligner", "crucial",
    "incontournable", "primordial", "véritablement", "réellement", "essentiellement", "en conclusion",
    "pour conclure", "en résumé", "en somme", "dans un monde où", "à l'ère de", "au cœur de",
    "un éventail de", "une gamme complète", "solutions sur mesure", "expertise inégalée", "n'hésitez pas",
    "faire la différence", "optimal", "optimiser", "votre sécurité est notre priorité", "fiable et efficace",
    "rapide et efficace", "effectuer", "effectuons", "débuter", "proactif", "holistique", "robuste", "synergie",
    "effet de levier", "non seulement", "joue un rôle clé", "témoigne de", "enjeu majeur", "bien sûr !",
]

warnings, errors = [], []


# ---------------------------------------------------------------------------
def esc(s):
    return html.escape(str(s), quote=True)


def fr_typo(page):
    """Espaces insécables de la typographie française, hors balises, scripts et styles."""
    parts = re.split(r"(<script.*?</script>|<style.*?</style>|<[^>]+>)", page, flags=re.S)
    for i, p in enumerate(parts):
        if p.startswith("<"):
            continue
        p = re.sub(r"[  ]([;!?])", " \\1", p)
        p = re.sub(r"[  ]:(?=\s|$)", " :", p)
        p = p.replace("« ", "« ").replace(" »", " »")
        parts[i] = p
    return "".join(parts)


def load_pages():
    pages = []
    for f in sorted(PAGES_DIR.glob("*.md")):
        raw = f.read_text(encoding="utf-8")
        m = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.S)
        if not m:
            errors.append(f"{f.name}: front matter manquant")
            continue
        fm = re.sub(r'^(\s*(?:- )?[a-z_]+): (?!["\'])(.*: .*)$',
                    lambda g: g.group(1) + ": " + json.dumps(g.group(2), ensure_ascii=False),
                    m.group(1), flags=re.M)
        meta = yaml.safe_load(fm)
        meta["body_md"] = m.group(2).strip()
        meta["file"] = f.name
        pages.append(meta)
    return pages


def plate_svg(slug, icon):
    """Illustration d'en-tête : cadran laiton, pictogramme et profil de clé propre à chaque page."""
    h = hashlib.md5(slug.encode()).digest()
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
    return f'''<svg class="plate" viewBox="0 0 320 300" role="img" aria-label="Illustration du service" xmlns="http://www.w3.org/2000/svg">
<circle cx="160" cy="150" r="128" class="pl-disc"/>
<g class="pl-ticks">{ticks}</g>
<circle cx="160" cy="150" r="96" class="pl-ring"/>
<g transform="rotate({rot} 160 150)"><circle cx="160" cy="54" r="5" class="pl-dot"/></g>
<g class="pl-icon" transform="translate(99 89) scale(1.9)">{ICONS[icon]}</g>
<g class="pl-keyg"><circle cx="74" cy="258" r="24" class="pl-key"/><circle cx="66" cy="258" r="7" class="pl-hole"/><polygon points="{' '.join(pts)}" class="pl-key"/></g>
</svg>'''


def icon_svg(icon, cls="ico"):
    return f'<svg class="{cls}" viewBox="0 0 64 64" aria-hidden="true" xmlns="http://www.w3.org/2000/svg">{ICONS[icon]}</svg>'


# ---------------------------------------------------------------------------
CSS = (ROOT / "src" / "style.css").read_text(encoding="utf-8")
CSS = re.sub(r"/\*.*?\*/", "", CSS, flags=re.S)
CSS = re.sub(r"\s+", " ", CSS)
CSS = re.sub(r"\s*([{};:,>])\s*", r"\1", CSS).replace(";}", "}")


def phone_cta(cls="btn btn-rust"):
    if CONFIG["phone"]:
        return f'<a class="{cls}" href="tel:{esc(CONFIG["phone_href"])}">Appeler le {esc(CONFIG["phone"])}</a>'
    return f'<a class="{cls}" href="/serrurier-urgence/">Besoin d\'un serrurier maintenant</a>'


def head(title, desc, path, schema):
    url = CONFIG["site_url"].rstrip("/") + path
    ld = "".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schema)
    return f'''<!doctype html>
<html lang="fr-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="fr-us" href="{url}">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">
<meta property="og:type" content="website">
<meta property="og:locale" content="fr_US">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta name="theme-color" content="#14202b">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preload" href="/fonts/fraunces-600.woff2" as="font" type="font/woff2" crossorigin>
<style>{CSS}</style>
{ld}
</head>
<body>
<a class="skip" href="#contenu">Aller au contenu</a>'''


def header(pages_by_cat):
    menu = ""
    for key, label, _ in CATEGORIES:
        items = "".join(f'<li><a href="/{p["slug"]}/">{esc(p["name"])}</a></li>' for p in pages_by_cat[key])
        menu += f'<div class="mcol"><p class="mcat">{esc(label)}</p><ul>{items}</ul></div>'
    return f'''<div class="strip"><div class="wrap">Serruriers francophones partout aux États-Unis, 24 h/24</div></div>
<header class="site-head"><div class="wrap hd">
<a class="logo" href="/" aria-label="{esc(BRAND)}, accueil">{icon_svg("key", "logo-ico")}<span>{esc(BRAND)}</span></a>
<details class="nav"><summary>Nos services</summary><div class="mega">{menu}<a class="mall" href="/services/">Voir tous les services</a></div></details>
{phone_cta("btn btn-rust hd-cta")}
</div></header>
<main id="contenu">'''


def footer(pages_by_cat):
    cols = ""
    for key, label, _ in CATEGORIES:
        items = "".join(f'<li><a href="/{p["slug"]}/">{esc(p["name"])}</a></li>' for p in pages_by_cat[key])
        cols += f'<div><p class="fcat">{esc(label)}</p><ul>{items}</ul></div>'
    contact = ""
    for k, lab in (("phone", "Téléphone"), ("email", "Courriel"), ("address", "Adresse")):
        if CONFIG[k]:
            contact += f"<p><strong>{lab}</strong> {esc(CONFIG[k])}</p>"
    return f'''</main>
<footer class="site-foot"><div class="wrap">
<div class="fbrand"><a class="logo logo-light" href="/">{icon_svg("key", "logo-ico")}<span>{esc(BRAND)}</span></a>
<p>Nous sommes des serruriers qui travaillent en français, pour les francophones installés aux États-Unis. On vous explique tout, dans votre langue, avant de toucher à quoi que ce soit.</p>{contact}</div>
<div class="fcols">{cols}</div>
</div><div class="wrap fbot"><span>{esc(BRAND)}</span><a href="/services/">Plan des services</a></div></footer>
<nav class="mbar" aria-label="Accès rapide">{phone_cta("btn btn-rust")}</nav>
</body></html>'''


def breadcrumb_ld(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": CONFIG["site_url"].rstrip("/") + u}
        for i, (n, u) in enumerate(items)]}


# ---------------------------------------------------------------------------
def render_service(p, by_slug, pages_by_cat):
    md = markdown.Markdown(extensions=["sane_lists"])
    body = md.convert(p["body_md"])
    # liens internes
    links = re.findall(r'href="(/[^"]*)"', body)
    if not 2 <= len(links) <= 3:
        warnings.append(f'{p["slug"]}: {len(links)} lien(s) interne(s) dans le texte (2 à 3 attendus)')
    if len(set(links)) != len(links):
        warnings.append(f'{p["slug"]}: lien interne en double')
    for l in links:
        target = l.strip("/")
        if target == p["slug"]:
            errors.append(f'{p["slug"]}: lien vers lui-même')
        elif target not in by_slug:
            errors.append(f'{p["slug"]}: lien cassé {l}')
    cat = next(c for c in CATEGORIES if c[0] == p["category"])
    url = f'/{p["slug"]}/'
    quick = "".join(f'<div><dt>{esc(q["label"])}</dt><dd>{esc(q["value"])}</dd></div>' for q in p["quick"])
    steps = "".join(
        f'<li><span class="sn">{i + 1:02d}</span><h3>{esc(s["t"])}</h3><p>{esc(s["d"])}</p></li>'
        for i, s in enumerate(p["steps"]))
    faq = "".join(
        f'<details class="qa"><summary><h3>{esc(f["q"])}</h3></summary><p>{esc(f["a"])}</p></details>'
        for f in p["faq"])
    schema = [
        {"@context": "https://schema.org", "@type": "WebPage", "name": p["title"], "description": p["description"],
         "inLanguage": "fr-US", "url": CONFIG["site_url"].rstrip("/") + url},
        {"@context": "https://schema.org", "@type": "Service", "name": p["h1"], "serviceType": p["name"],
         "description": p["description"], "areaServed": {"@type": "Country", "name": "États-Unis"},
         "availableLanguage": "fr"},
        breadcrumb_ld([("Accueil", "/"), ("Services", "/services/"), (p["name"], url)]),
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": f["q"], "acceptedAnswer": {"@type": "Answer", "text": f["a"]}}
            for f in p["faq"]]},
    ]
    words = len(re.findall(r"\w+", re.sub("<[^>]+>", " ", body) + " ".join(
        s["t"] + " " + s["d"] for s in p["steps"]) + " ".join(f["q"] + " " + f["a"] for f in p["faq"])))
    p["words"] = words
    if words < 650:
        warnings.append(f'{p["slug"]}: {words} mots (650 minimum)')
    page = head(p["title"], p["description"], url, schema) + header(pages_by_cat) + f'''
<section class="svc-hero"><div class="wrap sh">
<div class="sh-txt">
<nav class="crumbs" aria-label="Fil d'Ariane"><a href="/">Accueil</a><span>/</span><a href="/services/">{esc(cat[1])}</a><span>/</span><span aria-current="page">{esc(p["name"])}</span></nav>
<p class="kicker">{esc(p["kicker"])}</p>
<h1>{esc(p["h1"])}</h1>
<p class="lead">{esc(p["lead"])}</p>
<div class="ctas">{phone_cta()}<a class="btn btn-ghost" href="#deroulement">Comment ça se passe</a></div>
</div>
<div class="sh-art">{plate_svg(p["slug"], p["icon"])}</div>
</div><svg class="cuts" viewBox="0 0 1200 24" preserveAspectRatio="none" aria-hidden="true"><path d="M0 24V10L60 10L72 18L120 18L132 6L192 6L204 16L276 16L288 10L348 10L360 18L408 18L420 6L480 6L492 16L564 16L576 10L636 10L648 18L696 18L708 6L768 6L780 16L852 16L864 10L924 10L936 18L984 18L996 6L1056 6L1068 16L1140 16L1152 10L1200 10V24z"/></svg></section>
<div class="wrap svc-grid">
<article class="prose">{body}</article>
<aside class="side"><div class="tag"><span class="hole" aria-hidden="true"></span><p class="tag-t">Fiche express</p><dl>{quick}</dl></div>
<div class="side-cta"><p>Vous êtes bloqué ou vous avez une question précise ? On vous répond en français.</p>{phone_cta()}</div></aside>
</div>
<section class="steps" id="deroulement"><div class="wrap"><h2>Le déroulement, étape par étape</h2><ol>{steps}</ol></div></section>
<section class="faq"><div class="wrap narrow"><h2>Vos questions, nos réponses</h2>{faq}</div></section>
<section class="band"><div class="wrap band-in"><p>On parle votre langue, on vous dit ce qu'on va faire avant de le faire.</p>{phone_cta("btn btn-brass")}</div></section>''' + footer(pages_by_cat)
    return page


def render_home(pages, pages_by_cat):
    cats = ""
    for key, label, blurb in CATEGORIES:
        items = "".join(
            f'<li><a href="/{p["slug"]}/">{icon_svg(p["icon"])}<span>{esc(p["name"])}</span></a></li>'
            for p in pages_by_cat[key])
        cats += f'<div class="cat"><h3>{esc(label)}</h3><p>{esc(blurb)}</p><ul>{items}</ul></div>'
    faq = [
        ("Est-ce que vous intervenez partout aux États-Unis ?",
         "Oui, nous travaillons à l'échelle du pays. Quand vous nous appelez, on vous confirme tout de suite le délai d'arrivée pour votre adresse, avant de vous engager à quoi que ce soit."),
        ("Pourquoi faire appel à un serrurier qui parle français ?",
         "Parce qu'une porte bloquée à 23 h, c'est déjà assez stressant. Pouvoir expliquer le problème dans votre langue, comprendre le devis et poser vos questions sans chercher vos mots, ça évite les malentendus et les mauvaises surprises."),
        ("Comment savoir combien ça va coûter ?",
         "On vous donne le prix au téléphone dès qu'on connaît le type de serrure et la situation. Si, une fois sur place, on découvre autre chose, on vous le dit et on attend votre accord avant de continuer."),
        ("Devez-vous prouver que j'habite à l'adresse ?",
         "Oui, et c'est pour votre protection. Avant d'ouvrir un logement ou une voiture, nous demandons une pièce d'identité et un document qui relie la personne au lieu ou au véhicule."),
    ]
    faq_html = "".join(f'<details class="qa"><summary><h3>{esc(q)}</h3></summary><p>{esc(a)}</p></details>' for q, a in faq)
    schema = [
        {"@context": "https://schema.org", "@type": "WebSite", "name": BRAND, "inLanguage": "fr-US",
         "url": CONFIG["site_url"]},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
    ]
    title = "Serrurier francophone aux États-Unis, 24 h/24"
    desc = "Porte claquée, clé de voiture perdue, serrure à changer : nous sommes des serruriers qui parlent français et interviennent partout aux États-Unis, jour et nuit."
    pins = "".join(f'<span class="pin" style="--i:{i}"></span>' for i in range(5))
    return head(title, desc, "/", schema) + header(pages_by_cat) + f'''
<section class="hero"><div class="wrap hero-in">
<div class="hero-txt">
<p class="kicker kicker-light">Serruriers francophones aux États-Unis</p>
<h1>Porte claquée, clé perdue ? <em>On vous rouvre, en français.</em></h1>
<p class="lead">Nous sommes des serruriers qui travaillent en français pour les francophones qui vivent aux États-Unis. Maison, voiture, commerce ou coffre-fort, on vous explique ce qu'on va faire et combien ça coûte avant de commencer.</p>
<div class="ctas">{phone_cta()}<a class="btn btn-ghost-light" href="/services/">Voir nos 30 services</a></div>
</div>
<div class="hero-art" aria-hidden="true"><div class="cyl"><div class="plug"></div>{pins}<div class="hkey"></div></div><p class="cyl-cap">Cinq goupilles, une seule bonne clé.</p></div>
</div></section>
<section class="intro"><div class="wrap narrow prose">
<h2>Un serrurier qui comprend ce que vous dites</h2>
<p>Vous habitez à Miami, Boston, Houston ou dans un petit coin du Maine, et le jour où la clé casse dans la serrure, vous n'avez pas envie de chercher le mot anglais pour « gâche » ou « cylindre ». C'est pour ça qu'on existe.</p>
<p>Notre équipe parle français au téléphone et sur place. On ouvre les portes sans les abîmer quand c'est possible, on change ou on rekeye les serrures, on refait les clés de voiture modernes et on sécurise les commerces.</p>
<p>Et quand une intervention ne sert à rien, on vous le dit. Une serrure qui force un peu se règle souvent en dix minutes, sans rien remplacer.</p>
</div></section>
<section class="cats"><div class="wrap"><h2 class="sec-t">Ce qu'on fait pour vous</h2><div class="cat-grid">{cats}</div></div></section>
<section class="how"><div class="wrap"><h2 class="sec-t">Comment on travaille</h2><ol class="how-l">
<li><span class="sn">01</span><h3>Vous nous décrivez la situation</h3><p>Type de porte, marque de la serrure si vous la voyez, modèle de la voiture. Une photo aide beaucoup.</p></li>
<li><span class="sn">02</span><h3>On vous donne un prix et un délai</h3><p>Avant de partir, pas après. Si quelque chose change sur place, on vous demande votre accord.</p></li>
<li><span class="sn">03</span><h3>On vérifie, puis on intervient</h3><p>Pièce d'identité et justificatif d'abord. Ensuite, on choisit la méthode la moins destructive.</p></li>
<li><span class="sn">04</span><h3>On teste tout avec vous</h3><p>Chaque clé, chaque verrou, devant vous. Vous repartez en sachant comment tout fonctionne.</p></li>
</ol></div></section>
<section class="faq"><div class="wrap narrow"><h2>Questions fréquentes</h2>{faq_html}</div></section>
<section class="band"><div class="wrap band-in"><p>Bloqué dehors en ce moment ? Commencez par là.</p><a class="btn btn-brass" href="/serrurier-urgence/">Serrurier d'urgence 24 h/24</a></div></section>''' + footer(pages_by_cat)


def render_hub(pages_by_cat):
    blocks = ""
    for key, label, blurb in CATEGORIES:
        items = "".join(
            f'<li><a class="hub-card" href="/{p["slug"]}/">{icon_svg(p["icon"])}<span><strong>{esc(p["name"])}</strong><em>{esc(p["lead"])}</em></span></a></li>'
            for p in pages_by_cat[key])
        blocks += f'<section class="hub-sec"><h2>{esc(label)}</h2><p>{esc(blurb)}</p><ul class="hub-l">{items}</ul></section>'
    schema = [breadcrumb_ld([("Accueil", "/"), ("Services", "/services/")])]
    return head("Tous nos services de serrurerie en français", "La liste complète de nos services de serrurier aux États-Unis : maison, voiture, commerce, coffre-fort et urgence 24 h/24, expliqués en français.", "/services/", schema) + header(pages_by_cat) + f'''
<section class="svc-hero hub-hero"><div class="wrap"><nav class="crumbs" aria-label="Fil d'Ariane"><a href="/">Accueil</a><span>/</span><span aria-current="page">Services</span></nav><h1>Tous nos services de serrurerie</h1><p class="lead">Trente interventions que l'on fait chaque semaine, classées selon l'endroit où vous êtes bloqué.</p></div></section>
<div class="wrap hub">{blocks}</div>''' + footer(pages_by_cat)


def render_404(pages_by_cat):
    return head("Page introuvable", "Cette page n'existe pas ou a été déplacée.", "/404", []).replace(
        'content="index,follow,max-image-preview:large,max-snippet:-1"', 'content="noindex"') + header(pages_by_cat) + '''
<section class="svc-hero"><div class="wrap narrow"><p class="kicker">Erreur 404</p><h1>Cette porte-là ne mène nulle part</h1><p class="lead">La page que vous cherchez n'existe pas ou a changé d'adresse. Pas de panique, la suite est par ici.</p><div class="ctas"><a class="btn btn-rust" href="/services/">Voir nos services</a><a class="btn btn-ghost" href="/">Retour à l'accueil</a></div></div></section>''' + footer(pages_by_cat)


# ---------------------------------------------------------------------------
def main():
    pages = load_pages()
    by_slug = {p["slug"]: p for p in pages}
    pages_by_cat = {c[0]: [] for c in CATEGORIES}
    for p in pages:
        if p["icon"] not in ICONS:
            errors.append(f'{p["slug"]}: icône inconnue {p["icon"]}')
            continue
        pages_by_cat[p["category"]].append(p)
        raw = (ROOT / "content" / "pages" / p["file"]).read_text(encoding="utf-8")
        if "—" in raw or "–" in raw:
            errors.append(f'{p["slug"]}: tiret long ou demi-cadratin interdit')
        low = raw.lower()
        for b in BANNED:
            if b in low:
                warnings.append(f'{p["slug"]}: expression à éviter « {b} »')
        if len(p["title"]) > 62:
            warnings.append(f'{p["slug"]}: title trop long ({len(p["title"])})')
        if not 120 <= len(p["description"]) <= 165:
            warnings.append(f'{p["slug"]}: description {len(p["description"])} caractères')
    for key in pages_by_cat:
        pages_by_cat[key].sort(key=lambda p: p.get("order", 99))
    if errors:
        print("ERREURS :\n  " + "\n  ".join(errors))
        sys.exit(1)

    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "fonts").mkdir(parents=True)
    shutil.copy(ROOT / "src" / "fraunces-600.woff2", OUT / "fonts" / "fraunces-600.woff2")
    shutil.copy(ROOT / "src" / "favicon.svg", OUT / "favicon.svg")

    def write(path, content):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(fr_typo(content), encoding="utf-8")

    write(OUT / "index.html", render_home(pages, pages_by_cat))
    write(OUT / "services" / "index.html", render_hub(pages_by_cat))
    write(OUT / "404.html", render_404(pages_by_cat))
    for p in pages:
        write(OUT / p["slug"] / "index.html", render_service(p, by_slug, pages_by_cat))
    if errors:
        print("ERREURS :\n  " + "\n  ".join(errors))
        sys.exit(1)

    base = CONFIG["site_url"].rstrip("/")
    urls = ["/", "/services/"] + [f'/{p["slug"]}/' for p in pages]
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"<url><loc>{base}{u}</loc></url>\n" for u in urls) + "</urlset>\n", encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {base}/sitemap.xml\n", encoding="utf-8")
    llms = [f"# {BRAND}", "", "> Serruriers francophones qui interviennent partout aux États-Unis, 24 h/24 : ouverture de porte, serrures, clés de voiture, commerces et coffres-forts. Tout le site est en français.", ""]
    for key, label, _ in CATEGORIES:
        llms.append(f"## {label}")
        llms += [f'- [{p["name"]}]({base}/{p["slug"]}/): {p["description"]}' for p in pages_by_cat[key]]
        llms.append("")
    (OUT / "llms.txt").write_text("\n".join(llms), encoding="utf-8")

    total = sum(p["words"] for p in pages)
    print(f"OK : {len(pages)} pages de service, {total} mots au total.")
    if warnings:
        print("AVERTISSEMENTS :\n  " + "\n  ".join(warnings))


if __name__ == "__main__":
    main()
