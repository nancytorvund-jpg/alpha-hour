"""Google-Docs-friendly HTML for each Alpha Hours document.

Google Drive converts HTML into a Google Doc, keeping inline colors, fonts that exist in Google Fonts,
table cell fills and remote images. It drops CSS grid/flex, data URIs and most class-based layout, so
this generator emits plain, inline-styled HTML with tables for cards and callouts.

Usage: python3 tools/gdoc.py plan|brainlift|financials|ask|onepager|all  -> writes gdoc-<key>.html into the scratchpad dir
"""
import re, html, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from brand import parse, plain, DOCS, DATE, ROOT, is_num, TOTAL
OUT_DIR = os.environ.get("GDOC_OUT", "/private/tmp/claude-501/-Users-nancytorvund/feceb8c1-fb3f-4825-aa0e-4efcfbaa183d/scratchpad")
LOGO_URL = "https://apply.alpha.school/icon-512.png"
BLUE = "#0000ED"; INK = "#0B1020"; INK2 = "#3A4160"; MUTED = "#6B7290"; LINE = "#E3E6EF"; SOFT = "#EEF0FF"
SANS = "font-family:'DM Sans'"; MONO = "font-family:'Space Mono'"

def inl(t, size="10.5pt", color=INK, bold=False):
    t = html.escape(t, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    return f'<span style="{SANS};font-size:{size};color:{color}{";font-weight:bold" if bold else ""}">{t}</span>'
def bold_html(t): return re.sub(r"[*][*](.+?)[*][*]", r"<b>\1</b>", html.escape(t, quote=False))
def p(t, size="10.5pt", color=INK, bold=False, margin="0 0 7pt 0"):
    t2 = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", html.escape(t, quote=False))
    return f'<p style="{SANS};margin:{margin};font-size:{size};color:{color}{";font-weight:bold" if bold else ""}">{t2}</p>'
def eyebrow(t, size="8pt", margin="14pt 0 3pt 0", color=BLUE):
    return f'<p style="{MONO};margin:{margin};font-size:{size};color:{color};font-weight:bold;letter-spacing:2pt">{html.escape(t.upper())}</p>'
def h2(t, n=None):
    e = eyebrow(f"{n:02d}", margin="22pt 0 2pt 0") if n else ""
    return f'{e}<p style="{SANS};margin:{"0" if n else "22pt"} 0 6pt 0;font-size:19pt;color:{INK};font-weight:bold">{html.escape(t)}</p>'
def h3(t): return f'<p style="{SANS};margin:12pt 0 4pt 0;font-size:12.5pt;color:{INK};font-weight:bold">{html.escape(t)}</p>'
def rule(color=BLUE, h=3): return f'<table width="100%" border="0" cellspacing="0" cellpadding="0" style="margin:6pt 0"><tr><td style="border:none;border-bottom:{h}pt solid {color};font-size:2pt">&nbsp;</td></tr></table>'

def table(rows, size="9pt"):
    hdr, body = rows[0], rows[1:]
    ncol = len(hdr)
    numcols = [all(is_num(r[c].strip("*")) or r[c] == "" for r in body if c < len(r)) and any(is_num(r[c].strip("*")) for r in body if c < len(r)) for c in range(ncol)]
    out = ['<table width="100%" cellspacing="0" cellpadding="0" style="margin:4pt 0 10pt 0;border-collapse:collapse"><tr>']
    for c, x in enumerate(hdr):
        out.append(f'<th style="{SANS};background:{BLUE};color:#FFFFFF;padding:5pt 7pt;text-align:{"right" if numcols[c] else "left"};font-size:{size};font-weight:bold">{html.escape(plain(x))}</th>')
    out.append("</tr>")
    for i, r in enumerate(body):
        total = bool(TOTAL.match(r[0]))
        bg = SOFT if total else ("#FAFBFE" if i % 2 else "#FFFFFF")
        out.append("<tr>")
        for c in range(ncol):
            x = r[c].strip("*") if c < len(r) else ""
            font = MONO if numcols[c] else SANS
            cell_text = re.sub(r"[*][*](.+?)[*][*]", r"<b>\1</b>", html.escape(x))
            align = "right" if numcols[c] else "left"; weight = ";font-weight:bold" if total else ""
            out.append(f'<td style="{font};background:{bg};padding:4pt 7pt;border-bottom:1px solid {LINE};text-align:{align};vertical-align:top;font-size:{size};color:{INK}{weight}">{cell_text}</td>')
        out.append("</tr>")
    out.append("</table>")
    return "".join(out)

def cards(items, cols=3, vsize="15pt", lsize="8pt"):
    rows = [items[i:i + cols] for i in range(0, len(items), cols)]
    out = ['<table width="100%" border="0" cellspacing="6" cellpadding="0" style="margin:4pt 0 10pt 0">']
    for row in rows:
        out.append("<tr>")
        for v, l in row:
            out.append(f'<td width="{100 // cols}%" style="border:none;border-top:3pt solid {BLUE};background:#FFFFFF;padding:6pt 8pt;vertical-align:top"><p style="{MONO};margin:0 0 2pt 0;font-size:{vsize};color:{BLUE};font-weight:bold">{html.escape(v)}</p><p style="{SANS};margin:0;font-size:{lsize};color:{INK2}">{html.escape(l)}</p></td>')
        out.append("</tr>")
    out.append("</table>")
    return "".join(out)

def callout(label, text, size="12pt"):
    return f'<table width="100%" border="0" cellspacing="0" cellpadding="0" style="margin:10pt 0"><tr><td style="border:none;background:{BLUE};padding:12pt 14pt"><p style="{MONO};margin:0 0 4pt 0;font-size:7pt;color:#C9CDFF;letter-spacing:2pt">{html.escape(label.upper())}</p><p style="{SANS};margin:0;font-size:{size};color:#FFFFFF">{html.escape(plain(text))}</p></td></tr></table>'
def box(inner_html, bg=SOFT, border=None):
    b = f"border-left:4pt solid {BLUE};" if border == "left" else ""
    return f'<table width="100%" border="0" cellspacing="0" cellpadding="0" style="margin:6pt 0"><tr><td style="border:none;background:{bg};{b}padding:8pt 12pt">{inner_html}</td></tr></table>'


def compress(doc):
    """Replace repeated style attributes with classes; font-family stays inline because Google Docs ignores it in <style>."""
    classes = {}
    def sub(m):
        style = m.group(1)
        decls = [d.strip() for d in style.split(";") if d.strip()]
        fonts = [d for d in decls if d.startswith("font-family")]
        rest = ";".join(d for d in decls if not d.startswith("font-family"))
        parts = []
        if fonts: parts.append(f'style="{fonts[0]}"')
        if rest:
            if rest not in classes: classes[rest] = f"c{len(classes)}"
            parts.append(f'class="{classes[rest]}"')
        return " ".join(parts)
    body = re.sub(r'style="([^"]*)"', sub, doc)
    css = "".join(f".{v}{{{k}}}" for k, v in classes.items())
    return body.replace("</head>", f"<style>{css}</style></head>", 1)

def cover(cfg):
    return (f'<p style="margin:0 0 10pt 0"><img src="{LOGO_URL}" width="160"></p>'
            + eyebrow(cfg["eyebrow"], size="9pt", margin="0 0 4pt 0")
            + f'<p style="{SANS};margin:0 0 6pt 0;font-size:34pt;color:{INK};font-weight:bold">Alpha <span style="color:{BLUE}">Hours</span></p>'
            + p(cfg["sub"], "13pt", INK2, margin="0 0 10pt 0")
            + f'<p style="{SANS};margin:0 0 6pt 0;font-size:9.5pt;color:{INK}"><span style="font-size:7.5pt;color:{MUTED};letter-spacing:1.5pt">PREPARED BY</span> <b>Nancy Wisniewski Torvund, proposed Head of Alpha Hours</b> &nbsp;&nbsp; <span style="font-size:7.5pt;color:{MUTED};letter-spacing:1.5pt">DATE</span> <b>{cfg.get("date", DATE)}</b> &nbsp;&nbsp; <span style="font-size:7.5pt;color:{MUTED};letter-spacing:1.5pt">STATUS</span> <b>Draft for review</b></p>'
            + rule() + eyebrow("At a glance", margin="8pt 0 4pt 0") + cards(cfg["cards"]))

def build_doc(key):
    cfg = DOCS[key]; blocks = parse(os.path.join(ROOT, cfg["md"]))
    out = [f'<html><head><meta charset="utf-8"><title>{html.escape(cfg["title"])}</title></head><body style="{SANS};color:{INK}">', cover(cfg)]
    section = None; i = 0
    while i < len(blocks):
        kind, val = blocks[i]
        if kind == "h2":
            section = val
            if section == "Owner": i += 2; continue
            m = re.match(r"^(\d+)\.\s+(.*)$", val)
            out.append(rule(LINE, 1))
            out.append(h2(m.group(2), int(m.group(1))) if m else h2(val))
        elif kind == "h3":
            if section == "Spiky Points of View":
                m = re.match(r"^SPOV (\d+):\s*(.*)$", val); j = i + 1; body = []
                while j < len(blocks) and blocks[j][0] == "p": body.append(blocks[j][1]); j += 1
                inner = (eyebrow(f"SPOV {m.group(1)}", size="7.5pt", margin="0 0 2pt 0") if m else "") + p(m.group(2) if m else val, "12pt", INK, True, "0 0 4pt 0") + "".join(p(b, "10pt", INK2, margin="0 0 4pt 0") for b in body)
                out.append(box(inner, "#FFFFFF", "left")); i = j; continue
            if section == "Experts":
                j = i + 1; body = []
                while j < len(blocks) and blocks[j][0] == "p": body.append(plain(blocks[j][1])); j += 1
                why = re.sub(r"\s*Why follow:\s*", " ", " ".join(body)).strip()
                out.append(p(val, "11pt", INK, True, "8pt 0 2pt 0")); out.append(p(why, "10pt", INK2)); i = j; continue
            m = re.match(r"^Insight (\d+):\s*(.*)$", val)
            if m: out.append(eyebrow(f"Insight {m.group(1)}", margin="12pt 0 2pt 0")); out.append(p(m.group(2), "12.5pt", INK, True, "0 0 5pt 0")); i += 1; continue
            out.append(eyebrow(val, margin="12pt 0 4pt 0") if section == "Purpose" else h3(val))
        elif kind == "p":
            if cfg["callout"] and val.startswith(cfg["callout"]): out.append(callout(cfg.get("callout_label", "The one-sentence case"), val))
            elif section == "Knowledge Tree" and re.match(r"^(Summary|Insights):", val): out.append(p(val, "10.5pt", INK2))
            else: out.append(p(val))
        elif kind in ("ul", "ol"):
            out.append(f"<{kind}>" + "".join(f'<li style="{SANS};margin:0 0 3pt 0;font-size:10.5pt;color:{INK}">{bold_html(x)}</li>' for x in val) + f"</{kind}>")
        elif kind == "sources": out.append(p(val, "8.5pt", MUTED, margin="14pt 0 4pt 0"))
        elif kind == "table": out.append(table(val))
        i += 1
    out.append(p("Alpha's learning-speed and test-score figures cited throughout are Alpha's own internal data and are not independently audited.", "8.5pt", MUTED, margin="14pt 0 0 0"))
    out.append("</body></html>")
    path = os.path.join(OUT_DIR, f"gdoc-{key}.html"); doc = compress("\n".join(out)); open(path, "w", encoding="utf-8").write(doc); print("wrote", path, len(doc))

def build_onepager():
    blocks = parse(os.path.join(ROOT, "EXECUTIVE-ONE-PAGER.md"))
    secs, cur, lead = {}, None, []
    for kind, val in blocks:
        if kind == "h3": cur = val; secs[cur] = []
        elif cur is None: lead.append((kind, val))
        else: secs[cur].append((kind, val))
    def sec(name, size="8.8pt"):
        out = [eyebrow(name, size="7pt", margin="8pt 0 2pt 0")]
        for kind, val in secs[name]:
            if kind == "p": out.append(p(val, size, margin="0 0 4pt 0"))
            elif kind == "ul": out.append("<ul style=\"margin:0 0 4pt 0\">" + "".join(f'<li style="{SANS};margin:0 0 2pt 0;font-size:{size};color:{INK}">{bold_html(x)}</li>' for x in val) + "</ul>")
            elif kind == "table": out.append(table(val, "7.8pt"))
        return "".join(out)
    stats = [("$4,500", "a session, $22,500 a year, about a third of Alpha tuition"), ("NYC first", "Oct 19, 2026; Greenwich and Boston S3; Chicago and Florida S4; national Fall 2027"),
             ("$101M", "run rate at capacity from Session 4, nine campuses"), ("$28.2M", "Year 1 net on the plan case, $39.9M at capacity"),
             ("83%", "site margin at capacity, break-even 15 students a campus"), ("11,908", "children on Timeback after school at network capacity")]
    left = sec("The idea") + sec("How it runs") + sec("Who pays") + sec("The market")
    right = sec("The numbers") + sec("The rollout") + sec("Toward a billion kids") + sec("The team") + callout("The one-sentence case", secs["The one-sentence case"][0][1], "9.5pt") + box(eyebrow("The ask", size="7pt", margin="0 0 2pt 0") + p(plain(secs["The ask"][0][1]), "9pt", margin="0"))
    doc = (f'<html><head><meta charset="utf-8"><title>Alpha Hours: Executive One-Pager</title></head><body style="{SANS};color:{INK}">'
           f'<table width="100%" border="0" cellspacing="0" cellpadding="0"><tr><td style="border:none;vertical-align:top"><p style="margin:0 0 4pt 0"><img src="{LOGO_URL}" width="110"></p>'
           + eyebrow("Executive one-pager", size="7.5pt", margin="6pt 0 2pt 0")
           + f'<p style="{SANS};margin:0;font-size:24pt;color:{INK};font-weight:bold">Alpha <span style="color:{BLUE}">Hours</span></p>'
           + p(plain(lead[0][1]), "10.5pt", INK2, margin="3pt 0 0 0")
           + f'</td><td style="border:none;vertical-align:top;text-align:right;width:30%">' + eyebrow("Prepared by", size="7pt", margin="0", color=MUTED) + p("Nancy Wisniewski Torvund", "9pt", INK, True, "0") + eyebrow("Proposed Head of Alpha Hours", size="7pt", margin="0", color=MUTED) + p(DATE, "9pt", INK, True, "0") + '</td></tr></table>'
           + rule() + cards(stats, 6, "11pt", "6.8pt")
           + f'<table width="100%" border="0" cellspacing="0" cellpadding="0"><tr><td width="50%" style="border:none;vertical-align:top;padding-right:10pt">{left}</td><td width="50%" style="border:none;vertical-align:top;padding-left:10pt">{right}</td></tr></table>'
           + "</body></html>")
    path = os.path.join(OUT_DIR, "gdoc-onepager.html"); doc = compress(doc); open(path, "w", encoding="utf-8").write(doc); print("wrote", path, len(doc))

if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    for k in (list(DOCS) + ["onepager"] if what == "all" else [what]):
        build_onepager() if k == "onepager" else build_doc(k)
