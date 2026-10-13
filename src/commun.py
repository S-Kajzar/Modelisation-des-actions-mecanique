# -*- coding: utf-8 -*-
"""Outils communs aux pages construites sur le gabarit (exercices) et aux pages de cours.

Une page d'exercice se décrit par une liste de parties (titre, durée conseillée, introduction, figures, questions) ;
construire_exercice() l'injecte dans le gabarit sans toucher à son bloc de style ni à ses moteurs.

Types de questions :
  - question simple (par défaut) : un champ, un bouton « Valider », un correcteur du moteur (num, kw, code…) ;
  - torseur (type="torseur") : six cases X Y Z / L M N validées d'un bloc (mécanique « fast-q » du gabarit),
    chaque case notée juste ou fausse ;
  - vecteur (type="vecteur") : un ou plusieurs vecteurs écrits en colonne, une case par composante (nombre ou
    expression littérale), validés d'un bloc comme un torseur.
Vecteurs et torseurs reprennent la notation de l'exercice « Déplacer un torseur » : colonnes entre parenthèses
(sans nom de ligne pour un vecteur, nom de la case au-dessus pour un torseur), valeur attendue sous chaque case fausse.
"""
import base64
import html
import json
import pathlib
from decimal import Decimal, ROUND_HALF_UP
from struct import unpack

ROOT = pathlib.Path(__file__).resolve().parent.parent
GABARIT = ROOT / "src" / "gabarit-exercice-interactif.html"
IMAGES = ROOT / "src" / "images"

Q = dict
UNITE = "Saisis la valeur <strong>avec son unité</strong> : l'unité vaut la moitié des points de la question."

# ---------------------------------------------------------------- unités (le moteur normalise la saisie)
U_N = {"label": "N", "accept": ["n", "newton", "newtons"]}
U_DAN = {"label": "daN", "accept": ["dan", "decanewton", "decanewtons"]}
U_KN = {"label": "kN", "accept": ["kn", "kilonewton", "kilonewtons"]}
U_NM = {"label": "N·m", "accept": ["nm", "newtonmetre", "newtonmetres"]}
U_NMM = {"label": "N·mm", "accept": ["nmm", "newtonmillimetre", "newtonmillimetres"]}
U_DANM = {"label": "daN·m", "accept": ["danm", "decanewtonmetre", "decanewtonmetres"]}
U_DANMM = {"label": "daN·mm", "accept": ["danmm"]}
U_M = {"label": "m", "accept": ["m", "metre", "metres"]}
U_MM = {"label": "mm", "accept": ["mm", "millimetre", "millimetres"]}
U_KG = {"label": "kg", "accept": ["kg", "kilogramme", "kilogrammes", "kilo", "kilos"]}
U_DEG = {"label": "°", "accept": ["°", "deg", "degre", "degres"]}


def num(value, tol, unit=None, abs_=False, variants=()):
    """Correcteur numérique ; variants : autres (valeur, tolérance, unité) acceptées, par exemple en N·mm."""
    g = {"type": "num", "value": value, "absTol": tol}
    if unit:
        g["unit"] = unit
    if abs_:
        g["abs"] = True
    if variants:
        # variante = même grandeur dans une autre unité : retenue seulement si cette unité est écrite
        # (« 12 N·m » ne vaut rien quand on attend 120 N·m ou 12 daN·m)
        g["variants"] = [dict({"value": v, "absTol": t, "unit": u, "strictUnit": True}, **({"abs": True} if abs_ else {}))
                         for v, t, u in variants]
    return g


def kw(any_, forbid=None):
    g = {"type": "kw", "any": any_}
    if forbid:
        g["forbid"] = forbid
    return g


def code(contains=(), equals=(), reject_raw=(), reject_contains=()):
    g = {"type": "code"}
    if contains:
        g["contains"] = list(contains)
    if equals:
        g["equals"] = list(equals)
    if reject_raw:
        g["rejectRaw"] = list(reject_raw)
    if reject_contains:
        g["rejectContains"] = list(reject_contains)
    return g


def expr(expected, vars_, names, require=()):
    """Formule littérale : juste si elle vaut l'expression attendue pour chaque jeu de valeurs de vars_."""
    g = {"type": "expr", "expected": expected, "vars": vars_, "names": names}
    if require:
        g["require"] = list(require)
    return g


# ---------------------------------------------------------------- vecteurs en colonne (type="vecteur")
H_VEC = ("Écris le vecteur en colonne : une case par coordonnée, nombre seul avec son signe (zéros compris) ; "
         "l'unité est indiquée à droite du vecteur.")


def VEC(lettre):
    """Nom de vecteur surmonté d'une flèche (classe .vec du gabarit)."""
    return f'<span class="vec">{lettre}</span>'


def VI(nom, comps, unite="", lit=False):
    """Un vecteur à compléter : nom affiché, composantes [(étiquette, correcteur, texte attendu)…], unité."""
    return {"nom": nom, "comps": list(comps), "unite": unite, "lit": lit}


def cn(lab, v, tol=0.01, d=2):
    """Composante numérique d'un vecteur : nombre seul (l'unité est donnée par le vecteur)."""
    return (lab, num(v, tol), nb(v, d))


def VQ(s, e, *items, h=H_VEC, pts=1):
    """Question « vecteur(s) en colonne » : chaque case vaut pts point(s)."""
    return {"type": "vecteur", "s": s, "h": h, "e": e, "items": list(items), "pts_case": pts}


YES = {"type": "yesno", "value": True}
NO = {"type": "yesno", "value": False}


# ---------------------------------------------------------------- outils
def esc(s):
    return html.escape(s, quote=True)


def chemin(f, base=IMAGES):
    p = pathlib.Path(f)
    return p if p.is_absolute() else base / p


def data_uri(f, base=IMAGES):
    p = chemin(f, base)
    mime = "image/jpeg" if p.suffix == ".jpg" else ("image/svg+xml" if p.suffix == ".svg" else "image/png")
    return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()


def taille(f, base=IMAGES):
    p = chemin(f, base)
    d = p.read_bytes()
    if p.suffix == ".svg":  # dimensions lues sur la balise racine
        import re
        m = re.search(rb'<svg[^>]*\swidth="(\d+)"[^>]*\sheight="(\d+)"', d)
        return int(m.group(1)), int(m.group(2))
    if p.suffix == ".png":
        return unpack(">II", d[16:24])
    i = 2
    while i < len(d):  # JPEG : cherche le marqueur SOF
        m, l = d[i + 1], int.from_bytes(d[i + 2:i + 4], "big")
        if 0xC0 <= m <= 0xC3:
            return unpack(">HH", d[i + 5:i + 9])[::-1]
        i += 2 + l
    raise ValueError(p)


def fig(nom, alt, w, cap=""):
    return Q(f=nom, alt=alt, w=w, cap=cap)


def figure(f, base=IMAGES):
    w, h = taille(f["f"], base)
    cap = f'<figcaption>{f["cap"]}</figcaption>' if f.get("cap") else ""
    return (f'<figure class="q-fig" style="max-width:{f["w"]}px"><img src="{data_uri(f["f"], base)}" alt="{esc(f["alt"])}" '
            f'width="{w}" height="{h}">{cap}</figure>')


def fr1(x):
    return str(Decimal(str(x)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)).replace(".", ",")


def frn(x, d=2):
    """Nombre au format français, d décimales, espace fine insécable pour les milliers."""
    s = f"{x:,.{d}f}".replace(",", " ").replace(".", ",")
    return s.replace("-", "−")


def nb(v, d=2):
    """Valeur affichée : entier sans décimale, sinon d décimales."""
    return frn(v, 0) if abs(v - round(v)) < 1e-9 else frn(v, d)


def duree(m):
    return f"{m} min" if m < 60 else f"{m // 60} h {m % 60:02d}"


def pts_txt(p):
    v = fr1(p).replace(",0", "")
    return f"{v} point{'s' if p > 1 else ''}"


# ---------------------------------------------------------------- torseurs
TQ_RES, TQ_MOM = ("X", "Y", "Z"), ("L", "M", "N")


def torseur_html(cells, point, nom=""):
    """Torseur affiché {X L ; Y M ; Z N}_point ; cells : 6 textes HTML dans l'ordre X, L, Y, M, Z, N."""
    rows = "".join(f'<span class="tm-c">{cells[2 * i]}</span><span class="tm-c">{cells[2 * i + 1]}</span>' for i in range(3))
    tete = f'<span class="tm-nom">{nom} =</span>' if nom else ""
    return (f'<span class="tm">{tete}<span class="tm-b" aria-hidden="true">{{</span><span class="tm-g">{rows}</span>'
            f'<span class="tm-b" aria-hidden="true">}}</span><sub class="tm-p">{point}</sub></span>')


def question(pid, n, q, cfg):
    qid, label = f"q{pid}_{n}", f"Q{pid}.{n}"
    cfg[qid] = {"label": label, "part": str(pid), "pts": q.get("pts", 1), "grader": q["g"]}
    return f"""
        <div class="q" id="{qid}" data-q="{qid}">
          <p class="q-stem"><span class="q-num">{label}</span> <strong>{q["s"]}</strong></p>
          <p class="q-hint" id="h-{qid}">{q["h"]}</p>
          <div class="q-row">
            <input type="text" class="q-input" id="in-{qid}" aria-label="Réponse {label}" aria-describedby="h-{qid}" autocomplete="off" autocapitalize="off" spellcheck="false">
            <button type="button" class="btn btn-validate">Valider</button>
            <span class="q-status" aria-live="polite"></span>
            <span class="print-only pstat">Non validée : comptée fausse</span>
          </div>
          <p class="q-msg" role="alert"></p>
          <div class="q-expl" hidden>
            <p class="q-unit-msg" hidden></p>
            <p class="q-expected"><span>Réponse attendue :</span> {q["att"]}</p>
            <div class="q-why"><p>{q["e"]}</p></div>
          </div>
        </div>"""


def colonne(cellules, etiquettes=None):
    """Colonne entre parenthèses arrondies ; une étiquette (x, y, z…) à gauche de chaque ligne si fournie."""
    lignes = "".join("<tr>" + (f'<td class="vl">{etiquettes[i]}</td>' if etiquettes else "") + f"<td>{c}</td></tr>"
                     for i, c in enumerate(cellules))
    return f'<span class="vcol-b"><table>{lignes}</table></span>'


def vecteur_col(nom, cellules, unite=""):
    """Vecteur écrit en colonne, sans nom de ligne dans les parenthèses (l'ordre x, y, z suffit)."""
    u = f'<span class="vcol-u">{unite}</span>' if unite else ""
    return f'<span class="vcol"><span class="vcol-n">{nom} =</span>{colonne(cellules)}{u}</span>'


def torseur_col(cells, point, nom=""):
    """Torseur {X L ; Y M ; Z N} écrit en deux colonnes entre parenthèses ; cells dans l'ordre X, L, Y, M, Z, N."""
    nom = nom or "{<i>T</i>}"
    lignes = "".join(f"<tr><td>{cells[2 * i]}</td><td>{cells[2 * i + 1]}</td></tr>" for i in range(3))
    return (f'<span class="tzv"><span class="tzv-n">{nom}<sub>{point}</sub> =</span><span class="vcol-b"><table>{lignes}'
            f'</table></span><span class="tzv-r">({point}, x, y, z)</span></span>')


def case(cid, aria, attendu, etiquette="", lit=False):
    """Case de saisie d'un groupe : nom au-dessus (facultatif), valeur attendue affichée si la case est fausse."""
    lab = f'<span class="cq-lab">{etiquette}</span>' if etiquette else ""
    extra = 'autocapitalize="off" spellcheck="false"' if lit else 'inputmode="decimal" autocapitalize="off" spellcheck="false"'
    return (f'<label class="sol{" lit" if lit else ""}">{lab}<input type="text" data-q="{cid}" aria-label="{esc(aria)}" '
            f'autocomplete="off" {extra}><span class="mark" aria-live="polite"></span><span class="att">→ {attendu}</span></label>')


def bloc_groupe(qid, label, q, saisie, attendu, n, bouton, fait):
    return f"""
        <div class="fast-q cq" id="{qid}">
          <p class="q-stem"><span class="q-num">{label}</span> <strong>{q["s"]}</strong></p>
          <p class="q-hint">{q["h"]}</p>
          <div class="cq-items">{saisie}</div>
          <div class="fast-foot"><button type="button" class="btn btn-fast" data-done="{fait}">{bouton}</button>
            <span class="q-status" aria-live="polite"></span></div>
          <p class="q-msg" role="alert"></p>
          <div class="q-expl" hidden>
            <p class="q-expected"><span>Réponse attendue :</span></p>
            <div class="cq-items">{attendu}</div>
            <div class="q-why"><p>{q["e"]}</p></div>
          </div>
        </div>"""


def question_torseur(pid, n, q, cfg):
    """q : s (énoncé), h (consigne), nom (ex. « {T<sub>F</sub>} »), point, vals (6 valeurs X L Y M Z N),
    tol (tolérance absolue, ou liste de 6), pts_case, e (démarche), aff (textes attendus, facultatif)."""
    qid, label = f"q{pid}_{n}", f"Q{pid}.{n}"
    tols = q["tol"] if isinstance(q["tol"], (list, tuple)) else [q["tol"]] * 6
    noms = ("X", "L", "Y", "M", "Z", "N")
    textes = [nb(v, q.get("dec", 2)) if not isinstance(v, str) else v for v in q.get("aff", q["vals"])]
    cases = []
    for c, v, tl, att in zip(noms, q["vals"], tols, textes):
        cid = f"{qid}_{c}"
        cfg[cid] = {"label": f"{label} {c}", "part": str(pid), "pts": q.get("pts_case", 0.5),
                    "grader": num(v, tl, abs_=False)}
        cases.append(case(cid, f"{label}, composante {c}", att, c))
    return bloc_groupe(qid, label, q, torseur_col(cases, q["point"], q["nom"]), torseur_col(textes, q["point"], q["nom"]),
                       6, "Valider le torseur", "Torseur validé")


def question_vecteur(pid, n, q, cfg):
    """q : s, h, e, items = [Q(nom, unite, comps=[(étiquette, correcteur, texte attendu)…], lit)], pts_case (1 par défaut).
    Chaque vecteur s'écrit en colonne ; lit=True pour une colonne d'expressions littérales (cases plus larges)."""
    qid, label = f"q{pid}_{n}", f"Q{pid}.{n}"
    saisie, attendu, k = [], [], 0
    for it in q["items"]:
        cases, textes = [], []
        for lab, g, att in it["comps"]:
            k += 1
            cid = f"{qid}_{k}"
            cfg[cid] = {"label": f"{label} {lab}", "part": str(pid), "pts": q.get("pts_case", 1), "grader": g}
            nom_txt = it["nom"].replace("<sub>", "").replace("</sub>", "")
            cases.append(case(cid, f"{label}, {nom_txt}, composante {lab}", att, lit=it.get("lit", False)))
            textes.append(att)
        saisie.append(vecteur_col(it["nom"], cases, it.get("unite", "")))
        attendu.append(vecteur_col(it["nom"], textes, it.get("unite", "")))
    return bloc_groupe(qid, label, q, "".join(saisie), "".join(attendu), k,
                       "Valider le vecteur" if len(q["items"]) == 1 else "Valider les vecteurs", "Vecteur validé")


def nb_cases(q):
    if q.get("type") == "torseur":
        return 6
    if q.get("type") == "vecteur":
        return sum(len(it["comps"]) for it in q["items"])
    return 0


def points_question(q):
    if q.get("type") == "torseur":
        return q.get("pts_case", 0.5) * 6
    if q.get("type") == "vecteur":
        return q.get("pts_case", 1) * nb_cases(q)
    return q.get("pts", 1)


# ---------------------------------------------------------------- parties et page
METHODE_CHIP = ('<p class="only-training small">Besoin d\'un rappel ? <button type="button" class="doc-chip training-only" '
                'data-doc="METH" aria-pressed="false">Méthode</button></p>')


def partie(pid, p, total, cfg, base=IMAGES):
    blocs = p.get("blocs") or [Q(questions=p["questions"], fig=p.get("fig"), html=p.get("html"))]
    points = sum(points_question(q) for b in blocs for q in b["questions"])
    nq = sum(len(b["questions"]) for b in blocs)
    pct = fr1(Decimal(p["minutes"]) * 100 / total)
    body, n = [], 0
    body.append(p["intro"] if p["intro"].lstrip().startswith("<") else f'<p>{p["intro"]}</p>')
    body.append(METHODE_CHIP)
    for b in blocs:
        if b.get("sub"):
            body.append(f'<h3 class="sub-head">{b["sub"]}</h3>' + (f'<p>{b["intro"]}</p>' if b.get("intro") else ""))
        if b.get("fig"):
            body.append(figure(b["fig"], base))
        if b.get("html"):
            body.append(b["html"])
        for q in b["questions"]:
            n += 1
            if q.get("fig"):
                body.append(figure(q["fig"], base))
            if q.get("avant"):
                body.append(q["avant"])
            fab = {"torseur": question_torseur, "vecteur": question_vecteur}.get(q.get("type"), question)
            body.append(fab(pid, n, q, cfg))
    return nq, points, f"""
  <section class="part" id="partie-{pid}" aria-labelledby="t-partie-{pid}">
    <header class="part-head"><div class="part-num" aria-hidden="true">{pid}</div>
      <div><h2 id="t-partie-{pid}"><span class="sr-only">Partie {pid} : </span>{p["titre"]}</h2>
        <div class="duree">Durée conseillée : {duree(p["minutes"])} · Barème : {pts_txt(points)}, soit {pct} % de la note</div></div></header>
    <div class="part-body">
      {"".join(body)}
    </div>
  </section>
"""


CONSIGNE_COLONNE = ("<p><strong>Les vecteurs s'écrivent en colonne</strong>, entre parenthèses, une case par coordonnée "
                    "(x, y, z) : nombre seul avec son signe, zéros compris ; l'unité est indiquée à droite du vecteur. Les "
                    "cases se valident d'un bloc, chaque case juste rapporte ses points. Après validation, la valeur "
                    "attendue s'affiche en vert sous chaque case fausse.</p>")
CONSIGNE_UNITES = ("<p><strong>Les unités sont notées.</strong> Pour toute question numérique portant une unité, la valeur "
                   "vaut la moitié des points et l'unité l'autre moitié : une valeur juste écrite sans unité, ou avec une "
                   "unité fausse, ne rapporte qu'un demi-point.</p>")


def construire_exercice(*, titre, description, sous_titre, parties, methode_titre, methode, hero, facts, sortie,
                        script, consignes=(CONSIGNE_UNITES,), cartouche=None, base=IMAGES, nq_attendu=None, config_js=""):
    """Écrit la page d'exercice : gabarit + accueil + parties + configuration du moteur.

    config_js : script exécuté juste après la configuration et avant les moteurs ; il peut réécrire
    window.__QCFG__ et remplir la page (exercice à valeurs tirées au hasard, par exemple)."""
    g = GABARIT.read_text(encoding="utf-8")
    total = sum(p["minutes"] for p in parties)
    cfg, parts_cfg, sections, nq_total = {}, [], [], 0
    for i, p in enumerate(parties, 1):
        nq, pts, sec = partie(i, p, total, cfg, base)
        nq_total += nq
        sections.append(sec)
        parts_cfg.append({"num": str(i), "title": p["titre"], "minutes": p["minutes"], "duration": duree(p["minutes"]),
                          "points": pts})
    if nq_attendu is not None:
        assert nq_total == nq_attendu, (nq_total, nq_attendu)
    dur_totale = duree(total)

    i0, i1 = g.index("<!-- ====="), g.index("=== -->") + len("=== -->")
    g = g[:i0] + f"<!-- Page construite par src/{script} à partir du gabarit : ne pas modifier à la main. -->" + g[i1:]
    t0, t1 = g.index("<title>"), g.index("<style>:root{")
    g = g[:t0] + (f"<title>{titre} — exercice interactif</title>\n"
                  f'<meta name="description" content="{html.escape(description, quote=False).replace(chr(34), "&quot;")}">\n') + g[t1:]
    a0, a1 = g.index("<!-- RAIL DES DOCUMENTS"), g.index('<main class="page">')
    hw, hh = taille(hero["f"], base)
    faits = "\n".join(f"      <div><b>{b}</b><span>{s}</span></div>" for b, s in facts)
    accueil = f"""<!-- RAIL DES DOCUMENTS : la méthode est une aide du mode entraînement (classe training-only) -->
<nav class="rail" aria-label="Méthode">
  <button type="button" class="tab dt meth training-only" data-doc="METH" aria-selected="false" title="Méthode (mode entraînement uniquement)">Méthode</button>
</nav>

<aside id="docpanel" aria-label="Documents du sujet" aria-hidden="true">
  <div class="dp-head">
    <h3 id="dp-title">Documents</h3>
    <button type="button" id="dp-out" aria-label="Réduire">−</button><span id="dp-zoom" class="small">100 %</span>
    <button type="button" id="dp-in" aria-label="Agrandir">+</button>
    <button type="button" id="dp-fit">Ajuster</button>
    <button type="button" id="dp-close">Fermer</button>
  </div>
  <div class="dp-tabs" role="tablist" aria-label="Choisir un document">
    <button type="button" class="training-only" data-doc="METH" aria-selected="false">Méthode</button>
  </div>
  <div class="dp-body">
    <section class="doc training-only" id="doc-METH" data-title="Méthode : {methode_titre}" data-kind="Rappel de méthode · mode entraînement">
      <div class="doc-text">{methode}</div>
    </section>
  </div>
</aside>

<!-- PAGE D'ACCUEIL -->
<section id="home" aria-labelledby="home-title">
  <div class="home-inner">
    <header class="home-head">
      <h1 id="home-title">{titre}</h1>
      <p class="home-sub">{sous_titre}</p>
    </header>
    <figure class="home-hero">
      <img src="{data_uri(hero["f"], base)}" alt="{esc(hero["alt"])}" width="{hw}" height="{hh}">
      <figcaption>{hero["cap"]}</figcaption>
    </figure>
    <div class="home-facts">
{faits}
    </div>
    <h2 class="home-choose">Choisis ton mode de travail</h2>
    <div class="modes">
      <article class="mode-card">
        <div class="mc-head"><span class="mc-tag">Mode 1</span><h3>Mode entraînement</h3></div>
        <p class="mc-lead">Pour apprendre en avançant, question par question.</p>
        <ul><li>Chaque question se valide isolément ; la démarche corrigée s'affiche aussitôt.</li>
          <li>La note pondérée s'actualise en continu dans le bandeau.</li>
          <li>Une fiche de méthode est consultable à tout moment, sans contrainte de temps.</li></ul>
        <button type="button" class="btn btn-mode" data-mode="training">Commencer l'entraînement</button>
      </article>
      <article class="mode-card exam">
        <div class="mc-head"><span class="mc-tag">Mode 2</span><h3>Mode examen</h3></div>
        <p class="mc-lead">Pour se placer en conditions de contrôle.</p>
        <ul><li>Aucune correction, aucune note et <b>aucun accès à la méthode</b> pendant la composition ; les réponses restent modifiables.</li>
          <li>Le chronomètre tourne, à comparer à la durée conseillée.</li>
          <li>En fin de sujet, le bouton « J'ai fini, je fais corriger ma copie » dévoile d'un coup les corrections, les notes par partie et la note globale.</li></ul>
        <button type="button" class="btn btn-mode" data-mode="exam">Composer en mode examen</button>
      </article>
    </div>
    <p class="home-note small">Le mode se choisit une seule fois : pour en changer, recharge la page. Rien n'est enregistré sur l'ordinateur.</p>
  </div>
</section>

"""
    g = g[:a0] + accueil + g[a1:]
    m0, m1 = g.index('<main class="page">'), g.index("</main>") + len("</main>")
    cart = cartouche or f"{nq_total} questions notées, réparties en {len(parties)} parties pondérées par leur durée conseillée."
    main = f"""<main class="page">
  <section class="print-only print-summary">
    <p>Élève : <span class="print-nom"></span> | Copie imprimée le <span class="print-date"></span></p>
    <p>Mode : <span class="print-mode"></span> | Temps de rédaction : <strong class="print-time"></strong> (durée conseillée : {dur_totale})</p>
    <p class="print-note-line">Note finale pondérée : <strong class="final-note"></strong></p>
    <p class="print-nograde">Copie non corrigée : les corrections et la note n'apparaissent qu'après la remise de la copie en mode examen.</p>
  </section>

  <header class="cartouche">
    <div class="title">
      <h1>{titre}</h1>
      <p>{cart}</p></div>
    <div class="nom"><label for="nom-eleve">Nom et prénom</label><input id="nom-eleve" type="text" autocomplete="name"></div>
  </header>

  <div class="consignes">
    <p class="only-training"><strong>Mode entraînement.</strong> Réponds dans chaque champ puis clique sur « Valider » : une réponse validée est définitive et sa correction s'affiche aussitôt. La fiche « Méthode » (onglet sur le bord droit) rappelle les outils utiles.</p>
    <p class="only-exam"><strong>Mode examen.</strong> Compose tout le sujet sans correction, sans note et sans accès à la méthode : tes réponses restent modifiables jusqu'au bout. Le bouton « J'ai fini, je fais corriger ma copie », en fin de sujet, dévoile d'un coup les corrections, les notes par partie et la note globale.</p>
    {"".join(consignes)}
    <p><strong>Barème pondéré par la durée conseillée</strong> : chaque partie est notée sur 20, puis pèse au prorata de son temps. Le récapitulatif de fin de sujet donne le détail partie par partie.</p>
  </div>
{"".join(sections)}
  <section class="recap" id="recap" aria-labelledby="t-recap">
    <header class="recap-head"><h2 id="t-recap">Récapitulatif et note finale</h2>
      <p class="small">Les questions non validées comptent comme fausses. Chaque partie est ramenée sur 20, puis pondérée par sa durée conseillée.</p></header>
    <div id="exam-submit-wrap">
      <p class="es-lead">Ta copie n'est pas encore corrigée : aucune réponse n'est verrouillée, tu peux encore revenir sur les questions.</p>
      <button type="button" class="btn btn-exam" id="exam-submit">J'ai fini, je fais corriger ma copie</button>
      <p class="es-warn" id="exam-warn" role="alert"></p>
    </div>
    <div id="recap-graded">
      <div class="recap-wrap">
        <table class="t recap-table">
          <thead><tr><th>Partie</th><th>Durée</th><th>Poids</th><th>Points</th><th>Note /20</th><th>Contribution</th></tr></thead>
          <tbody id="recap-body"></tbody>
          <tfoot><tr><th colspan="4">Note globale pondérée</th><th class="final-note"></th><th></th></tr></tfoot>
        </table>
      </div>
      <p class="final-detail small"></p>
    </div>
    <div class="recap-foot" id="recap-foot"><button type="button" class="btn btn-print">Imprimer ma copie</button>
      <span class="small no-print">L'impression reprend tes réponses, les corrections et ce récapitulatif.</span></div>
  </section>
</main>"""
    g = g[:m0] + main + g[m1:]
    c0 = g.index("<script>window.__PARTS__")
    c1 = g.index("</script>", c0) + len("</script>")
    conf = ("<script>window.__PARTS__ = " + json.dumps(parts_cfg, ensure_ascii=False) + ";\n"
            "window.__QCFG__ = " + json.dumps(cfg, ensure_ascii=False) + ";\n"
            "window.__SKCFG__ = {};" + (("\n" + config_js) if config_js else "") + "</script>")
    g = g[:c0] + conf + g[c1:]
    sortie = pathlib.Path(sortie)
    sortie.parent.mkdir(exist_ok=True)
    sortie.write_text(g, encoding="utf-8")
    print(f"{sortie.relative_to(ROOT)} : {len(g.encode('utf-8')) / 1024:.0f} Kio, {nq_total} questions, {dur_totale}")
    return cfg
