# -*- coding: utf-8 -*-
"""Schémas vectoriels du cours « Modélisation des actions mécaniques » (SVG en ligne, sans image externe).

Chaque schéma « réel → modèle » se compose de deux calques : `.reel` (l'objet réel, qui s'estompe) et `.modele`
(repère, droite d'action, vecteurs-forces, qui apparaissent) ; le bouton « Schématiser » de cours.js bascule de l'un
à l'autre. Les autres schémas sont statiques. Couleurs : forces en rouge, charges réparties en bleu, encre du gabarit.
"""
import math

ENCRE, ROUGE, BLEU, VERT, GRIS = "#1C2530", "#B42318", "#1F5FA8", "#1B7A43", "#7A848C"
ACIER, ACIER_C, CREME, SOL = "#7D8A96", "#A9B4BE", "#E8E2CF", "#D9D2B4"


def n(x):
    return f"{x:.1f}".rstrip("0").rstrip(".")


def defs(p, couleurs=(("r", ROUGE), ("k", ENCRE), ("b", BLEU))):
    """Pointes de flèche et hachures, identifiants préfixés (plusieurs SVG par page)."""
    mk = "".join(f'<marker id="{p}-{c}" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="13" markerHeight="13" markerUnits="userSpaceOnUse" '
                 f'orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{v}"/></marker>' for c, v in couleurs)
    return (f'<defs>{mk}<pattern id="{p}-h" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
            f'<rect width="7" height="7" fill="#F1F2EE"/><line x1="0" y1="0" x2="0" y2="7" stroke="#8A939A" stroke-width="1.6"/>'
            f'</pattern></defs>')


def fl(p, x1, y1, x2, y2, c="r", w=4, coul=None, extra=""):
    coul = coul or {"r": ROUGE, "k": ENCRE, "b": BLEU}[c]
    return (f'<line x1="{n(x1)}" y1="{n(y1)}" x2="{n(x2)}" y2="{n(y2)}" stroke="{coul}" stroke-width="{w}" '
            f'marker-end="url(#{p}-{c})"{extra}/>')


def vlab(x, y, lettre, ind="", coul=ENCRE, suite="", ancre="start"):
    """Nom de vecteur surmonté d'une flèche : lettre, indice, puis texte facultatif (intensité)."""
    larg = 10.5 * len(lettre) + 6.6 * len(ind)
    if ancre == "end":
        x -= larg + (7.2 * len(suite) + 6 if suite else 0)
    sub = f'<tspan font-size="11" dy="4">{ind}</tspan>' if ind else ""
    dy = ' dy="-4"' if ind else ""
    s = f'<tspan font-size="13" font-weight="500" dx="6"{dy}>{suite}</tspan>' if suite else ""
    return (f'<text x="{n(x)}" y="{n(y)}" class="g-lab" fill="{coul}">{lettre}{sub}{s}</text>'
            f'<path d="M{n(x)} {n(y - 16)}h{n(larg)}m-4 -3.5l4 3.5l-4 3.5" fill="none" stroke="{coul}" stroke-width="1.4"/>')


def txt(x, y, t, cls="g-lab-s", coul=None, ancre=None, extra=""):
    a = f' text-anchor="{ancre}"' if ancre else ""
    c = f' fill="{coul}"' if coul else ""
    return f'<text x="{n(x)}" y="{n(y)}" class="{cls}"{c}{a}{extra}>{t}</text>'


def renvoi(x1, y1, x2, y2, t, ancre="start", dy=4):
    """Ligne de rappel vers une pièce, terminée par un petit point, et son nom."""
    tx = x2 + (4 if ancre == "start" else -4)
    return (f'<circle cx="{n(x1)}" cy="{n(y1)}" r="2.2" fill="{ENCRE}"/><line x1="{n(x1)}" y1="{n(y1)}" x2="{n(x2)}" '
            f'y2="{n(y2)}" stroke="{ENCRE}" stroke-width="1"/>' + txt(tx, y2 + dy, t, "g-lab-s", ENCRE, ancre))


def arc(cx, cy, r, a1, a2, coul=ENCRE, w=1.6, p=None, fin=False):
    """Arc de cercle, angles en degrés dans le repère de l'écran (y vers le bas), de a1 vers a2."""
    x1, y1 = cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1))
    x2, y2 = cx + r * math.cos(math.radians(a2)), cy + r * math.sin(math.radians(a2))
    grand = 1 if abs(a2 - a1) > 180 else 0
    sens = 1 if a2 > a1 else 0
    m = f' marker-end="url(#{p}-k)"' if fin else ""
    return (f'<path d="M{n(x1)} {n(y1)}A{n(r)} {n(r)} 0 {grand} {sens} {n(x2)} {n(y2)}" fill="none" stroke="{coul}" '
            f'stroke-width="{w}"{m}/>')


def schema(svg, legende, bouton="Schématiser"):
    return (f'<figure class="schema" data-widget="schema"><div class="schema-zone">{svg}</div><figcaption>{legende}</figcaption>'
            f'<p class="schema-btns no-print"><button type="button" class="btn schema-go" aria-pressed="false">{bouton}'
            f'</button><span class="small">Passe du système réel à son modèle, et inversement.</span></p></figure>')


# ------------------------------------------------------------------------------------------------- câble sur une chape
def svg_cable():
    p = "sc"
    A = (215, 165)
    d = (math.cos(math.radians(30)), math.sin(math.radians(30)))
    nrm = (-d[1], d[0])

    def pt(t, o=0):
        return A[0] + t * d[0] + o * nrm[0], A[1] + t * d[1] + o * nrm[1]

    mur = (f'<rect x="26" y="18" width="24" height="296" fill="url(#{p}-h)"/>'
           f'<line x1="50" y1="18" x2="50" y2="314" stroke="{ENCRE}" stroke-width="2.5"/>')
    platine = f'<rect x="50" y="52" width="16" height="226" fill="#D7DDE2" stroke="{ENCRE}" stroke-width="2"/>'
    for yb in (84, 246):
        platine += (f'<rect x="66" y="{yb - 15}" width="14" height="30" fill="#C9CED2" stroke="{ENCRE}" stroke-width="1.6"/>'
                    f'<line x1="66" y1="{yb - 5}" x2="80" y2="{yb - 5}" stroke="{ENCRE}"/><line x1="66" y1="{yb + 5}" '
                    f'x2="80" y2="{yb + 5}" stroke="{ENCRE}"/><rect x="80" y="{yb - 6}" width="7" height="12" '
                    f'fill="#C9CED2" stroke="{ENCRE}" stroke-width="1.4"/>')
    chape = (f'<path d="M66 116L{A[0]} 133A32 32 0 0 1 {A[0]} 197L66 214Z" fill="{CREME}" stroke="{ENCRE}" stroke-width="2"/>'
             f'<line x1="36" y1="{A[1]}" x2="268" y2="{A[1]}" stroke="{GRIS}" stroke-width="1" stroke-dasharray="12 4 2 4"/>'
             f'<line x1="{A[0]}" y1="118" x2="{A[0]}" y2="212" stroke="{GRIS}" stroke-width="1" stroke-dasharray="12 4 2 4"/>')
    # câble : œillet autour de l'axe, puis toron torsadé
    s0, s1 = pt(22), pt(360)
    cable = (f'<circle cx="{A[0]}" cy="{A[1]}" r="19" fill="none" stroke="{ACIER}" stroke-width="8"/>'
             f'<line x1="{n(s0[0])}" y1="{n(s0[1])}" x2="{n(s1[0])}" y2="{n(s1[1])}" stroke="{ACIER}" stroke-width="14"/>'
             f'<line x1="{n(s0[0])}" y1="{n(s0[1])}" x2="{n(s1[0])}" y2="{n(s1[1])}" stroke="{ACIER_C}" stroke-width="8"/>')
    for k in range(int((360 - 30) / 8)):
        a, b = pt(30 + 8 * k + 3, 5), pt(30 + 8 * k - 3, -5)
        cable += f'<line x1="{n(a[0])}" y1="{n(a[1])}" x2="{n(b[0])}" y2="{n(b[1])}" stroke="#56636F" stroke-width="1.3"/>'
    axe = (f'<circle cx="{A[0]}" cy="{A[1]}" r="11" fill="#9AA2A8" stroke="{ENCRE}" stroke-width="1.8"/>'
           f'<circle cx="{A[0]}" cy="{A[1]}" r="3" fill="{ENCRE}"/>')
    noms = (txt(58, 38, "mur 0", "g-lab-s", ENCRE) + renvoi(150, 127, 168, 70, "support 1") +
            renvoi(*pt(140, -6), 400, 196, "câble 2 tendu") + renvoi(A[0] - 6, A[1] + 7, 150, 268, "axe lié à 1", "end"))
    # modèle
    i_ = pt(282)
    e_ = pt(150)
    modele = (f'<line x1="{A[0]}" y1="{A[1]}" x2="600" y2="{A[1]}" stroke="{ENCRE}" stroke-width="1.4" '
              f'stroke-dasharray="7 5" marker-end="url(#{p}-k)"/>' + txt(606, A[1] + 5, "x", "g-lab", ENCRE) +
              f'<line x1="{A[0]}" y1="{A[1]}" x2="{A[0]}" y2="36" stroke="{ENCRE}" stroke-width="1.4" stroke-dasharray="7 5" '
              f'marker-end="url(#{p}-k)"/>' + txt(A[0] + 8, 40, "y", "g-lab", ENCRE) +
              f'<line x1="{A[0]}" y1="{A[1]}" x2="{n(pt(330)[0])}" y2="{n(pt(330)[1])}" stroke="{ROUGE}" stroke-width="1.3" '
              f'stroke-dasharray="10 5"/>' + f'<circle cx="{n(i_[0])}" cy="{n(i_[1])}" r="3.5" fill="{ROUGE}"/>' +
              txt(i_[0] + 10, i_[1] - 2, "I", "g-lab", ROUGE) +
              arc(A[0], A[1], 100, 0, 30, ENCRE, 1.6, p, fin=True) + txt(322, 200, "30°", "g-lab", ENCRE) +
              fl(p, A[0], A[1], e_[0], e_[1], "r", 5) +
              f'<circle cx="{A[0]}" cy="{A[1]}" r="4.5" fill="{ROUGE}" stroke="#fff" stroke-width="1.5"/>' +
              txt(A[0] - 20, A[1] - 12, "A", "g-lab", ENCRE) +
              vlab(298, 270, "A", "2/1", ROUGE) + txt(298, 290, "(1 000 daN)", "g-lab-s", ROUGE))
    return (f'<svg viewBox="0 0 640 330" role="img" aria-label="Câble 2 tendu, accroché par un œillet à l\'axe de la chape '
            f'1 fixée au mur 0 ; schématisé par le vecteur-force A2/1 de 1 000 daN appliqué en A, incliné de 30° sous '
            f'l\'axe x, dirigé de A vers I">{defs(p)}<g class="reel">{mur}{platine}{chape}<g class="reel-att">{cable}'
            f'</g>{axe}<g class="reel-lab">{noms}</g></g><g class="modele">{modele}</g></svg>')


# ------------------------------------------------------------------------------------------------- tir dans un ballon
def _rot(pts, ang, ox, oy):
    c, s = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    return [(ox + x * c - y * s, oy + x * s + y * c) for x, y in pts]


def _poly(pts):
    return " ".join(f"{n(x)},{n(y)}" for x, y in pts)


def svg_ballon():
    p = "sb"
    G, R = (400, 160), 104
    d = (math.sin(math.radians(40)), -math.cos(math.radians(40)))          # de T vers K
    T = (G[0] - R * d[0], G[1] - R * d[1])
    K = (G[0] + (R + 40) * d[0], G[1] + (R + 40) * d[1])
    # ballon : pentagone central, cinq pentagones extérieurs, coutures ; découpé par le cercle
    def penta(cx, cy, r, a0):
        return [(cx + r * math.cos(math.radians(a0 + 72 * k)), cy + r * math.sin(math.radians(a0 + 72 * k))) for k in range(5)]
    motifs, coutures = [], []
    c0 = penta(G[0], G[1], 25, -90)
    motifs.append(c0)
    ext = []
    for i in range(5):
        a = -90 + 72 * i
        cx, cy = G[0] + 90 * math.cos(math.radians(a)), G[1] + 90 * math.sin(math.radians(a))
        pe = penta(cx, cy, 25, a + 180)
        ext.append(pe)
        motifs.append(pe)
        coutures.append((c0[i], pe[0]))
    for i in range(5):
        coutures.append((ext[i][1], ext[(i + 1) % 5][4]))
        coutures.append((ext[i][2], (ext[i][2][0] + (ext[i][2][0] - G[0]) * .6, ext[i][2][1] + (ext[i][2][1] - G[1]) * .6)))
    ballon = (f'<defs><radialGradient id="{p}-g" cx="38%" cy="32%" r="75%"><stop offset="0" stop-color="#fff"/>'
              f'<stop offset="1" stop-color="#D5DADF"/></radialGradient><clipPath id="{p}-c"><circle cx="{G[0]}" cy="{G[1]}" '
              f'r="{R - 1}"/></clipPath></defs><circle cx="{G[0]}" cy="{G[1]}" r="{R}" fill="url(#{p}-g)"/>'
              f'<g class="reel-att" clip-path="url(#{p}-c)">' +
              "".join(f'<line x1="{n(a[0])}" y1="{n(a[1])}" x2="{n(b[0])}" y2="{n(b[1])}" stroke="#5E6670" stroke-width="1.6"/>'
                      for a, b in coutures) +
              "".join(f'<polygon points="{_poly(m)}" fill="#2B3036"/>' for m in motifs) + '</g>'
              f'<circle cx="{G[0]}" cy="{G[1]}" r="{R}" fill="none" stroke="{ENCRE}" stroke-width="2.5"/>')
    # chaussure (repère local : bout en (0, 0), semelle vers +y), inclinée de −12°
    ox, oy, ang = T[0] - 3, T[1] + 4, -12
    tige = [(0, -4), (-6, -20), (-30, -30), (-62, -34), (-100, -50), (-112, -74), (-152, -76), (-166, -58),
            (-170, -26), (-164, 2), (-150, 8), (-12, 9)]
    semelle = [(-170, 0), (-164, 13), (-150, 18), (-10, 18), (2, 8), (0, -2), (-12, 7), (-150, 8)]
    jambe = [(-112, -72), (-152, -76), (-196, -250), (-140, -262)]
    chaussette = [(-115, -84), (-155, -88), (-163, -118), (-123, -116)]
    lacets = "".join(f'<line x1="{n(a[0])}" y1="{n(a[1])}" x2="{n(b[0])}" y2="{n(b[1])}" stroke="#fff" stroke-width="2.2"/>'
                     for a, b in zip(_rot([(-48 - 13 * k, -38 - 4.5 * k) for k in range(4)], ang, ox, oy),
                                     _rot([(-40 - 13 * k, -26 - 4.5 * k) for k in range(4)], ang, ox, oy)))
    crampons = "".join(f'<polygon points="{_poly(_rot([(x - 5, 18), (x + 5, 18), (x + 3, 26), (x - 3, 26)], ang, ox, oy))}" '
                       f'fill="#46525C"/>' for x in (-22, -50, -128, -152))
    pied = (f'<polygon points="{_poly(_rot(jambe, ang, ox, oy))}" fill="#E7C29E" stroke="{ENCRE}" stroke-width="1.8"/>'
            f'<polygon points="{_poly(_rot(chaussette, ang, ox, oy))}" fill="#fff" stroke="{ENCRE}" stroke-width="1.5"/>'
            f'<polygon points="{_poly(_rot(chaussette, ang, ox, oy))}" fill="none" stroke="{BLEU}" stroke-width="4" '
            f'stroke-dasharray="0 10 30 200"/>'
            f'<polygon points="{_poly(_rot(semelle, ang, ox, oy))}" fill="#9AA2A8" stroke="{ENCRE}" stroke-width="1.6"/>'
            f'{crampons}<polygon points="{_poly(_rot(tige, ang, ox, oy))}" fill="#2F3A44" stroke="{ENCRE}" stroke-width="2"/>'
            f'{lacets}')
    noms = (renvoi(*_rot([(-90, -10)], ang, ox, oy)[0], 150, 312, "pied 2", "end") +
            renvoi(G[0] + 60, G[1] + 72, 545, 300, "ballon 1") + txt(T[0] - 6, T[1] - 14, "T", "g-lab", ENCRE, "end"))
    ech = 6                                                                  # px par newton
    e_T = (T[0] + 15 * ech * d[0], T[1] + 15 * ech * d[1])
    bas = (T[0] - 75 * d[0], T[1] - 75 * d[1])
    modele = (f'<line x1="{G[0]}" y1="318" x2="{G[0]}" y2="22" stroke="{ENCRE}" stroke-width="1.4" stroke-dasharray="7 5" '
              f'marker-end="url(#{p}-k)"/>' + txt(G[0] + 8, 26, "y", "g-lab", ENCRE) +
              f'<line x1="260" y1="{G[1]}" x2="594" y2="{G[1]}" stroke="{ENCRE}" stroke-width="1.4" stroke-dasharray="7 5" '
              f'marker-end="url(#{p}-k)"/>' + txt(598, G[1] + 5, "x", "g-lab", ENCRE) +
              f'<line x1="{n(bas[0])}" y1="{n(bas[1])}" x2="{n(K[0])}" y2="{n(K[1])}" stroke="{ROUGE}" stroke-width="1.3" '
              f'stroke-dasharray="10 5"/><circle cx="{n(K[0])}" cy="{n(K[1])}" r="3.5" fill="{ROUGE}"/>' +
              txt(K[0] + 10, K[1] + 2, "K", "g-lab", ROUGE) +
              f'<line x1="{n(T[0])}" y1="{n(T[1])}" x2="{n(T[0])}" y2="330" stroke="{ENCRE}" stroke-width="1.2" '
              f'stroke-dasharray="3 4"/>' + txt(T[0] - 8, 326, "verticale", "g-lab-s", ENCRE, "end") +
              arc(T[0], T[1], 46, 90, 130, ENCRE, 1.6, p, fin=True) +
              txt(T[0] - 36, T[1] + 64, "40°", "g-lab", ENCRE, "middle") +
              fl(p, T[0], T[1], e_T[0], e_T[1], "r", 5) +
              f'<circle cx="{n(T[0])}" cy="{n(T[1])}" r="4.5" fill="{ROUGE}" stroke="#fff" stroke-width="1.5"/>' +
              txt(T[0] - 6, T[1] - 14, "T", "g-lab", ENCRE, "end") +
              vlab(T[0] - 40, T[1] - 40, "T", "2/1", ROUGE, "", "end") + txt(T[0] - 40, T[1] - 22, "(15 N)", "g-lab-s", ROUGE, "end") +
              fl(p, G[0], G[1], G[0], G[1] + 5 * ech + 6, "r", 5) +
              f'<path d="M{G[0] - 5} {G[1] - 5}l10 10m0 -10l-10 10" stroke="{ENCRE}" stroke-width="2"/>' +
              txt(G[0] + 10, G[1] - 8, "G", "g-lab", ENCRE) + vlab(G[0] + 12, G[1] + 40, "P", "1", ROUGE, "(5 N)"))
    return (f'<svg viewBox="0 0 620 340" role="img" aria-label="Pied 2 frappant le ballon 1 au point T ; schématisation : '
            f'force T2/1 de 15 N appliquée en T, inclinée de 40° sur la verticale, dirigée de T vers K ; poids P1 de 5 N, '
            f'vertical vers le bas, appliqué au centre de gravité G">{defs(p)}<g class="reel"><g class="reel-att">{pied}</g>'
            f'{ballon}<g class="reel-lab">{noms}</g></g><g class="modele">{modele}</g></svg>')


# ------------------------------------------------------------------------------------------------- trois types de contact
def _plan(p, x1, x2, y, h=14):
    return (f'<rect x="{x1}" y="{y}" width="{x2 - x1}" height="{h}" fill="url(#{p}-h)"/>'
            f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{ENCRE}" stroke-width="2.2"/>')


def svg_contacts():
    """Trois petits schémas : action concentrée (bille), linéique (cylindre couché), surfacique (cube)."""
    out = []
    p = "c1"
    out.append((f'<svg viewBox="0 0 240 222" role="img" aria-label="Bille 1 posée sur le plan 0 : contact au point A, '
                f'action schématisée par le vecteur-force A0/1 vertical">{defs(p)}' + _plan(p, 20, 220, 160) +
                f'<circle cx="120" cy="104" r="56" fill="#E1E7EC" stroke="{ENCRE}" stroke-width="2.2"/>'
                f'<path d="M115 99l10 10m0 -10l-10 10" stroke="{ENCRE}" stroke-width="1.8"/>' +
                txt(130, 98, "G", "g-lab", ENCRE) + fl(p, 120, 160, 120, 110, "r", 4.5) +
                f'<circle cx="120" cy="160" r="4" fill="{ROUGE}" stroke="#fff" stroke-width="1.4"/>' +
                txt(108, 182, "A", "g-lab", ENCRE, "end") + vlab(128, 146, "A", "0/1", ROUGE) +
                txt(176, 60, "1", "g-lab", ENCRE) + txt(28, 192, "0", "g-lab", ENCRE) + '</svg>',
                "<b>Concentrée</b> : contact en un point A → un vecteur-force (N)."))
    p = "c2"
    fleches = "".join(fl(p, x, 196, x, 162, "b", 2) for x in range(46, 199, 17))
    out.append((f'<svg viewBox="0 0 240 222" role="img" aria-label="Cylindre 1 couché sur le plan 0 : contact le long du '
                f'segment AB, action schématisée par une charge linéique q uniforme">{defs(p)}' + _plan(p, 14, 226, 160) +
                f'<path d="M46 90H194A13 35 0 0 1 194 160H46Z" fill="#E1E7EC" stroke="{ENCRE}" stroke-width="2.2"/>'
                f'<ellipse cx="46" cy="125" rx="13" ry="35" fill="#C9D3DB" stroke="{ENCRE}" stroke-width="2.2"/>'
                f'<line x1="46" y1="160" x2="194" y2="160" stroke="{BLEU}" stroke-width="4"/>' + fleches +
                f'<line x1="46" y1="196" x2="194" y2="196" stroke="{BLEU}" stroke-width="2"/>' +
                txt(30, 156, "A", "g-lab", ENCRE, "end") + txt(212, 156, "B", "g-lab", ENCRE) +
                txt(120, 116, "1", "g-lab", ENCRE, "middle") + txt(20, 186, "0", "g-lab", ENCRE) +
                txt(120, 216, "q (N/m)", "g-lab-s", BLEU, "middle", ' font-weight="700"') + '</svg>',
                "<b>Linéique</b> : contact le long d'une ligne AB → charge q (N/m)."))
    p = "c3"
    fleches = "".join(fl(p, x, 194, x, 162, "b", 2) for x in range(64, 147, 13))
    out.append((f'<svg viewBox="0 0 240 222" role="img" aria-label="Cube 1 posé sur le plan 0 : contact sur toute la base, '
                f'action schématisée par une pression p uniforme">{defs(p)}' + _plan(p, 14, 226, 160) +
                f'<polygon points="142,68 182,40 182,132 142,160" fill="#C9D3DB" stroke="{ENCRE}" stroke-width="2.2"/>'
                f'<polygon points="64,68 104,40 182,40 142,68" fill="#EEF1F4" stroke="{ENCRE}" stroke-width="2.2"/>'
                f'<rect x="64" y="68" width="78" height="92" fill="#E1E7EC" stroke="{ENCRE}" stroke-width="2.2"/>'
                f'<line x1="64" y1="160" x2="142" y2="160" stroke="{BLEU}" stroke-width="4"/>' + fleches +
                f'<line x1="64" y1="194" x2="142" y2="194" stroke="{BLEU}" stroke-width="2"/>' +
                txt(103, 120, "1", "g-lab", ENCRE, "middle") + txt(20, 186, "0", "g-lab", ENCRE) +
                txt(103, 216, "p (Pa)", "g-lab-s", BLEU, "middle", ' font-weight="700"') + '</svg>',
                "<b>Surfacique</b> : contact sur une surface → pression p (Pa)."))
    return ('<div class="schemas3">' + "".join(f'<figure>{s}<figcaption>{c}</figcaption></figure>' for s, c in out) +
            '</div>')


# ------------------------------------------------------------------------------------------------- coordonnées du câble
def svg_cable_coord():
    p = "cc"
    A, L = (70, 56), 230
    E = (A[0] + L * math.cos(math.radians(30)), A[1] + L * math.sin(math.radians(30)))
    return (f'<svg viewBox="0 0 400 206" role="img" aria-label="Coordonnées de A2/1 : Ax = 866 daN suivant x, Ay = −500 daN '
            f'suivant y">{defs(p, (("r", ROUGE), ("k", ENCRE), ("b", BLEU), ("v", VERT)))}'
            f'<line x1="{A[0]}" y1="{A[1]}" x2="380" y2="{A[1]}" stroke="{ENCRE}" stroke-width="1.3" marker-end="url(#{p}-k)"/>'
            + txt(384, A[1] + 5, "x", "g-lab", ENCRE) +
            f'<line x1="{A[0]}" y1="200" x2="{A[0]}" y2="14" stroke="{ENCRE}" stroke-width="1.3" marker-end="url(#{p}-k)"/>'
            + txt(A[0] + 8, 18, "y", "g-lab", ENCRE) +
            f'<line x1="{n(E[0])}" y1="{n(E[1])}" x2="{n(E[0])}" y2="{A[1]}" stroke="{GRIS}" stroke-dasharray="5 4"/>'
            f'<line x1="{n(E[0])}" y1="{n(E[1])}" x2="{A[0]}" y2="{n(E[1])}" stroke="{GRIS}" stroke-dasharray="5 4"/>' +
            fl(p, A[0], A[1], E[0], A[1], "r", 5) + fl(p, A[0], A[1], A[0], E[1], "b", 5) +
            fl(p, A[0], A[1], E[0], E[1], "v", 4.5, VERT) + arc(A[0], A[1], 70, 0, 30, ENCRE, 1.5, p, fin=True) +
            txt(150, 86, "30°", "g-lab", ENCRE) + txt(A[0] - 10, A[1] - 8, "A", "g-lab", ENCRE, "end") +
            vlab(170, 40, "A", "x", ROUGE, "= 866 daN") + vlab(A[0] - 8, 150, "A", "y", BLEU, "", "end") +
            txt(A[0] - 8, 170, "= −500 daN", "g-lab-s", BLEU, "end", ' font-weight="700"') +
            vlab(150, 152, "A", "2/1", VERT) + txt(128, 192, "(1 000 daN)", "g-lab-s", VERT, extra=' font-weight="700"') + '</svg>')
