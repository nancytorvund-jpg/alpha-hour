"""Generate brainlift.html, BRAINLIFT.opml, BRAINLIFT-workflowy.txt from BRAINLIFT.md."""
import re, html, sys
REV = "August 27, 2026 revision"
import os
MD=os.environ.get("MD","BRAINLIFT.md"); HTML=os.environ.get("HTML","brainlift.html"); H1=os.environ.get("H1","BrainLift"); OUTLINE=os.environ.get("OUTLINE","1")=="1"
src = open(MD, encoding="utf-8").read().split("\n")

# ---------- parse markdown into a tree ----------
# node: dict(kind, text, children) ; kinds: h1,h2,h3,p,ul,ol,table
root = {"kind": "h1", "text": "", "children": []}
stack = [root]
def cur(): return stack[-1]
def push(level, text):
    node = {"kind": f"h{level}", "text": text, "children": []}
    while len(stack) > level - 0 and stack[-1]["kind"] != "h1" and int(stack[-1]["kind"][1]) >= level:
        stack.pop()
    while len(stack) > 1 and int(stack[-1]["kind"][1]) >= level: stack.pop()
    stack[-1]["children"].append(node); stack.append(node)
i = 0
para = []
def flush():
    global para
    if para:
        cur()["children"].append({"kind": "p", "text": " ".join(para)}); para = []
while i < len(src):
    line = src[i]
    if line.startswith("# "): flush(); root["text"] = line[2:].strip(); i += 1; continue
    m = re.match(r"^(#{2,3}) (.*)$", line)
    if m: flush(); push(len(m.group(1)), m.group(2).strip()); i += 1; continue
    if line.startswith("|"):
        flush(); rows = []
        while i < len(src) and src[i].startswith("|"):
            cells = [c.strip() for c in src[i].strip().strip("|").split("|")]
            if not all(re.fullmatch(r"-+", c) for c in cells): rows.append(cells)
            i += 1
        cur()["children"].append({"kind": "table", "rows": rows}); continue
    m = re.match(r"^(-|\d+\.) (.*)$", line)
    if m:
        flush(); kind = "ul" if m.group(1) == "-" else "ol"; items = []
        while i < len(src) and re.match(r"^(-|\d+\.) ", src[i]):
            items.append(re.sub(r"^(-|\d+\.) ", "", src[i]).strip()); i += 1
        cur()["children"].append({"kind": kind, "items": items}); continue
    if line.strip() in ("", "---"): flush(); i += 1; continue
    para.append(line.strip()); i += 1
flush()

# ---------- inline ----------
def inline_html(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    return t
def plain(t): return re.sub(r"\*\*(.+?)\*\*", r"\1", t)

# ---------- HTML ----------
old = open("brainlift.html", encoding="utf-8").read()
style = old.split("</style>")[0] + "</style>"
if "table {" not in style:
    style = style.replace("</style>", """  table { width: 100%; border-collapse: collapse; margin: 6px 0 18px; font-size: 14px; }
  .tbl { overflow-x: auto; margin: 0 0 6px; }
  th, td { text-align: left; padding: 7px 10px; border-bottom: 1px solid var(--line); vertical-align: top; }
  th { font-size: 12.5px; letter-spacing: 0.04em; text-transform: uppercase; color: var(--muted); font-weight: 650; }
  td:nth-child(n+2):not(:last-child), th:nth-child(n+2):not(:last-child) { white-space: nowrap; }
  tr.total td { font-weight: 650; }
</style>""")
out = [style, "", '<div class="doc">', "", "  <header>", '    <p class="eyebrow">Alpha Hours</p>', f"    <h1>{H1}</h1>",
       f'    <p class="meta"><strong>Owner:</strong> Nancy Wisniewski Torvund &nbsp;&#183;&nbsp; {REV}</p>', "  </header>", ""]
def render_block(b, section):
    k = b["kind"]
    if k == "p":
        cls = ' class="lead"' if section == "Knowledge Tree" and re.match(r"^(Summary|Insights):", b["text"]) else ""
        return [f"  <p{cls}>{inline_html(b['text'])}</p>"]
    if k in ("ul", "ol"):
        return [f"  <{k}>"] + [f"    <li>{inline_html(x)}</li>" for x in b["items"]] + [f"  </{k}>"]
    if k == "table":
        hdr, body = b["rows"][0], b["rows"][1:]
        lines = ['  <div class="tbl"><table>', "    <thead><tr>" + "".join(f"<th>{inline_html(c)}</th>" for c in hdr) + "</tr></thead>", "    <tbody>"]
        for r in body:
            cls = ' class="total"' if re.match(r"^(Launch total|Expanded total|Year 1 total|Full network|Total|Net$|Site profit$|Variable cost$|Contribution)", r[0]) else ""
            lines.append(f"      <tr{cls}>" + "".join(f"<td>{inline_html(c)}</td>" for c in r) + "</tr>")
        return lines + ["    </tbody>", "  </table></div>"]
    return []
for sec in root["children"]:
    if sec["kind"] != "h2":
        out += render_block(sec, ""); continue
    if sec["text"] == "Owner": continue
    out.append(f"  <h2>{inline_html(sec['text'])}</h2>")
    for b in sec["children"]:
        if b["kind"] != "h3":
            out += render_block(b, sec["text"]); continue
        if sec["text"] == "Experts":
            why = " ".join(plain(c["text"]) for c in b["children"] if c["kind"] == "p")
            why = re.sub(r"\s*Why follow:\s*", " ", why).strip()
            out.append(f'  <div class="exp"><p class="name">{inline_html(b["text"])}</p><p class="why">{inline_html(why)}</p></div>')
        elif sec["text"] == "Spiky Points of View":
            body = " ".join(plain(c["text"]) for c in b["children"] if c["kind"] == "p")
            out.append(f'  <div class="spov"><p class="t">{inline_html(b["text"])}</p><p>{inline_html(body)}</p></div>')
        else:
            tag = "h4" if sec["text"] == "Purpose" else "h3"
            out.append(f"  <{tag}>{inline_html(b['text'])}</{tag}>")
            for c in b["children"]: out += render_block(c, sec["text"])
    out.append("")
out += ['  <p class="foot">Alpha\'s learning-speed and test-score figures are Alpha\'s own internal data and are not independently audited.</p>', "", "</div>", ""]
open(HTML, "w", encoding="utf-8").write("\n".join(out).replace("<title>Alpha Hours: BrainLift</title>", f"<title>Alpha Hours: {H1}</title>"))

# ---------- outline (opml + workflowy) ----------
if not OUTLINE: sys.exit(0)
def leaves(b):
    k = b["kind"]
    if k == "p": return [plain(b["text"])]
    if k in ("ul", "ol"): return [plain(x) for x in b["items"]]
    if k == "table":
        hdr = b["rows"][0]
        return [{"text": plain(r[0]), "kids": [{"text": f"{plain(h)}: {plain(c)}", "kids": []} for h, c in zip(hdr[1:], r[1:]) if c]} for r in b["rows"][1:]]
    return []
def walk(node):
    kids = []
    for b in node.get("children", []):
        if b["kind"] == "h3": kids.append({"text": plain(b["text"]), "kids": walk(b)})
        else:
            for l in leaves(b): kids.append(l if isinstance(l, dict) else {"text": l, "kids": []})
    return kids
tree = {"text": plain(root["text"]), "kids": [{"text": plain(s["text"]), "kids": walk(s)} for s in root["children"] if s["kind"] == "h2"]}
def opml(n, d):
    pad = "    " + "  " * d; t = html.escape(n["text"], quote=True)
    return [f'{pad}<outline text="{t}">'] + [l for k in n["kids"] for l in opml(k, d + 1)] + [f"{pad}</outline>"]
open("BRAINLIFT.opml", "w", encoding="utf-8").write('<?xml version="1.0" encoding="UTF-8"?>\n<opml version="2.0">\n<head><title>Alpha Hours BrainLift</title></head>\n<body>\n' + "\n".join(opml(tree, 0)) + "\n</body>\n</opml>\n")
def wf(n, d): return ["\t" * d + n["text"]] + [l for k in n["kids"] for l in wf(k, d + 1)]
open("BRAINLIFT-workflowy.txt", "w", encoding="utf-8").write("\n".join(wf(tree, 0)) + "\n")
print("sections:", [s["text"] for s in root["children"]])
