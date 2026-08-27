#!/usr/bin/env python3
"""Regenerate html, opml and Workflowy outlines from the markdown sources. No dependencies."""
import re, html, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
CSS = """body{font-family:Georgia,'Times New Roman',serif;max-width:860px;margin:40px auto;padding:0 24px;color:#12100c;background:#fffdf7;line-height:1.55}
h1{font-size:2rem;margin:0 0 .5em}h2{font-size:1.4rem;margin:2em 0 .5em;border-bottom:1px solid #d9d2c3;padding-bottom:.2em}h3{font-size:1.1rem;margin:1.5em 0 .4em}
table{border-collapse:collapse;width:100%;margin:1em 0;font-size:.92rem}th,td{border:1px solid #d9d2c3;padding:6px 8px;text-align:left;vertical-align:top}th{background:#f3eee2}
p{margin:.7em 0}ul,ol{margin:.6em 0 .6em 1.4em}code{background:#f3eee2;padding:1px 4px}"""

def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'`(.+?)`', r'<code>\1</code>', s)
    s = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', s)
    return s

def md_to_html(text, title):
    out = []; lines = text.splitlines(); i = 0
    while i < len(lines):
        l = lines[i]
        if l.startswith('#'):
            n = len(l) - len(l.lstrip('#')); out.append(f'<h{n}>{inline(l[n:].strip())}</h{n}>'); i += 1
        elif l.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].startswith('|'):
                rows.append([c.strip() for c in lines[i].strip().strip('|').split('|')]); i += 1
            rows = [r for r in rows if not all(re.fullmatch(r':?-+:?', c) for c in r)]
            out.append('<table>' + ''.join('<tr>' + ''.join(f'<{"th" if k==0 else "td"}>{inline(c)}</{"th" if k==0 else "td"}>' for c in r) + '</tr>' for k, r in enumerate(rows)) + '</table>')
        elif re.match(r'^(\d+\.|-)\s', l):
            tag = 'ol' if l[0].isdigit() else 'ul'; items = []
            while i < len(lines) and re.match(r'^(\d+\.|-)\s', lines[i]):
                items.append(re.sub(r'^(\d+\.|-)\s', '', lines[i])); i += 1
            out.append(f'<{tag}>' + ''.join(f'<li>{inline(x)}</li>' for x in items) + f'</{tag}>')
        elif l.strip() == '':
            i += 1
        else:
            para = []
            while i < len(lines) and lines[i].strip() and not lines[i].startswith(('#', '|')) and not re.match(r'^(\d+\.|-)\s', lines[i]):
                para.append(lines[i]); i += 1
            out.append(f'<p>{inline(" ".join(para))}</p>')
    return f'<!doctype html><html><head><meta charset="utf-8"><title>{html.escape(title)}</title><style>{CSS}</style></head><body>{"".join(out)}</body></html>'

def md_to_outline(text):
    """Return nested (title, children) from headings; paragraphs become leaf nodes."""
    root = ('root', []); stack = [(0, root)]
    for l in text.splitlines():
        if not l.strip(): continue
        if l.startswith('#'):
            n = len(l) - len(l.lstrip('#')); node = (l[n:].strip(), [])
            while stack and stack[-1][0] >= n: stack.pop()
            stack[-1][1][1].append(node); stack.append((n, node))
        else:
            stack[-1][1][1].append((re.sub(r'\*\*', '', l.strip()), []))
    return root

def to_opml(node, depth=0):
    if depth == 0:
        body = ''.join(to_opml(c, 1) for c in node[1])
        return f'<?xml version="1.0" encoding="UTF-8"?><opml version="2.0"><head><title>{html.escape(node[0])}</title></head><body>{body}</body></opml>'
    kids = ''.join(to_opml(c, depth + 1) for c in node[1])
    return f'<outline text="{html.escape(node[0], quote=True)}">{kids}</outline>' if kids else f'<outline text="{html.escape(node[0], quote=True)}"/>'

def to_workflowy(node, depth=0):
    lines = [] if depth == 0 else ['  ' * (depth - 1) + '- ' + node[0]]
    for c in node[1]: lines.extend(to_workflowy(c, depth + 1))
    return lines

JOBS = [('BRAINLIFT.md', 'brainlift.html', 'BrainLift: Alpha Hours'), ('BUSINESS-PLAN.md', 'business-plan.html', 'Alpha Hours: Business plan'),
        ('FINANCIALS.md', 'financials.html', 'Alpha Hours: Financials'), ('EXECUTIVE-ONE-PAGER.md', 'one-pager.html', 'Alpha Hours: Executive one-pager')]
for src, dst, title in JOBS:
    (ROOT / dst).write_text(md_to_html((ROOT / src).read_text(), title))
bl = (ROOT / 'BRAINLIFT.md').read_text()
tree = md_to_outline(bl); tree = ('BrainLift: Alpha Hours', tree[1][0][1]) if tree[1] else tree
(ROOT / 'BRAINLIFT.opml').write_text(to_opml(tree))
(ROOT / 'BRAINLIFT-workflowy.txt').write_text('\n'.join(to_workflowy(tree)) + '\n')
bm = bl.split('## Business Model and Operations')[1].split('## Financials')[0]
bm_tree = md_to_outline('## Business Model and Operations' + bm)
(ROOT / 'BUSINESS-MODEL.opml').write_text(to_opml(('Alpha Hours: Business model', bm_tree[1])))
print('generated', [d for _, d, _ in JOBS], 'BRAINLIFT.opml BRAINLIFT-workflowy.txt BUSINESS-MODEL.opml')
