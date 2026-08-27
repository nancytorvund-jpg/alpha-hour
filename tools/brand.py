"""Alpha-branded HTML for every Alpha Hours document.

Usage: python3 tools/brand.py plan|brainlift|financials|onepager|all
Reads the markdown source, writes the html next to it. PDFs are made from the html by tools/pdf.sh.
"""
import re, html, base64, sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGO = base64.b64encode(open("/Users/nancytorvund/alpha-application/alpha-application-main/public/alpha-logo.webp", "rb").read()).decode()
DATE = "August 27, 2026"

DOCS = {
    "plan": dict(md="BUSINESS-PLAN.md", out="business-plan.html", title="Alpha Hours: Business Plan", eyebrow="Business plan",
                 sub="The Alpha day, after school. A premium after-school business inside Alpha buildings, built for the families who will never enroll at Alpha.",
                 cards=[("$4,500", "per seven-week session, five sessions a year. $22,500 a year, about a third of Alpha tuition."),
                        ("New York first", "Session 2, October 19, 2026. Greenwich and Boston in Session 3, Chicago and Florida in Session 4, national Fall 2027."),
                        ("$101M", "revenue run rate at capacity from Session 4, nine campuses, 1,127 seats, 4,508 enrolled."),
                        ("$28.2M", "Year 1 net on the plan case, leaving Session 5 at an $82M run rate."),
                        ("83%", "site margin at capacity. Guides hired to sold seats; fixed cost $188K a campus."),
                        ("15 students", "break-even per campus, about four per cohort. Profitable at zero conversions.")],
                 callout="Alpha Hours turns empty Alpha buildings into a profitable", foot="Business plan"),
    "brainlift": dict(md="BRAINLIFT.md", out="brainlift.html", title="Alpha Hours: BrainLift", eyebrow="BrainLift",
                 sub="Purpose, experts, spiky points of view, insights, knowledge tree, business model, financials and rollout for a profitable after-school business unit inside Alpha buildings.",
                 cards=[("70%", "of every room is families who will never enroll at Alpha. They are the business, not a leak."),
                        ("4 children", "on every seat after 3:30, six with the evening block, in buildings Alpha already pays for."),
                        ("$40B", "a year of US tutoring and after-school spend, almost none of it from families shopping for a school."),
                        ("$101M", "revenue run rate at capacity from Session 4 on the nine-campus pilot."),
                        ("11,908", "children on Timeback after school at full-network capacity, more than Alpha enrolls full-time."),
                        ("8 SPOVs", "one owner, one P&L, one number the Head is held to.")],
                 callout=None, foot="BrainLift"),
    "financials": dict(md="FINANCIALS.md", out="financials.html", title="Alpha Hours: Financials", eyebrow="Financials",
                 sub="Unit economics, per-campus P&L, Year 1 by session in three cases, lanes, launch budget, cash timing, sensitivities, the national build and the feeder. One model behind every number.",
                 cards=[("$35.4M", "Year 1 revenue on the plan case, each campus at 60 / 75 / 90 / 100 percent by its own session count."),
                        ("$28.2M", "Year 1 net after the central team. Capacity $39.9M, floor $8.6M."),
                        ("$20,325", "contribution per child per year before guides, $19,075 after."),
                        ("$141K", "New York launch budget, covered by Session 2 deposits alone."),
                        ("15 students", "break-even per campus. Maximum downside at any site is seven weeks of payroll."),
                        ("$268M", "full-network revenue at capacity, about $216M net, 1.7 percent of the serviceable market.")],
                 callout=None, foot="Financials"),
}

# ---------------- markdown parser ----------------
def parse(path):
    src = open(path, encoding="utf-8").read().split("\n")
    blocks, para, i = [], [], 0
    def flush():
        nonlocal para
        if para: blocks.append(("p", " ".join(para))); para = []
    while i < len(src):
        l = src[i]
        if l.startswith("# "): flush(); i += 1; continue
        m = re.match(r"^(#{2,3}) (.*)$", l)
        if m: flush(); blocks.append(("h2" if len(m.group(1)) == 2 else "h3", m.group(2).strip())); i += 1; continue
        if l.startswith("|"):
            flush(); rows = []
            while i < len(src) and src[i].startswith("|"):
                cells = [c.strip() for c in src[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r"-+", c) for c in cells): rows.append(cells)
                i += 1
            blocks.append(("table", rows)); continue
        m = re.match(r"^(-|\d+\.) (.*)$", l)
        if m:
            flush(); kind = "ul" if m.group(1) == "-" else "ol"; items = []
            while i < len(src) and re.match(r"^(-|\d+\.) ", src[i]): items.append(re.sub(r"^(-|\d+\.) ", "", src[i]).strip()); i += 1
            blocks.append((kind, items)); continue
        if l.strip() in ("", "---"): flush(); i += 1; continue
        if l.startswith("**Prepared by:**") or l.startswith("**Date:**") or l.startswith("**Status:**") or l.startswith("Prepared by "): i += 1; continue
        if l.startswith("*Sources:"): flush(); blocks.append(("sources", l.strip("*"))); i += 1; continue
        para.append(l.strip()); i += 1
    flush()
    return blocks

def inl(t):
    t = html.escape(t, quote=False)
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
def plain(t): return re.sub(r"\*\*(.+?)\*\*", r"\1", t)
NUM = re.compile(r"^[\$\d\-,\.%KM\s/x()]+$")
def is_num(c): return bool(c) and (c[0] in "$0123456789" or c.endswith("%")) and bool(NUM.match(c.replace("**", "")))
TOTAL = re.compile(r"^\**(Launch total|Expanded total|Total|Net$|Net\b|Site profit$|Fixed cost per campus|Variable cost per child|Variable cost$|Contribution|Year 1 total|Full network)")

def table_html(rows, compact=False):
    hdr, body = rows[0], rows[1:]
    numcols = [all(is_num(r[c].strip("*")) or r[c] == "" for r in body if c < len(r)) and any(is_num(r[c].strip("*")) for r in body if c < len(r)) for c in range(len(hdr))]
    h = "".join(f'<th class="{"num" if numcols[c] else ""}">{inl(x)}</th>' for c, x in enumerate(hdr))
    out = []
    for r in body:
        cls = ' class="total"' if TOTAL.match(r[0]) else ""
        out.append(f"<tr{cls}>" + "".join(f'<td class="{"num" if c < len(numcols) and numcols[c] else ""}">{inl(x.strip("*"))}</td>' for c, x in enumerate(r)) + "</tr>")
    return f'<div class="tbl"><table><thead><tr>{h}</tr></thead><tbody>{"".join(out)}</tbody></table></div>'

# ---------------- shared style ----------------
STYLE = """
:root{--blue:#0000ED;--blue-deep:#0000B8;--blue-soft:#EEF0FF;--blue-line:#C9CDFF;--ink:#0B1020;--ink-2:#3A4160;--muted:#6B7290;--line:#E3E6EF;--paper:#FFFFFF;--bg:#F7F8FC;}
*{box-sizing:border-box}
html{background:var(--bg)}
body{margin:0;background:var(--bg);color:var(--ink);font-family:"DM Sans",system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;font-size:15.5px;line-height:1.6;-webkit-font-smoothing:antialiased;font-feature-settings:"tnum" 1}
.page{max-width:900px;margin:0 auto;background:var(--paper);box-shadow:0 1px 0 var(--line),0 24px 60px -30px rgba(11,16,32,.25)}
.cover{padding:56px 64px 44px;border-bottom:6px solid var(--blue);position:relative;overflow:hidden}
.cover .logo{width:200px;height:auto;display:block;margin-bottom:44px}
.cover .eyebrow{font-family:"Space Mono",monospace;font-size:12px;letter-spacing:.22em;text-transform:uppercase;color:var(--blue);font-weight:700;margin:0 0 14px}
.cover h1{font-size:56px;line-height:1.02;letter-spacing:-.03em;font-weight:700;margin:0 0 10px;color:var(--ink)}
.cover h1 span{color:var(--blue)}
.cover .sub{font-size:22px;color:var(--ink-2);margin:0 0 30px;font-weight:500;letter-spacing:-.01em;max-width:640px;line-height:1.35}
.cover .meta{display:flex;gap:36px;flex-wrap:wrap;font-family:"Space Mono",monospace;font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:.12em}
.cover .meta b{display:block;color:var(--ink);font-family:"DM Sans",sans-serif;font-size:14px;text-transform:none;letter-spacing:0;font-weight:600;margin-top:4px}
.cover .mark{position:absolute;right:-40px;top:-30px;width:360px;opacity:.06;pointer-events:none}
.glance{padding:36px 64px 8px}
.glance h2{font-family:"Space Mono",monospace;font-size:12px;letter-spacing:.22em;text-transform:uppercase;color:var(--blue);margin:0 0 16px;border:0;padding:0}
.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.card{border:1px solid var(--line);border-top:3px solid var(--blue);border-radius:6px;padding:16px 18px 14px;background:#fff}
.card .v{font-family:"Space Mono",monospace;font-size:26px;font-weight:700;color:var(--blue);letter-spacing:-.02em;line-height:1.1}
.card .l{font-size:13px;color:var(--ink-2);margin-top:6px;line-height:1.35}
.body{padding:20px 64px 56px}
h2{font-size:28px;letter-spacing:-.02em;font-weight:700;margin:52px 0 14px;padding-top:26px;border-top:1px solid var(--line);color:var(--ink);line-height:1.15}
h2 .n{font-family:"Space Mono",monospace;font-size:13px;color:var(--blue);letter-spacing:.2em;display:block;margin-bottom:10px;font-weight:700}
h3{font-size:18px;font-weight:700;margin:30px 0 8px;color:var(--ink);letter-spacing:-.01em}
h4{font-family:"Space Mono",monospace;font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:var(--blue);margin:26px 0 6px}
p{margin:0 0 14px;color:var(--ink)}
strong{font-weight:700}
ul,ol{margin:0 0 16px;padding-left:22px} li{margin-bottom:7px} li::marker{color:var(--blue);font-weight:700}
.tbl{overflow-x:auto;margin:8px 0 22px;border:1px solid var(--line);border-radius:6px}
table{width:100%;border-collapse:collapse;font-size:13.5px}
th{background:var(--blue);color:#fff;text-align:left;padding:10px 12px;font-weight:600;font-size:12.5px;letter-spacing:.02em;vertical-align:bottom}
td{padding:9px 12px;border-top:1px solid var(--line);vertical-align:top}
tbody tr:nth-child(even) td{background:#FAFBFE}
td.num,th.num{text-align:right;font-family:"Space Mono",monospace;font-size:12.5px;white-space:nowrap}
tr.total td{background:var(--blue-soft)!important;font-weight:700;border-top:2px solid var(--blue-line)}
.callout{background:var(--blue);color:#fff;border-radius:8px;padding:26px 30px;margin:36px 0 10px;font-size:20px;line-height:1.4;font-weight:500;letter-spacing:-.01em}
.callout .k{font-family:"Space Mono",monospace;font-size:11px;letter-spacing:.22em;text-transform:uppercase;opacity:.75;display:block;margin-bottom:10px}
.spov{border:1px solid var(--line);border-left:4px solid var(--blue);border-radius:6px;padding:18px 22px 14px;margin:0 0 14px;background:#fff}
.spov .t{font-size:17px;font-weight:700;margin:0 0 8px;color:var(--ink);letter-spacing:-.01em;line-height:1.3}
.spov .t .n{font-family:"Space Mono",monospace;font-size:11px;letter-spacing:.2em;color:var(--blue);display:block;margin-bottom:6px}
.spov p{margin:0 0 6px;font-size:14.5px;color:var(--ink-2)}
.exp{margin:0 0 18px;padding-left:16px;border-left:2px solid var(--blue-line)}
.exp .name{font-weight:700;margin:0 0 4px}
.exp .why{color:var(--ink-2);font-size:14.5px;margin:0}
.lead{color:var(--ink-2)}
.sources{margin-top:40px;padding-top:16px;border-top:1px solid var(--line);font-size:12.5px;color:var(--muted);line-height:1.5}
.foot{padding:18px 64px 28px;border-top:1px solid var(--line);display:flex;justify-content:space-between;font-family:"Space Mono",monospace;font-size:11px;color:var(--muted);letter-spacing:.1em;text-transform:uppercase}
@media (max-width:720px){.cover,.glance,.body,.foot{padding-left:22px;padding-right:22px}.cover h1{font-size:40px}.cards{grid-template-columns:1fr 1fr}}
@media print{html,body{background:#fff}.page{box-shadow:none;max-width:none}.cover{padding:40px 0 30px}.glance,.body{padding-left:0;padding-right:0}.foot{padding-left:0;padding-right:0}h2{page-break-after:avoid}h3{page-break-after:avoid}.tbl,.card,.callout,.spov{page-break-inside:avoid}table{font-size:12px}.cover .mark{display:none}a{color:inherit;text-decoration:none}}
@page{margin:16mm 16mm 18mm}
"""
HEAD = '''<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600;9..40,700&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">'''

def cover(cfg, h1="Alpha <span>Hours</span>"):
    return f'''<header class="cover">
  <img class="mark" src="data:image/webp;base64,{LOGO}" alt="">
  <img class="logo" src="data:image/webp;base64,{LOGO}" alt="Alpha">
  <p class="eyebrow">{cfg["eyebrow"]}</p>
  <h1>{h1}</h1>
  <p class="sub">{cfg["sub"]}</p>
  <div class="meta"><div>Prepared by<b>Nancy Wisniewski Torvund, proposed Head of Alpha Hours</b></div><div>Date<b>{DATE}</b></div><div>Status<b>Draft for review</b></div></div>
</header>
<section class="glance">
  <h2>At a glance</h2>
  <div class="cards">{"".join(f'<div class="card"><div class="v">{v}</div><div class="l">{l}</div></div>' for v, l in cfg["cards"])}</div>
</section>'''

def build_doc(key):
    cfg = DOCS[key]
    blocks = parse(os.path.join(ROOT, cfg["md"]))
    out = [f'<title>{cfg["title"]}</title>', HEAD, f"<style>{STYLE}</style>", '<div class="page">', cover(cfg), '<main class="body">']
    section = None; n = 0; spov_n = 0; exp_open = False
    i = 0
    while i < len(blocks):
        kind, val = blocks[i]
        if kind == "h2":
            section = val
            if section == "Owner": i += 2; continue
            m = re.match(r"^(\d+)\.\s+(.*)$", val)
            if m: n = int(m.group(1)); out.append(f'<h2><span class="n">{n:02d}</span>{inl(m.group(2))}</h2>')
            else: out.append(f"<h2>{inl(val)}</h2>")
        elif kind == "h3":
            if section == "Spiky Points of View":
                m = re.match(r"^SPOV (\d+):\s*(.*)$", val)
                body = []
                j = i + 1
                while j < len(blocks) and blocks[j][0] == "p": body.append(f"<p>{inl(blocks[j][1])}</p>"); j += 1
                t = f'<span class="n">SPOV {m.group(1)}</span>{inl(m.group(2))}' if m else inl(val)
                out.append(f'<div class="spov"><p class="t">{t}</p>{"".join(body)}</div>')
                i = j; continue
            if section == "Experts":
                body = []
                j = i + 1
                while j < len(blocks) and blocks[j][0] == "p": body.append(plain(blocks[j][1])); j += 1
                why = re.sub(r"\s*Why follow:\s*", " ", " ".join(body)).strip()
                out.append(f'<div class="exp"><p class="name">{inl(val)}</p><p class="why">{inl(why)}</p></div>')
                i = j; continue
            if section == "Insights":
                m = re.match(r"^Insight (\d+):\s*(.*)$", val)
                if m: out.append(f'<h3><span style="font-family:Space Mono,monospace;font-size:11px;letter-spacing:.2em;color:var(--blue);display:block;margin-bottom:4px">INSIGHT {m.group(1)}</span>{inl(m.group(2))}</h3>'); i += 1; continue
            tag = "h4" if section == "Purpose" else "h3"
            out.append(f"<{tag}>{inl(val)}</{tag}>")
        elif kind == "p":
            if cfg["callout"] and val.startswith(cfg["callout"]):
                out.append(f'<div class="callout"><span class="k">The one-sentence case</span>{inl(val)}</div>')
            elif section == "Knowledge Tree" and re.match(r"^(Summary|Insights):", val):
                out.append(f'<p class="lead">{inl(val)}</p>')
            else: out.append(f"<p>{inl(val)}</p>")
        elif kind in ("ul", "ol"): out.append(f"<{kind}>" + "".join(f"<li>{inl(x)}</li>" for x in val) + f"</{kind}>")
        elif kind == "sources": out.append(f'<p class="sources">{inl(val)}</p>')
        elif kind == "table": out.append(table_html(val))
        i += 1
    out.append(f'''<p class="sources">Alpha's learning-speed and test-score figures cited throughout are Alpha's own internal data and are not independently audited.</p></main>
<footer class="foot"><span>Alpha Hours · {cfg["foot"]}</span><span>{DATE} · Confidential draft</span></footer>
</div>''')
    path = os.path.join(ROOT, cfg["out"])
    open(path, "w", encoding="utf-8").write("\n".join(out)); print("wrote", cfg["out"], len("\n".join(out)))

# ---------------- one-pager: a single Letter page, two columns ----------------
ONE_STYLE = """
:root{--blue:#0000ED;--blue-soft:#EEF0FF;--blue-line:#C9CDFF;--ink:#0B1020;--ink-2:#3A4160;--muted:#6B7290;--line:#E3E6EF;--bg:#F7F8FC}
*{box-sizing:border-box}
html{background:var(--bg)}
body{margin:0;background:var(--bg);color:var(--ink);font-family:"DM Sans",system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;font-size:9.8px;line-height:1.34;-webkit-font-smoothing:antialiased;font-feature-settings:"tnum" 1}
.sheet{width:8.5in;min-height:11in;margin:24px auto;background:#fff;padding:.5in .55in .45in;box-shadow:0 1px 0 var(--line),0 24px 60px -30px rgba(11,16,32,.25);display:flex;flex-direction:column}
.top{display:flex;align-items:flex-start;justify-content:space-between;border-bottom:4px solid var(--blue);padding-bottom:9px;margin-bottom:10px}
.top .logo{width:110px;height:auto;display:block;margin-bottom:6px}
.top .eyebrow{font-family:"Space Mono",monospace;font-size:8.5px;letter-spacing:.22em;text-transform:uppercase;color:var(--blue);font-weight:700;margin:0 0 5px}
.top h1{font-size:28px;line-height:1;letter-spacing:-.03em;font-weight:700;margin:0 0 5px}
.top h1 span{color:var(--blue)}
.top .sub{font-size:12.5px;color:var(--ink-2);margin:0;font-weight:500;max-width:5.2in;line-height:1.3;letter-spacing:-.01em}
.top .meta{text-align:right;font-family:"Space Mono",monospace;font-size:8px;color:var(--muted);text-transform:uppercase;letter-spacing:.12em;line-height:1.5;padding-top:4px}
.top .meta b{display:block;color:var(--ink);font-family:"DM Sans",sans-serif;font-size:10px;text-transform:none;letter-spacing:0;font-weight:600}
.stats{display:grid;grid-template-columns:repeat(6,1fr);gap:7px;margin:0 0 9px}
.stat{border:1px solid var(--line);border-top:3px solid var(--blue);border-radius:4px;padding:6px 8px 5px}
.stat .v{font-family:"Space Mono",monospace;font-size:14.5px;font-weight:700;color:var(--blue);letter-spacing:-.02em;line-height:1.1;white-space:nowrap}
.stat .l{font-size:8.6px;color:var(--ink-2);margin-top:3px;line-height:1.25}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:0 22px;flex:1}
h3{font-family:"Space Mono",monospace;font-size:8.5px;letter-spacing:.2em;text-transform:uppercase;color:var(--blue);margin:7px 0 3px;padding-top:6px;border-top:1px solid var(--line)}
.cols > div > h3:first-child{border-top:0;padding-top:0;margin-top:0}
p{margin:0 0 5px}
strong{font-weight:700}
ul{margin:0 0 5px;padding-left:13px} li{margin-bottom:3px} li::marker{color:var(--blue);font-weight:700}
table{width:100%;border-collapse:collapse;font-size:9.4px;margin:2px 0 6px}
table td:first-child,table th:first-child{width:30%;white-space:normal}
table th.num{white-space:normal}
th{background:var(--blue);color:#fff;text-align:left;padding:4px 7px;font-weight:600;font-size:8.6px}
td{padding:4px 7px;border-bottom:1px solid var(--line);vertical-align:top}
td.num,th.num{text-align:right;font-family:"Space Mono",monospace;font-size:9px;white-space:nowrap}
.case{background:var(--blue);color:#fff;border-radius:5px;padding:8px 12px;margin:5px 0 5px;font-size:11px;line-height:1.35;font-weight:500}
.case .k{font-family:"Space Mono",monospace;font-size:7.5px;letter-spacing:.22em;text-transform:uppercase;opacity:.75;display:block;margin-bottom:3px}
.ask{border:1px solid var(--blue-line);background:var(--blue-soft);border-radius:5px;padding:8px 12px;margin-top:2px}
.ask h3{border:0;padding:0;margin:0 0 3px}
.foot{margin-top:auto;padding-top:8px;border-top:1px solid var(--line);display:flex;justify-content:space-between;font-family:"Space Mono",monospace;font-size:7.5px;color:var(--muted);letter-spacing:.1em;text-transform:uppercase}
@media print{html,body{background:#fff}.sheet{margin:0;box-shadow:none;width:auto;min-height:0;padding:0;height:auto}}
@page{size:Letter;margin:.4in .5in .35in}
"""

def build_onepager():
    blocks = parse(os.path.join(ROOT, "EXECUTIVE-ONE-PAGER.md"))
    # group by h3
    secs, cur, lead = {}, None, []
    for kind, val in blocks:
        if kind == "h3": cur = val; secs[cur] = []
        elif cur is None: lead.append((kind, val))
        else: secs[cur].append((kind, val))
    def render(name, drop_first_p=False):
        out = [f"<h3>{inl(name)}</h3>"]
        for kind, val in secs[name]:
            if kind == "p": out.append(f"<p>{inl(val)}</p>")
            elif kind == "ul": out.append("<ul>" + "".join(f"<li>{inl(x)}</li>" for x in val) + "</ul>")
            elif kind == "table": out.append(table_html(val).replace('<div class="tbl">', "").rsplit("</div>", 1)[0])
        return "\n".join(out)
    tagline = plain(lead[0][1]) if lead else ""
    stats = [("$4,500", "a session, $22,500 a year, about a third of Alpha tuition"),
             ("NYC first", "Oct 19, 2026; Greenwich and Boston S3; Chicago and Florida S4; national Fall 2027"),
             ("$101M", "run rate at capacity from Session 4, nine campuses"),
             ("$28.2M", "Year 1 net on the plan case, $39.9M at capacity"),
             ("83%", "site margin at capacity, break-even 15 students a campus"),
             ("11,908", "children on Timeback after school at full-network capacity")]
    left = "\n".join([render("The idea"), render("How it runs"), render("Who pays"), render("The market")])
    case = plain(secs["The one-sentence case"][0][1])
    ask = plain(secs["The ask"][0][1])
    right = "\n".join([render("The numbers"), render("The rollout"), render("Toward a billion kids"), render("The team"),
                       f'<div class="case"><span class="k">The one-sentence case</span>{inl(case)}</div>',
                       f'<div class="ask"><h3>The ask</h3><p style="margin:0">{inl(ask)}</p></div>'])
    doc = f'''<title>Alpha Hours: Executive One-Pager</title>
{HEAD}
<style>{ONE_STYLE}</style>
<div class="sheet">
<header class="top">
  <div>
    <img class="logo" src="data:image/webp;base64,{LOGO}" alt="Alpha">
    <p class="eyebrow">Executive one-pager</p>
    <h1>Alpha <span>Hours</span></h1>
    <p class="sub">{inl(tagline)}</p>
  </div>
  <div class="meta">Prepared by<b>Nancy Wisniewski Torvund</b>Proposed Head of Alpha Hours<b>{DATE}</b></div>
</header>
<div class="stats">{"".join(f'<div class="stat"><div class="v">{v}</div><div class="l">{l}</div></div>' for v, l in stats)}</div>
<div class="cols">
<div>
{left}
</div>
<div>
{right}
</div>
</div>
<footer class="foot"><span>Alpha Hours · Executive one-pager</span><span>{DATE} · Confidential draft</span></footer>
</div>'''
    open(os.path.join(ROOT, "one-pager.html"), "w", encoding="utf-8").write(doc); print("wrote one-pager.html", len(doc))

if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    keys = list(DOCS) + ["onepager"] if what == "all" else [what]
    for k in keys:
        build_onepager() if k == "onepager" else build_doc(k)
