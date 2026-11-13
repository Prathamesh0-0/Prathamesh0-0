# -*- coding: utf-8 -*-
"""
Generates every SVG in assets/. Run from the repository root:

    python scripts/build.py

The images are plain SVG with CSS animation: no scripts, no web fonts, no outside requests,
which is what GitHub allows inside a README image. Every animation is switched off for
viewers who ask for reduced motion, and each image still reads correctly when it is still.
"""
import os
import random
from string import Template
from xml.sax.saxutils import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets")
os.makedirs(OUT, exist_ok=True)

# Palette: the same tokens as prathameshtikle.tech.
COL = dict(
    BG="#0b0e12", PANE="#10141a", PANE2="#151a22", LINE="#222934", LINE2="#2e3744",
    TEXT="#d3d8df", STRONG="#f4f1ea", MUT="#919baa", FAINT="#6d7684", AMBER="#f0b73f",
    BLUE="#7cc4ff", GREEN="#8fd6a4", VIOLET="#c0a8ff", CORAL="#ff9f7a",
)
BG, PANE, PANE2, LINE, LINE2 = COL["BG"], COL["PANE"], COL["PANE2"], COL["LINE"], COL["LINE2"]
TEXT, STRONG, MUT, FAINT, AMBER = COL["TEXT"], COL["STRONG"], COL["MUT"], COL["FAINT"], COL["AMBER"]
BLUE, GREEN, VIOLET, CORAL = COL["BLUE"], COL["GREEN"], COL["VIOLET"], COL["CORAL"]

MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans',Helvetica,Arial,sans-serif"

BASE_CSS = (
    "text{font-family:" + MONO + "}"
    ".s{font-family:" + SANS + "}"
    ".rec{animation:rec 1.6s ease-in-out infinite}"
    "@keyframes rec{0%,100%{opacity:1}50%{opacity:.25}}"
)
REDUCED = "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"


def css(s):
    return Template(s).substitute(COL)


def e(s):
    return escape(str(s), {'"': "&quot;"})


def n(v):
    """Compact number for attributes."""
    s = ("%.2f" % v).rstrip("0").rstrip(".")
    return s if s else "0"


def pct(v):
    return n(v) + "%"


def t(x, y, s, fill=TEXT, size=12, anchor=None, weight=None, cls=None, style=None, ls=None, extra=""):
    a = ['x="%s"' % n(x), 'y="%s"' % n(y), 'fill="%s"' % fill, 'font-size="%s"' % n(size), 'xml:space="preserve"']
    if anchor:
        a.append('text-anchor="%s"' % anchor)
    if weight:
        a.append('font-weight="%s"' % weight)
    if cls:
        a.append('class="%s"' % cls)
    if style:
        a.append('style="%s"' % style)
    if ls:
        a.append('letter-spacing="%s"' % n(ls))
    if extra:
        a.append(extra)
    return "<text %s>%s</text>" % (" ".join(a), e(s))


def shell(w, h, r=14, fill=BG, stroke=LINE):
    return '<rect x=".5" y=".5" width="%s" height="%s" rx="%d" fill="%s" stroke="%s"/>' % (n(w - 1), n(h - 1), r, fill, stroke)


def topbar(w, label, right="", live="REC"):
    out = [
        '<line x1="1" y1="40.5" x2="%d" y2="40.5" stroke="%s"/>' % (w - 1, LINE),
        '<circle class="rec" cx="26" cy="21" r="4" fill="%s"/>' % AMBER,
        t(38, 25, live, AMBER, 11, weight=700, ls=1.5),
        t(38 + len(live) * 8.4 + 12, 25, label, TEXT, 12),
    ]
    if right:
        out.append(t(w - 22, 25, right, MUT, 11.5, anchor="end"))
    return "".join(out)


def svg(name, w, h, title, body, style="", defs=""):
    doc = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
        'role="img" aria-label="{t}"><title>{t}</title><style>{c}</style>{d}{b}</svg>\n'
    ).format(w=w, h=h, t=e(title), c=BASE_CSS + style + REDUCED, d=("<defs>%s</defs>" % defs) if defs else "", b=body)
    with open(os.path.join(OUT, name), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(doc)
    print("%-22s %6.1f KB" % (name, len(doc.encode("utf-8")) / 1024))


# --------------------------------------------------------------------------------------------
# 1. Hero: the name decrypts, its sixteen bytes light up underneath, a pulse runs the trace.
# --------------------------------------------------------------------------------------------
def hero():
    W, H = 840, 384
    rnd = random.Random(77)
    name = "PRATHAMESH TIKLE"
    noise = "01#$%&/<>[]{}=+*?XA7E"
    frames_n, step, cycle = 18, 0.075, 14.0

    frames = []
    for i in range(frames_n):
        solved = int(round(len(name) * i / (frames_n - 1)))
        frames.append("".join(c if (k < solved or c == " ") else rnd.choice(noise) for k, c in enumerate(name)))

    st = [css(
        ".nm{opacity:0;animation-duration:14s;animation-timing-function:step-end;animation-iteration-count:infinite}"
        ".nf{opacity:1}"
        ".caret{animation:caret 1s step-end infinite}@keyframes caret{50%{opacity:0}}"
        ".in{animation:in .7s ease-out backwards}@keyframes in{from{opacity:0;transform:translateY(6px)}}"
        ".scan{animation:scan 9s linear infinite}@keyframes scan{to{transform:translateX(1180px)}}"
        ".pulse{animation:pulse 5.5s linear infinite}@keyframes pulse{from{stroke-dashoffset:110}to{stroke-dashoffset:-1000}}"
        ".by{animation-duration:14s;animation-timing-function:linear;animation-iteration-count:infinite}"
    )]
    for i in range(frames_n):
        a, b = i * step / cycle * 100, (i + 1) * step / cycle * 100
        if i == 0:
            kf = "0%{opacity:1}" + pct(b) + "{opacity:0}100%{opacity:0}"
        elif i == frames_n - 1:
            kf = "0%{opacity:0}" + pct(a) + "{opacity:1}100%{opacity:1}"
        else:
            kf = "0%{opacity:0}" + pct(a) + "{opacity:1}" + pct(b) + "{opacity:0}100%{opacity:0}"
        st.append("@keyframes n%d{%s}.n%d{animation-name:n%d}" % (i, kf, i, i))
    for k in range(16):
        a = max(0.2, (k / 16.0) * (frames_n - 1) * step / cycle * 100)
        st.append(
            "@keyframes b%d{0%%{fill:%s}%s{fill:%s}%s{fill:%s}%s{fill:%s}100%%{fill:%s}}.b%d{animation-name:b%d}"
            % (k, FAINT, pct(a), FAINT, pct(a + 0.4), AMBER, pct(a + 5), TEXT, TEXT, k, k)
        )

    defs = (
        '<pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="#1b2129"/></pattern>'
        '<radialGradient id="glow" cx="88%" cy="0%" r="70%"><stop offset="0" stop-color="{a}" stop-opacity=".16"/><stop offset="1" stop-color="{a}" stop-opacity="0"/></radialGradient>'
        '<linearGradient id="band" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="{a}" stop-opacity="0"/><stop offset=".5" stop-color="{a}" stop-opacity=".07"/><stop offset="1" stop-color="{a}" stop-opacity="0"/></linearGradient>'
        '<clipPath id="clip"><rect x="1" y="1" width="{w}" height="{h}" rx="13"/></clipPath>'
    ).format(a=AMBER, w=W - 2, h=H - 2)

    b = [shell(W, H)]
    b.append('<g clip-path="url(#clip)">')
    b.append('<rect x="1" y="41" width="%d" height="%d" fill="url(#dots)"/>' % (W - 2, H - 42))
    b.append('<rect x="1" y="1" width="%d" height="%d" fill="url(#glow)"/>' % (W - 2, H - 2))
    b.append('<rect class="scan" x="-180" y="41" width="180" height="%d" fill="url(#band)"/>' % (H - 42))
    b.append("</g>")
    b.append(topbar(W, "prathamesh-tikle.pcap", "eth0 · 18.52°N 73.85°E · Pune, IN"))

    # prompt
    b.append(t(40, 86, "77pseudo@pune", AMBER, 13))
    b.append(t(40 + 13 * 7.8, 86, ":~$ whoami", MUT, 13))

    # the name, as a stack of frames
    for i, fr in enumerate(frames):
        last = i == frames_n - 1
        b.append(t(40, 152, fr, STRONG if last else AMBER, 52, weight=800,
                   cls="nm n%d%s" % (i, " nf" if last else ""), extra='textLength="496"'))
    b.append('<rect class="caret" x="548" y="112" width="16" height="42" fill="%s"/>' % AMBER)

    b.append(t(40, 190, "Offensive security and security engineering.", TEXT, 18, cls="s in", style="animation-delay:1.3s"))
    b.append(t(40, 222, "→ prathameshtikle.tech", AMBER, 13, cls="in", style="animation-delay:1.6s"))

    # detail card
    x0, y0 = 600, 62
    b.append('<rect x="%d" y="%d" width="214" height="170" rx="8" fill="%s" stroke="%s"/>' % (x0, y0, PANE, LINE))
    b.append(t(x0 + 14, y0 + 25, "▸ Frame 1: whoami", STRONG, 11.5, weight=700))
    b.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s"/>' % (x0 + 1, y0 + 36, x0 + 213, y0 + 36, LINE))
    detail = [
        ("alias", "77Pseudo", TEXT),
        ("focus", "offensive security", TEXT),
        ("base", "Pune, India", TEXT),
        ("cert", "CompTIA Security+", AMBER),
        ("rank", "TryHackMe top 3%", TEXT),
        ("state", "capturing", GREEN),
    ]
    for i, (k, v, c) in enumerate(detail):
        y = y0 + 58 + i * 20
        d = "animation-delay:%ss" % n(1.4 + i * 0.12)
        b.append(t(x0 + 14, y, k, FAINT, 11.5, cls="in", style=d))
        b.append(t(x0 + 62, y, v, c, 11.5, cls="in", style=d))

    # the name as bytes
    b.append('<line x1="40" y1="250.5" x2="%d" y2="250.5" stroke="%s"/>' % (W - 26, LINE))
    cw, hy = 7.8, 278
    b.append(t(40, hy, "0000", FAINT, 13))
    plain = "Prathamesh Tikle"
    for k, ch in enumerate(plain):
        col = 6 + k * 3 + (1 if k >= 8 else 0)
        b.append(t(40 + col * cw, hy, "%02x" % ord(ch), TEXT, 13, cls="by b%d" % k))
        b.append(t(40 + (58 + k) * cw, hy, ch, TEXT, 13, cls="by b%d" % k))
    b.append(t(40 + 57 * cw, hy, "|", FAINT, 13))
    b.append(t(40 + 74 * cw, hy, "|", FAINT, 13))
    b.append(t(W - 26, hy, "16 bytes on the wire", FAINT, 11, anchor="end"))

    # the trace
    base = 334
    d = ["M40 %d" % base]
    for x in (112, 226, 318, 446, 540, 636, 738):
        up, dn = rnd.randint(14, 26), rnd.randint(6, 12)
        d.append("L%d %d L%d %d L%d %d L%d %d" % (x, base, x + 7, base - up, x + 14, base + dn, x + 21, base))
    d.append("L800 %d" % base)
    path = " ".join(d)
    b.append('<path d="%s" fill="none" stroke="%s" stroke-width="1.5" stroke-linejoin="round"/>' % (path, LINE2))
    b.append('<path class="pulse" d="%s" fill="none" stroke="%s" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" pathLength="1000" stroke-dasharray="110 1890" stroke-dashoffset="-400"/>' % (path, AMBER))
    for x, lab, anchor in ((40, "2024", None), (293, "2025", "middle"), (547, "2026", "middle"), (800, "now", "end")):
        b.append('<line x1="%d" y1="352" x2="%d" y2="357" stroke="%s"/>' % (x, x, FAINT))
        b.append(t(x, 371, lab, FAINT, 10.5, anchor=anchor))

    svg("hero.svg", W, H, "Prathamesh Tikle (77Pseudo): offensive security and security engineering, Pune, India", "".join(b), "".join(st), defs)


# --------------------------------------------------------------------------------------------
# 2. The capture: two years of work as a packet list.
# --------------------------------------------------------------------------------------------
def capture():
    rows = [
        ("2024", "tryhackme", "LAB", "First lab solved. Everything after this follows from it.", STRONG),
        ("Oct 2024", "github", "REPO", "Samvidhan Simplified: a Flutter app, my first public repo", VIOLET),
        ("Sep 2025", "Ceres Canopus", "WORK", "Technical Operations Engineer: Python and n8n automation", BLUE),
        ("Jan 2026", "CompTIA", "CERT", "Security+ passed. A globally recognised certification.", AMBER),
        ("Feb 2026", "Secur Wires", "WORK", "Cadet Intern: API security controls and GRC frameworks", BLUE),
        ("Mar 2026", "github", "TOOL", "SocketSnoop: a honeypot that maps every command to ATT&CK", GREEN),
        ("Jun 2026", "github", "TOOL", "VeriFlow: document forensics for loan underwriting, live demo", GREEN),
        ("Jul 2026", "github", "TOOL", "Panoptes: insider-threat detection for a banking hackathon", GREEN),
        ("Jul 2026", "github", "REPO", "CrimeIntel: crime analytics you ask in English or Kannada", VIOLET),
        ("Jul 2026", "DevTown", "TEACH", "Cyber Security Mentor: web-vulnerability bootcamps on DVWA", CORAL),
        ("Oct 2026", "github", "TOOL", "IPsec Sentinel: passive IPsec analyser, SIH 2026 PS 160", GREEN),
        ("Now", "not public", "NOW", "MALINT-X: triage for fraudulent banking APKs. In progress.", AMBER),
    ]
    W, r0, rh = 840, 104, 26
    H = r0 + len(rows) * rh + 36
    X = dict(no=26, time=66, dest=156, proto=296, info=366)

    st = css(
        ".r{animation:row .5s ease-out backwards}@keyframes row{from{opacity:0;transform:translateX(-10px)}}"
        ".sel{animation:sel 24s steps(12) infinite}@keyframes sel{to{transform:translateY(312px)}}"
    )
    b = [shell(W, H), topbar(W, "prathamesh-tikle.pcap", "12 frames · 2024 to now")]
    # display filter
    b.append('<rect x="16.5" y="49.5" width="%d" height="22" rx="4" fill="%s" stroke="%s"/>' % (W - 33, PANE, LINE2))
    b.append(t(28, 65, 'frame.owner == "77Pseudo"', GREEN, 11.5))
    b.append(t(W - 28, 65, "12 displayed · 0 dropped", FAINT, 10.5, anchor="end"))
    # column header
    b.append('<rect x="1" y="78" width="%d" height="26" fill="%s"/>' % (W - 2, PANE))
    for key, lab in (("no", "NO."), ("time", "TIME"), ("dest", "DESTINATION"), ("proto", "PROTO"), ("info", "INFO")):
        b.append(t(X[key], 95, lab, MUT, 10, ls=1.2))
    for i, (time, dest, proto, info, colr) in enumerate(rows):
        y = r0 + i * rh
        cert = proto == "CERT"
        g = ['<g class="r" style="animation-delay:%ss">' % n(0.2 + i * 0.11)]
        if cert:
            g.append('<rect x="1" y="%d" width="%d" height="%d" fill="%s" fill-opacity=".1"/>' % (y, W - 2, rh, AMBER))
            g.append('<rect x="1" y="%d" width="3" height="%d" fill="%s"/>' % (y, rh, AMBER))
        elif i % 2:
            g.append('<rect x="1" y="%d" width="%d" height="%d" fill="#0e1217"/>' % (y, W - 2, rh))
        ink = AMBER if cert else TEXT
        g.append(t(X["no"], y + 17, str(i + 1), FAINT, 12))
        g.append(t(X["time"], y + 17, time, AMBER if cert else MUT, 12))
        g.append(t(X["dest"], y + 17, dest, ink, 12))
        g.append(t(X["proto"], y + 17, proto, colr, 12, weight=700))
        g.append(t(X["info"], y + 17, info, STRONG if cert else TEXT, 12, weight=700 if cert else None))
        if cert:
            g.append('<circle cx="%d" cy="%d" r="8" fill="%s"/>' % (W - 26, y + 13, AMBER))
            g.append('<path d="M%d %d l3 3 l5.5 -6.5" fill="none" stroke="%s" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>' % (W - 30, y + 13, BG))
        g.append("</g>")
        b.append("".join(g))
    b.append('<g class="sel"><rect x="1" y="%d" width="%d" height="%d" fill="%s" fill-opacity=".07"/><rect x="%d" y="%d" width="2" height="%d" fill="%s"/></g>' % (r0, W - 2, rh, STRONG, W - 3, r0, rh, AMBER))
    sy = r0 + len(rows) * rh
    b.append('<line x1="1" y1="%s" x2="%d" y2="%s" stroke="%s"/>' % (n(sy + 0.5), W - 1, n(sy + 0.5), LINE))
    b.append('<circle class="rec" cx="26" cy="%d" r="3.5" fill="%s"/>' % (sy + 18, GREEN))
    b.append(t(38, sy + 22, "still capturing", MUT, 11))
    b.append(t(W - 22, sy + 22, "the full capture, down to the bytes: prathameshtikle.tech/capture", AMBER, 11, anchor="end"))

    svg("capture.svg", W, H, "The trace so far: twelve dated events from the first TryHackMe lab in 2024 to MALINT-X now, with CompTIA Security+ passed in January 2026", "".join(b), st)


# --------------------------------------------------------------------------------------------
# 3. Case files: one card per project, each with its own small moving figure.
# --------------------------------------------------------------------------------------------
def glyph_ipsec():
    return css(
        ".g1{animation:flow 1s linear infinite}@keyframes flow{to{stroke-dashoffset:-24}}"
    ), (
        '<line x1="17" y1="28" x2="53" y2="28" stroke="{l}" stroke-width="1.5"/>'
        '<line x1="17" y1="42" x2="53" y2="42" stroke="{l}" stroke-width="1.5"/>'
        '<line class="g1" x1="17" y1="35" x2="53" y2="35" stroke="{a}" stroke-width="2.5" stroke-dasharray="6 6"/>'
        '<circle cx="10" cy="35" r="6.5" fill="{p}" stroke="{t}" stroke-width="1.5"/>'
        '<circle cx="60" cy="35" r="6.5" fill="{p}" stroke="{t}" stroke-width="1.5"/>'
    ).format(l=LINE2, a=AMBER, t=TEXT, p=PANE) + t(35, 62, "ESP", FAINT, 9, anchor="middle", ls=1.5)


def glyph_veriflow():
    lines = "".join(
        '<line x1="22" y1="{y}" x2="{x}" y2="{y}" stroke="{c}" stroke-width="2" stroke-linecap="round"/>'.format(
            y=y, x=x, c=(AMBER if y == 38 else LINE2))
        for y, x in ((20, 44), (29, 48), (38, 40), (47, 48), (56, 36)))
    return css(
        ".g1{animation:doc 2.6s ease-in-out infinite alternate}@keyframes doc{to{transform:translateY(56px)}}"
    ), (
        '<rect x="14" y="6" width="42" height="60" rx="4" fill="{p}" stroke="{t}" stroke-width="1.5"/>'.format(p=PANE, t=TEXT)
        + lines
        + '<rect class="g1" x="8" y="7" width="54" height="2" rx="1" fill="%s"/>' % AMBER
    )


def glyph_panoptes():
    pts = [(12, 44), (20, 54), (26, 40), (30, 58), (36, 48), (16, 30), (40, 60), (24, 26), (46, 44), (34, 34)]
    dots = "".join('<circle cx="%d" cy="%d" r="3" fill="%s"/>' % (x, y, LINE2) for x, y in pts)
    return css(
        ".g1{transform-box:fill-box;transform-origin:center;animation:ring 2s ease-out infinite}"
        "@keyframes ring{from{transform:scale(1);opacity:.9}to{transform:scale(3.4);opacity:0}}"
    ), (
        dots
        + '<circle class="g1" cx="57" cy="14" r="4" fill="none" stroke="%s" stroke-width="1.5"/>' % AMBER
        + '<circle cx="57" cy="14" r="4" fill="%s"/>' % AMBER
    )


def glyph_socketsnoop():
    return css(
        ".g1{animation:tag 4s step-end infinite}@keyframes tag{0%{opacity:0}35%{opacity:1}100%{opacity:1}}"
        ".g2{animation:caret 1s step-end infinite}@keyframes caret{50%{opacity:0}}"
    ), (
        '<rect x="3" y="8" width="64" height="54" rx="5" fill="{p}" stroke="{t}" stroke-width="1.5"/>'
        '<line x1="3" y1="20" x2="67" y2="20" stroke="{l}"/>'
        '<circle cx="11" cy="14" r="1.8" fill="{l}"/><circle cx="18" cy="14" r="1.8" fill="{l}"/>'
    ).format(p=PANE, t=TEXT, l=LINE2) + (
        t(9, 35, "$ whoami", TEXT, 9.5)
        + t(9, 50, "T1033", AMBER, 9.5, weight=700, cls="g1")
        + '<rect class="g2" x="42" y="42" width="6" height="10" fill="%s"/>' % AMBER
    )


def glyph_crimeintel():
    bars = []
    for i, (x, h) in enumerate(((8, 22), (23, 38), (38, 28), (53, 48))):
        bars.append('<rect class="g1" style="animation-delay:%ss" x="%d" y="%d" width="10" height="%d" rx="2" fill="%s"/>' % (
            n(i * 0.25), x, 62 - h, h, AMBER if i == 3 else LINE2))
    return css(
        ".g1{transform-box:fill-box;transform-origin:bottom;animation:bar 1.8s ease-in-out infinite alternate}"
        "@keyframes bar{from{transform:scaleY(.45)}to{transform:scaleY(1)}}"
    ), "".join(bars) + '<line x1="4" y1="63.5" x2="67" y2="63.5" stroke="%s"/>' % TEXT


def glyph_malintx():
    hexagon = "35,13 54,24 54,46 35,57 16,46 16,24"
    return css(
        ".g1{transform-box:fill-box;transform-origin:center;animation:spin 14s linear infinite}@keyframes spin{to{transform:rotate(360deg)}}"
    ), (
        '<circle class="g1" cx="35" cy="35" r="31" fill="none" stroke="%s" stroke-width="1.5" stroke-dasharray="4 7"/>' % AMBER
        + '<polygon points="%s" fill="%s" stroke="%s" stroke-width="1.5" stroke-linejoin="round"/>' % (hexagon, PANE, TEXT)
        + t(35, 39, "APK", STRONG, 10, anchor="middle", weight=700)
    )


def card(fname, idx, title, aka, kicker, stack, stage, stage_col, link, glyph):
    W, H = 410, 190
    gst, gbody = glyph()
    st = css(
        ".sw{animation:sw 5s ease-in-out infinite}@keyframes sw{from{transform:translateX(0)}to{transform:translateX(560px)}}"
        ".ar{animation:ar 1.6s ease-in-out infinite alternate}@keyframes ar{to{transform:translate(2px,-2px)}}"
    ) + gst
    defs = (
        '<clipPath id="clip"><rect x="1" y="1" width="{w}" height="{h}" rx="11"/></clipPath>'
        '<linearGradient id="sw" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="{a}" stop-opacity="0"/><stop offset=".5" stop-color="{a}"/><stop offset="1" stop-color="{a}" stop-opacity="0"/></linearGradient>'
    ).format(w=W - 2, h=H - 2, a=AMBER)
    b = [shell(W, H, 12, PANE)]
    b.append('<g clip-path="url(#clip)"><rect class="sw" style="animation-delay:%ss" x="-150" y="%d" width="150" height="2" fill="url(#sw)"/></g>' % (n(idx * 0.6), H - 3))
    b.append(t(22, 31, "0x%02d" % (idx + 1), AMBER, 11, weight=700, ls=1))
    b.append(t(W - 22, 31, stage, MUT, 10.5, anchor="end"))
    b.append('<circle class="rec" cx="%s" cy="27" r="3" fill="%s"/>' % (n(W - 22 - len(stage) * 6.3 - 9), stage_col))
    b.append(t(22, 70, title, STRONG, 23, weight=700, cls="s"))
    b.append(t(22, 91, aka, MUT, 11.5, cls="s"))
    for i, ln in enumerate(kicker):
        b.append(t(22, 124 + i * 19, ln, TEXT, 13.5, cls="s"))
    b.append(t(22, 172, stack, FAINT, 10.5))
    b.append('<g class="ar">%s</g>' % t(W - 22, 172, link, AMBER, 11, anchor="end", weight=700))
    b.append('<g transform="translate(318 42)">%s</g>' % gbody)
    svg(fname, W, H, "%s: %s" % (title, " ".join(kicker)), "".join(b), st, defs)


def cards():
    data = [
        ("card-ipsec.svg", "IPsec Sentinel", "Smart India Hackathon 2026 · problem statement 160",
         ["Facts are parsed. Estimates are inferred.", "A passive analyser for IPsec VPN captures."],
         "Python · scikit-learn · SHAP · strongSwan", "advanced", GREEN, "repo ↗", glyph_ipsec),
        ("card-veriflow.svg", "VeriFlow", "VeriFlow Suraksha",
         ["Document DNA for loan underwriting.", "A forensics engine, with a live demo."],
         "Python · FastAPI · PyMuPDF · OpenCV", "shipped", GREEN, "repo ↗", glyph_veriflow),
        ("card-panoptes.svg", "Panoptes", "Peer-group baselines · policy as code · signed audit",
         ["Insider-threat detection that knows", "an admin is not an anomaly."],
         "Python · scikit-learn · OPA/Rego · ML-KEM", "prototype", AMBER, "repo ↗", glyph_panoptes),
        ("card-socketsnoop.svg", "SocketSnoop AI", "PhantomNet engine · NexaCore decoy",
         ["A decoy company that interviews its intruders.", "Every command is mapped to MITRE ATT&CK."],
         "Python · asyncio · WebSockets · SQLite", "prototype", AMBER, "repo ↗", glyph_socketsnoop),
        ("card-crimeintel.svg", "KSP CrimeIntel", "Conversational crime analytics",
         ["Crime records you can question", "in English or Kannada."],
         "FastAPI · DuckDB · Gemini · React", "public", GREEN, "repo ↗", glyph_crimeintel),
        ("card-malintx.svg", "MALINT-X", "Previously SENTINEL",
         ["Triage for fraudulent banking APKs:", "decompiled, sliced, then explained."],
         "Python · JADX · Apktool · Shodan", "active research", AMBER, "case file ↗", glyph_malintx),
    ]
    for i, (fname, title, aka, kicker, stack, stage, col, link, glyph) in enumerate(data):
        card(fname, i, title, aka, kicker, stack, stage, col, link, glyph)


# --------------------------------------------------------------------------------------------
# 4. The record: the certification, then the results.
# --------------------------------------------------------------------------------------------
def record():
    W, H = 840, 284
    rows = [
        ("02", "2nd prize, national level", "InnovationXPO 2026, PCCOE", True),
        ("03", "3rd prize, national level", "National Project Competition, VIIT Pune", True),
        ("01", "1st place, solo", "DPCOE HackFest 2026: CTF challenge", False),
        ("02", "2nd prize, team Boots N Guts", "DPCOE hackathon 2026", False),
        ("★", "Student Excellence Award 2026", "ZSkillUp · Saksham Bharat · FTPO", False),
        ("3%", "Top 3% globally", "TryHackMe: 77Pseudo", False),
    ]
    st = css(
        ".ring{transform-box:fill-box;transform-origin:center;animation:spin 18s linear infinite}@keyframes spin{to{transform:rotate(360deg)}}"
        ".halo{transform-box:fill-box;transform-origin:center;animation:halo 3s ease-out infinite}"
        "@keyframes halo{from{transform:scale(1);opacity:.5}to{transform:scale(1.7);opacity:0}}"
        ".tick{animation:tick 6s ease-in-out infinite}@keyframes tick{0%,8%{stroke-dashoffset:1}20%,100%{stroke-dashoffset:0}}"
        ".r{animation:row .6s ease-out backwards}@keyframes row{from{opacity:0;transform:translateX(14px)}}"
    )
    b = [shell(W, H)]
    # the seal
    b.append('<rect x="16.5" y="16.5" width="268" height="%d" rx="10" fill="%s" fill-opacity=".06" stroke="%s" stroke-opacity=".6"/>' % (H - 33, AMBER, AMBER))
    cx, cy = 150, 88
    b.append('<circle class="halo" cx="%d" cy="%d" r="34" fill="none" stroke="%s" stroke-width="1.5"/>' % (cx, cy, AMBER))
    b.append('<circle class="ring" cx="%d" cy="%d" r="45" fill="none" stroke="%s" stroke-width="1.5" stroke-dasharray="3 6"/>' % (cx, cy, AMBER))
    b.append('<circle cx="%d" cy="%d" r="34" fill="%s"/>' % (cx, cy, AMBER))
    b.append('<path class="tick" d="M%d %d l11 11 l19 -23" pathLength="1" stroke-dasharray="1" fill="none" stroke="%s" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>' % (cx - 15, cy + 1, BG))
    b.append(t(cx, 164, "CompTIA Security+", STRONG, 19, anchor="middle", weight=700, cls="s"))
    b.append(t(cx, 186, "PASSED · JAN 2026", AMBER, 11, anchor="middle", weight=700, ls=1.6))
    b.append('<line x1="56" y1="204.5" x2="244" y2="204.5" stroke="%s" stroke-opacity=".35"/>' % AMBER)
    b.append(t(cx, 226, "Google Cybersecurity Professional Certificate", MUT, 10.5, anchor="middle", cls="s"))
    b.append(t(cx, 244, "Securiti: AI Security & Governance", MUT, 10.5, anchor="middle", cls="s"))
    # results
    x0, y0, rh = 314, 20, 41
    for i, (mark, title, event, national) in enumerate(rows):
        y = y0 + i * rh
        g = ['<g class="r" style="animation-delay:%ss">' % n(0.3 + i * 0.12)]
        g.append(t(x0 + 20, y + 26, mark, AMBER, 17, anchor="middle", weight=800))
        g.append(t(x0 + 54, y + 18, title, STRONG, 14, weight=600, cls="s"))
        g.append(t(x0 + 54, y + 34, event, MUT, 12, cls="s"))
        if national:
            g.append('<rect x="%d" y="%d" width="82" height="20" rx="10" fill="none" stroke="%s"/>' % (W - 22 - 82, y + 10, AMBER))
            g.append(t(W - 22 - 41, y + 23.5, "NATIONAL", AMBER, 9.5, anchor="middle", weight=700, ls=1.2))
        if i < len(rows) - 1:
            g.append('<line x1="%d" y1="%s" x2="%d" y2="%s" stroke="%s"/>' % (x0, n(y + rh + 0.5), W - 20, n(y + rh + 0.5), LINE))
        g.append("</g>")
        b.append("".join(g))
    svg("record.svg", W, H, "The record: CompTIA Security+ passed January 2026; 2nd prize national level at InnovationXPO 2026; 3rd prize national level at VIIT Pune; 1st place solo in the DPCOE HackFest 2026 CTF; 2nd prize with team Boots N Guts; Student Excellence Award 2026; TryHackMe top 3% globally", "".join(b), st)


# --------------------------------------------------------------------------------------------
# 5. Toolbelt: a real hex dump. The bytes on the left are the ASCII on the right.
# --------------------------------------------------------------------------------------------
def stack():
    rows = [
        ("Burp Suite  Nmap", "; web and recon"),
        ("Metasploit  JADX", "; exploit and reverse"),
        ("Wireshark tshark", "; what crosses the wire"),
        ("Python   FastAPI", "; what the tools are in"),
        ("Docker  OPA/Rego", "; ship it, then enforce it"),
        ("scikit-learn SQL", "; models and their data"),
        ("React TypeScript", "; dashboards"),
        ("Apktool  Flutter", "; android, both sides"),
        ("strongSwan  SHAP", "; vpn testbed, explained"),
        ("Kali Linux   Git", "; home"),
    ]
    for r, _ in rows:
        assert len(r) == 16, r
    W, y0, rh, cw, x0 = 840, 94, 22, 7.2, 26
    H = y0 + len(rows) * rh + 22
    st = css(
        ".hl{animation:hl 20s steps(10) infinite}@keyframes hl{to{transform:translateY(220px)}}"
        ".a{animation:glow 20s linear infinite}"
    )
    kf = []
    for i in range(len(rows)):
        a, z = i * 10.0, (i + 1) * 10.0
        parts = []
        if i > 0:
            parts.append("0%%{fill:%s}%s{fill:%s}" % (TEXT, pct(a - 0.01), TEXT))
        parts.append("%s{fill:%s}%s{fill:%s}" % (pct(a), AMBER, pct(z - 0.01), AMBER))
        if i < len(rows) - 1:
            parts.append("%s{fill:%s}100%%{fill:%s}" % (pct(z), TEXT, TEXT))
        kf.append("@keyframes g%d{%s}.a%d{animation-name:g%d}" % (i, "".join(parts), i, i))
    b = [shell(W, H), topbar(W, "toolbelt.bin", "160 bytes · every one of them printable")]
    b.append(t(x0, 68, "$", AMBER, 12))
    b.append(t(x0 + 2 * cw, 68, "hexdump -C toolbelt.bin", TEXT, 12))
    b.append('<g class="hl"><rect x="1" y="%d" width="%d" height="%d" fill="%s" fill-opacity=".07"/><rect x="1" y="%d" width="3" height="%d" fill="%s"/></g>' % (y0 - 16, W - 2, rh, AMBER, y0 - 16, rh, AMBER))
    for i, (txt, note) in enumerate(rows):
        y = y0 + i * rh
        hx = ["%02x" % ord(c) for c in txt]
        b.append(t(x0, y, "%08x" % (i * 16), FAINT, 12))
        b.append(t(x0 + 10 * cw, y, " ".join(hx[:8]) + "  " + " ".join(hx[8:]), MUT, 12))
        b.append(t(x0 + 60 * cw, y, "|", FAINT, 12))
        b.append(t(x0 + 61 * cw, y, txt, TEXT, 12, weight=700, cls="a a%d" % i))
        b.append(t(x0 + 77 * cw, y, "|", FAINT, 12))
        b.append(t(x0 + 81 * cw, y, note, FAINT, 11))
    b.append(t(x0, y0 + len(rows) * rh, "%08x" % (len(rows) * 16), FAINT, 12))
    svg("stack.svg", W, H, "Toolbelt as a hex dump: Burp Suite, Nmap, Metasploit, JADX, Wireshark, tshark, Python, FastAPI, Docker, OPA/Rego, scikit-learn, SQL, React, TypeScript, Apktool, Flutter, strongSwan, SHAP, Kali Linux, Git", "".join(b), st + "".join(kf))


# --------------------------------------------------------------------------------------------
# 6. Section bars, link buttons and the closing handshake.
# --------------------------------------------------------------------------------------------
def bars():
    data = [
        ("bar-capture.svg", "01", "THE CAPTURE", "two years in twelve frames"),
        ("bar-cases.svg", "02", "CASE FILES", "five public, one still in the lab"),
        ("bar-record.svg", "03", "THE RECORD", "one global certification, two national podiums"),
        ("bar-toolbelt.svg", "04", "TOOLBELT", "read the right-hand column"),
        ("bar-connect.svg", "05", "OPEN A CONNECTION", "three packets, then say hello"),
        ("bar-activity.svg", "06", "LIVE TRAFFIC", "the last year of commits, eaten daily"),
    ]
    W, H = 840, 44
    for i, (fname, num, title, note) in enumerate(data):
        st = css(".p{animation:p 7s linear infinite}@keyframes p{to{transform:translateX(1000px)}}")
        defs = (
            '<clipPath id="clip"><rect x="1" y="1" width="{w}" height="{h}" rx="9"/></clipPath>'
            '<linearGradient id="p" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="{a}" stop-opacity="0"/><stop offset="1" stop-color="{a}"/></linearGradient>'
        ).format(w=W - 2, h=H - 2, a=AMBER)
        b = [shell(W, H, 10)]
        b.append('<g clip-path="url(#clip)"><rect class="p" style="animation-delay:-%ss" x="-140" y="%d" width="140" height="2" fill="url(#p)"/></g>' % (n(i * 1.1), H - 3))
        b.append(t(20, 27, "// " + num, AMBER, 12, weight=700))
        b.append(t(74, 27, title, STRONG, 13, weight=700, ls=2.6))
        b.append(t(W - 20, 27, note, MUT, 11, anchor="end"))
        svg(fname, W, H, title.title(), "".join(b), st, defs)


def buttons():
    data = [
        ("btn-site.svg", "Portfolio", "prathameshtikle.tech"),
        ("btn-linkedin.svg", "LinkedIn", "in/prathamesh-tikle"),
        ("btn-tryhackme.svg", "TryHackMe", "77Pseudo · top 3%"),
        ("btn-email.svg", "Email", "tikle.prathamesh@gmail.com"),
    ]
    W, H = 204, 60
    for i, (fname, label, sub) in enumerate(data):
        st = css(".ar{animation:ar 1.4s ease-in-out infinite alternate}@keyframes ar{to{transform:translate(3px,-3px)}}")
        b = [shell(W, H, 10, PANE, LINE2)]
        b.append('<rect x="1" y="12" width="3" height="%d" rx="1.5" fill="%s"/>' % (H - 24, AMBER))
        b.append(t(18, 27, label, STRONG, 14, weight=700, cls="s"))
        b.append(t(18, 45, sub, MUT, 9.8))
        b.append('<g class="ar" style="animation-delay:%ss">%s</g>' % (n(i * 0.2), t(W - 16, 28, "↗", AMBER, 15, anchor="end", weight=700)))
        svg(fname, W, H, "%s: %s" % (label, sub), "".join(b), st)


def handshake():
    W, H = 840, 176
    xa, xb = 150, 690
    steps = [("SYN", True, 74), ("SYN, ACK", False, 106), ("ACK · connection open", True, 138)]
    st = [css(".ln{animation-duration:9s;animation-timing-function:ease-out;animation-iteration-count:infinite}")]
    b = [shell(W, H)]
    b.append(t(xa, 34, "you", STRONG, 12.5, anchor="middle", weight=700))
    b.append(t(xb, 34, "77Pseudo", AMBER, 12.5, anchor="middle", weight=700))
    for x in (xa, xb):
        b.append('<line x1="%d" y1="46" x2="%d" y2="%d" stroke="%s" stroke-dasharray="3 5"/>' % (x, x, H - 18, LINE2))
        b.append('<circle cx="%d" cy="46" r="3" fill="%s"/>' % (x, LINE2))
    for i, (label, forward, y) in enumerate(steps):
        a = 5 + i * 15  # start of the draw, as a percentage of the cycle
        z = a + 10
        st.append(
            "@keyframes d%d{0%%,%s{stroke-dashoffset:1;opacity:1}%s,90%%{stroke-dashoffset:0;opacity:1}96%%,100%%{stroke-dashoffset:0;opacity:0}}"
            "@keyframes f%d{0%%,%s{opacity:0}%s,90%%{opacity:1}96%%,100%%{opacity:0}}"
            ".d%d{animation-name:d%d}.f%d{animation-name:f%d}"
            % (i, pct(a), pct(z), i, pct(z - 3), pct(z), i, i, i, i)
        )
        colr = AMBER if not forward or i == 2 else TEXT
        if forward:
            d, head = "M%d %dH%d" % (xa + 8, y, xb - 12), "%d,%d %d,%d %d,%d" % (xb - 4, y, xb - 14, y - 5, xb - 14, y + 5)
        else:
            d, head = "M%d %dH%d" % (xb - 8, y, xa + 12), "%d,%d %d,%d %d,%d" % (xa + 4, y, xa + 14, y - 5, xa + 14, y + 5)
        b.append('<path class="ln d%d" d="%s" pathLength="1" stroke-dasharray="1" fill="none" stroke="%s" stroke-width="1.5"/>' % (i, d, colr))
        b.append('<polygon class="ln f%d" points="%s" fill="%s"/>' % (i, head, colr))
        b.append(t((xa + xb) / 2, y - 9, label, colr, 11.5, anchor="middle", weight=700, cls="ln f%d" % i))
    svg("handshake.svg", W, H, "A TCP three-way handshake between you and 77Pseudo: SYN, SYN-ACK, ACK. The connection is open.", "".join(b), "".join(st))


if __name__ == "__main__":
    hero()
    capture()
    cards()
    record()
    stack()
    bars()
    buttons()
    handshake()
