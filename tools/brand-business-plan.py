import re, html, base64, sys
MD="/Users/nancytorvund/alpha-hour/BUSINESS-PLAN.md"; OUT="/Users/nancytorvund/alpha-hour/business-plan.html"
LOGO=base64.b64encode(open("/Users/nancytorvund/alpha-application/alpha-application-main/public/alpha-logo.webp","rb").read()).decode()
src=open(MD,encoding="utf-8").read().split("\n")
# ---- parse ----
blocks=[]; para=[]; i=0
def flush():
    global para
    if para: blocks.append(("p"," ".join(para))); para=[]
while i<len(src):
    l=src[i]
    if l.startswith("# "): flush(); i+=1; continue
    m=re.match(r"^(#{2,3}) (.*)$",l)
    if m: flush(); blocks.append(("h2" if len(m.group(1))==2 else "h3", m.group(2).strip())); i+=1; continue
    if l.startswith("|"):
        flush(); rows=[]
        while i<len(src) and src[i].startswith("|"):
            cells=[c.strip() for c in src[i].strip().strip("|").split("|")]
            if not all(re.fullmatch(r"-+",c) for c in cells): rows.append(cells)
            i+=1
        blocks.append(("table",rows)); continue
    m=re.match(r"^(-|\d+\.) (.*)$",l)
    if m:
        flush(); kind="ul" if m.group(1)=="-" else "ol"; items=[]
        while i<len(src) and re.match(r"^(-|\d+\.) ",src[i]): items.append(re.sub(r"^(-|\d+\.) ","",src[i]).strip()); i+=1
        blocks.append((kind,items)); continue
    if l.strip() in ("","---"): flush(); i+=1; continue
    if l.startswith("**Prepared by:**") or l.startswith("**Date:**") or l.startswith("**Status:**"): i+=1; continue
    if l.startswith("*Sources:"): flush(); blocks.append(("sources",l.strip("*"))); i+=1; continue
    para.append(l.strip()); i+=1
flush()
def inl(t):
    t=html.escape(t,quote=False); t=re.sub(r"\*\*(.+?)\*\*",r"<strong>\1</strong>",t); return t
NUM=re.compile(r"^[\$\d\-,\.%KM\s/x]+$")
def is_num(c): return bool(c) and (c[0] in "$0123456789" or c.endswith("%")) and bool(NUM.match(c.replace("**","")))
TOTAL=re.compile(r"^\**(Launch total|Expanded total|Total|Net|Site profit|Fixed cost per campus|Variable cost per child|Contribution|Year 1 total)")
out=[]
out.append(f'''<title>Alpha Hours: Business Plan</title>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600;9..40,700&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
:root{{--blue:#0000ED;--blue-deep:#0000B8;--blue-soft:#EEF0FF;--blue-line:#C9CDFF;--ink:#0B1020;--ink-2:#3A4160;--muted:#6B7290;--line:#E3E6EF;--paper:#FFFFFF;--bg:#F7F8FC;}}
*{{box-sizing:border-box}}
html{{background:var(--bg)}}
body{{margin:0;background:var(--bg);color:var(--ink);font-family:"DM Sans",system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;font-size:15.5px;line-height:1.6;-webkit-font-smoothing:antialiased;font-feature-settings:"tnum" 1}}
.page{{max-width:900px;margin:0 auto;background:var(--paper);box-shadow:0 1px 0 var(--line),0 24px 60px -30px rgba(11,16,32,.25)}}
.cover{{padding:56px 64px 44px;border-bottom:6px solid var(--blue);position:relative;overflow:hidden}}
.cover .logo{{width:200px;height:auto;display:block;margin-bottom:44px}}
.cover .eyebrow{{font-family:"Space Mono",monospace;font-size:12px;letter-spacing:.22em;text-transform:uppercase;color:var(--blue);font-weight:700;margin:0 0 14px}}
.cover h1{{font-size:56px;line-height:1.02;letter-spacing:-.03em;font-weight:700;margin:0 0 10px;color:var(--ink)}}
.cover h1 span{{color:var(--blue)}}
.cover .sub{{font-size:22px;color:var(--ink-2);margin:0 0 30px;font-weight:500;letter-spacing:-.01em;max-width:640px;line-height:1.35}}
.cover .meta{{display:flex;gap:36px;flex-wrap:wrap;font-family:"Space Mono",monospace;font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:.12em}}
.cover .meta b{{display:block;color:var(--ink);font-family:"DM Sans",sans-serif;font-size:14px;text-transform:none;letter-spacing:0;font-weight:600;margin-top:4px}}
.cover .mark{{position:absolute;right:-40px;top:-30px;width:360px;opacity:.06;pointer-events:none}}
.glance{{padding:36px 64px 8px}}
.glance h2{{font-family:"Space Mono",monospace;font-size:12px;letter-spacing:.22em;text-transform:uppercase;color:var(--blue);margin:0 0 16px;border:0;padding:0}}
.cards{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}}
.card{{border:1px solid var(--line);border-top:3px solid var(--blue);border-radius:6px;padding:16px 18px 14px;background:#fff}}
.card .v{{font-family:"Space Mono",monospace;font-size:26px;font-weight:700;color:var(--blue);letter-spacing:-.02em;line-height:1.1}}
.card .l{{font-size:13px;color:var(--ink-2);margin-top:6px;line-height:1.35}}
.body{{padding:20px 64px 56px}}
h2{{font-size:28px;letter-spacing:-.02em;font-weight:700;margin:52px 0 14px;padding-top:26px;border-top:1px solid var(--line);color:var(--ink);line-height:1.15}}
h2 .n{{font-family:"Space Mono",monospace;font-size:13px;color:var(--blue);letter-spacing:.2em;display:block;margin-bottom:10px;font-weight:700}}
h3{{font-size:18px;font-weight:700;margin:30px 0 8px;color:var(--ink);letter-spacing:-.01em}}
p{{margin:0 0 14px;color:var(--ink)}}
strong{{font-weight:700}}
ul,ol{{margin:0 0 16px;padding-left:22px}} li{{margin-bottom:7px}} li::marker{{color:var(--blue);font-weight:700}}
.tbl{{overflow-x:auto;margin:8px 0 22px;border:1px solid var(--line);border-radius:6px}}
table{{width:100%;border-collapse:collapse;font-size:13.5px}}
th{{background:var(--blue);color:#fff;text-align:left;padding:10px 12px;font-weight:600;font-size:12.5px;letter-spacing:.02em;vertical-align:bottom}}
td{{padding:9px 12px;border-top:1px solid var(--line);vertical-align:top}}
tbody tr:nth-child(even) td{{background:#FAFBFE}}
td.num,th.num{{text-align:right;font-family:"Space Mono",monospace;font-size:12.5px;white-space:nowrap}}
tr.total td{{background:var(--blue-soft)!important;font-weight:700;border-top:2px solid var(--blue-line)}}
.callout{{background:var(--blue);color:#fff;border-radius:8px;padding:26px 30px;margin:36px 0 10px;font-size:20px;line-height:1.4;font-weight:500;letter-spacing:-.01em}}
.callout .k{{font-family:"Space Mono",monospace;font-size:11px;letter-spacing:.22em;text-transform:uppercase;opacity:.75;display:block;margin-bottom:10px}}
.sources{{margin-top:40px;padding-top:16px;border-top:1px solid var(--line);font-size:12.5px;color:var(--muted);line-height:1.5}}
.foot{{padding:18px 64px 28px;border-top:1px solid var(--line);display:flex;justify-content:space-between;font-family:"Space Mono",monospace;font-size:11px;color:var(--muted);letter-spacing:.1em;text-transform:uppercase}}
@media (max-width:720px){{.cover,.glance,.body,.foot{{padding-left:22px;padding-right:22px}}.cover h1{{font-size:40px}}.cards{{grid-template-columns:1fr 1fr}}}}
@media print{{html,body{{background:#fff}}.page{{box-shadow:none;max-width:none}}.cover{{padding:40px 0 30px}}.glance,.body{{padding-left:0;padding-right:0}}.foot{{padding-left:0;padding-right:0}}h2{{page-break-after:avoid}}h3{{page-break-after:avoid}}.tbl,.card,.callout{{page-break-inside:avoid}}table{{font-size:12px}}.cover .mark{{display:none}}a{{color:inherit;text-decoration:none}}}}
@page{{margin:16mm 16mm 18mm}}
</style>
<div class="page">
<header class="cover">
  <img class="mark" src="data:image/webp;base64,{LOGO}" alt="">
  <img class="logo" src="data:image/webp;base64,{LOGO}" alt="Alpha">
  <p class="eyebrow">Business plan</p>
  <h1>Alpha <span>Hours</span></h1>
  <p class="sub">The Alpha day, after school. A premium after-school business inside Alpha buildings, built for the families who will never enroll at Alpha.</p>
  <div class="meta"><div>Prepared by<b>Nancy Wisniewski Torvund, proposed Head of Alpha Hours</b></div><div>Date<b>August 27, 2026</b></div><div>Status<b>Draft for review</b></div></div>
</header>
<section class="glance">
  <h2>At a glance</h2>
  <div class="cards">
    <div class="card"><div class="v">$4,500</div><div class="l">per seven-week session, five sessions a year. $22,500 a year, about a third of Alpha tuition.</div></div>
    <div class="card"><div class="v">6 campuses</div><div class="l">New York (2), Greenwich, Boston (2), Chicago. Session 2 launch, October 19, 2026.</div></div>
    <div class="card"><div class="v">$78M</div><div class="l">revenue run rate at capacity from January 2027, on 867 seats and 3,468 enrolled.</div></div>
    <div class="card"><div class="v">$37.3M</div><div class="l">Year 1 net on the plan case (60 to 100 percent fill across four sessions).</div></div>
    <div class="card"><div class="v">83%</div><div class="l">site margin at capacity. Guides hired to sold seats; fixed cost $188K a campus.</div></div>
    <div class="card"><div class="v">15 students</div><div class="l">break-even per campus, about four per cohort. Profitable at zero conversions.</div></div>
  </div>
</section>
<main class="body">''')
n=0
for kind,val in blocks:
    if kind=="h2":
        m=re.match(r"^(\d+)\.\s+(.*)$",val)
        if m: n=int(m.group(1)); out.append(f'<h2><span class="n">{n:02d}</span>{inl(m.group(2))}</h2>')
        else: out.append(f"<h2>{inl(val)}</h2>")
    elif kind=="h3": out.append(f"<h3>{inl(val)}</h3>")
    elif kind=="p":
        if val.startswith("Alpha Hours turns empty Alpha buildings into a profitable"):
            out.append(f'<div class="callout"><span class="k">The one-sentence case</span>{inl(val)}</div>')
        else: out.append(f"<p>{inl(val)}</p>")
    elif kind in ("ul","ol"): out.append(f"<{kind}>"+"".join(f"<li>{inl(x)}</li>" for x in val)+f"</{kind}>")
    elif kind=="sources": out.append(f'<p class="sources">{inl(val)}</p>')
    elif kind=="table":
        hdr,body=val[0],val[1:]
        numcols=[all(is_num(r[c].strip("*")) or r[c]=="" for r in body if c<len(r)) and any(is_num(r[c].strip("*")) for r in body if c<len(r)) for c in range(len(hdr))]
        h="".join(f'<th class="{"num" if numcols[c] else ""}">{inl(x)}</th>' for c,x in enumerate(hdr))
        rows=[]
        for r in body:
            cls=' class="total"' if TOTAL.match(r[0]) else ""
            rows.append(f"<tr{cls}>"+"".join(f'<td class="{"num" if c<len(numcols) and numcols[c] else ""}">{inl(x.strip("*"))}</td>' for c,x in enumerate(r))+"</tr>")
        out.append(f'<div class="tbl"><table><thead><tr>{h}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>')
out.append('''</main>
<footer class="foot"><span>Alpha Hours · Business plan</span><span>August 27, 2026 · Confidential draft</span></footer>
</div>''')
open(OUT,"w",encoding="utf-8").write("\n".join(out)); print("html written", len("\n".join(out)))
