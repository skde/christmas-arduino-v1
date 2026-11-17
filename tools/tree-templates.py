# Builds printable 1:1 cutting templates for the turning Christmas tree on the rink disc.
# Sizes match the tree in concept/concept-page.html (cR, cY, 7.2 tall cones). Units are cm; pages are A4 portrait.
# Reuses the page layout and drawing code of house-templates.py.
# Usage: python3 tools/tree-templates.py [out-dir]   (default: drawings/templates)
#   writes <out-dir>/tree-templates-N.svg (one per page) and tree-templates.html (all pages, for printing)
import importlib.util, math, os, sys

_spec = importlib.util.spec_from_file_location('ht', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'house-templates.py'))
ht = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(ht)
piece, rect, circle, tab, f = ht.piece, ht.rect, ht.circle, ht.tab, ht.f

CARD = 'thin card'
# Cone tiers, bottom to top: base radius, base height above the rink disc top. All cones are 7.2 tall.
# Model: cR=[8.2,7,5.7,4.3,2.9], cY (cone centres, deck coords) minus 3.6 minus disc top 0.6.
TIERS = [(8.2, 2.2), (7.0, 6.1), (5.7, 9.9), (4.3, 13.8), (2.9, 17.5)]
CH = 7.2          # cone height
TUBE_R = 0.95     # outer radius of the core tube (2 turns of thin card on a 1.8 cm former)
TUBE_L = 22.0     # core tube length, from the disc top
PIX_Z = 1.5       # pixel height above each cone's bottom rim
PIX_HOLE = 0.3    # pixel window radius (6 mm)
NOTCH = 0.6       # wire notch at the top hole of each cone, width and depth
# 12 pixels, 4-3-2-2-1 per tier, spread by the golden angle and kept clear of the seams.
PER_TIER = [4, 3, 2, 2, 1]
PIX = []
k = 0
for t, n in enumerate(PER_TIER):
    angs = sorted(((k + j) * 137.5 + 15) % 360 for j in range(n))
    PIX.append(angs); k += n

def slant(r): return math.hypot(r, CH)

def cone_pieces(i):
    """Sector net(s) for tier i. Tiers 1 and 2 are too big for A4, so they come in two halves."""
    r, base = TIERS[i]
    s = slant(r)
    theta = 2*math.pi*r/s                        # sector angle of the whole net
    top = i == len(TIERS) - 1                    # top cone stays pointed
    a = 0 if top else s*TUBE_R/r                 # inner hole radius on the net
    parts = 2 if 2*s > 17 and theta > math.pi else 1
    first = sum(PER_TIER[:i]) + 1
    out = []
    for h in range(parts):
        span = theta/parts
        a0, a1 = -span/2, span/2                 # bisector along +x
        phi0 = 360*h/parts                       # cone angle covered by this piece starts here
        P = lambda rad, ang: (rad*math.cos(ang), rad*math.sin(ang))
        n = 48
        outer = [P(s, a0 + (a1 - a0)*j/n) for j in range(n + 1)]
        pts = list(outer)
        e0, e1 = outer[-1], (P(a, a1) if a else (0, 0))
        t_ = tab(e0, e1, 1.0, 0.25, (s/2, 0))
        pts += [t_[0], t_[1]]
        if a:
            inner = [P(a, a1 - (a1 - a0)*j/n) for j in range(n + 1)]
            if h == 0:                           # wire notch in the middle of the inner arc
                w = NOTCH/2/a
                inner = [q for q in inner if abs(math.atan2(q[1], q[0])) > w]
                m = next(j for j, q in enumerate(inner) if math.atan2(q[1], q[0]) < 0)
                inner[m:m] = [P(a, w), P(a + NOTCH, w*a/(a + NOTCH)), P(a + NOTCH, -w*a/(a + NOTCH)), P(a, -w)]
            pts += inner
        else:
            pts.append((0, 0))
        holes, labels = [], []
        for j, phi in enumerate(PIX[i]):
            if not (phi0 <= phi < phi0 + 360/parts): continue
            ang = a0 + (phi - phi0)/360*theta    # position on the net
            rad = s*(1 - PIX_Z/CH)
            c = P(rad, ang)
            holes.append(circle(c[0], c[1], PIX_HOLE, 16))
            l = P(rad - 0.9, ang); labels.append((l[0], l[1], str(first + j)))
        name = f'Tree tier {i + 1}' + (f', half {"AB"[h]}' if parts > 1 else '')
        notes = [f'Cone {2*r:g} across, {CH:g} tall. Arc radius {f(s)}, sector {math.degrees(theta):.0f}° in total.']
        if parts > 1:
            notes.append(f'Two halves: glue each tab under the other half\'s straight edge.')
        else:
            notes.append('Roll into a cone and glue the tab under the other straight edge.')
        if top:
            notes.append('Pointed: it slides over the top of the core tube. Star on a toothpick in the tip.')
        else:
            notes.append(f'Top hole fits the core tube ({2*TUBE_R:g} across).' + (' Notch lets the pixel wires up to the next tier.' if h == 0 else ''))
        if holes:
            notes.append(f'Pixel windows Ø{2*PIX_HOLE*10:g} mm at {PIX_Z:g} cm above the rim. Numbers give the chain order.')
        g = ((t_[0][0] + t_[1][0])/2*0.5 + (e0[0] + e1[0])/2*0.5, (t_[0][1] + t_[1][1])/2*0.5 + (e0[1] + e1[1])/2*0.5)
        labels.append((g[0], g[1], 'glue'))
        out.append(piece(name, pts, 'cut 1', mat=CARD, holes=holes, labels=labels, folds=[(e0, e1)], notes=notes))
    return out

def tube():
    c = 2*math.pi*TUBE_R
    W = 2*c + 1.0                                # two turns plus 1 cm glue overlap
    ox = W - c                                   # the last turn (outer face) starts here
    marks, labels = [], []
    trunk = TIERS[0][1]
    marks.append(rect(ox, 0, W, trunk))
    labels.append((ox + c/2, trunk/2, 'paint brown'))
    for i, (r, base) in enumerate(TIERS[:-1]):
        y = base + CH*(1 - TUBE_R/r)             # where this cone's top hole sits
        marks.append([(ox, y), (W, y)]); labels.append((ox + c/2, y + 0.3, f'tier {i + 1} top'))
    slot = lambda x: rect(x - 0.3, trunk + 0.4, x + 0.3, trunk + 1.6)
    holes = [slot(ox - c/2), slot(ox + c/2)]     # same spot on both turns
    return piece('Core tube', rect(0, 0, W, TUBE_L), mat=CARD, holes=holes, marks=marks, labels=labels,
                 dims=[('h', 0, W, -0.7, f(W)), ('v', 0, TUBE_L, -0.7, f(TUBE_L))],
                 notes=['Roll two turns around a 1.8 cm former (a thick marker), starting from the left edge,',
                        'so the marked strip ends up outside. Glue all over. The two slots line up.',
                        'Pixel wires come up inside the tube from the disc and leave through the slot.'])

def foot():
    return piece('Tree foot ring', circle(0, 0, 2.5, 48), 'cut 2', mat=ht.CORR, holes=[circle(0, 0, TUBE_R, 24)],
                 dims=[('h', -2.5, 2.5, -3.2, '5.0')],
                 notes=['Glue both on the disc centre, over the wire hole. The tube stands in them. Cover with cotton snow.'])

def star():
    pts = []
    for i in range(10):
        a = i*math.pi/5 + math.pi/2; r = 0.72 if i % 2 else 1.65
        pts.append((r*math.cos(a), r*math.sin(a)))
    return piece('Star', pts, 'cut 2', mat=CARD, marks=[[(0, -0.72), (0, -1.6)]],
                 notes=['Cover with gold foil. Glue the two stars back to back on a toothpick (the mark).',
                        'Push the toothpick 1.5 cm into the tip of tier 5.'])

def main(out):
    os.makedirs(out, exist_ok=True)
    P = [p for i in range(len(TIERS)) for p in cone_pieces(i)] + [tube(), foot(), star()]
    pages = ht.layout([('Christmas tree', P)])
    legend = 'Print at 100 % on paper, then trace onto thin card. Sizes in cm. The glue tab lies beyond the dashed line.'
    svgs = [ht.page_svg(t, b, i + 1, len(pages), head='tree templates', legend=legend) for i, (t, b) in enumerate(pages)]
    for i, s in enumerate(svgs):
        open(os.path.join(out, f'tree-templates-{i+1}.svg'), 'w').write(s)
    html = ('<!doctype html><meta charset="utf-8"><title>Tree templates</title>'
            '<style>@page{size:A4;margin:0}body{margin:0}svg{display:block;page-break-after:always}</style>\n'
            + '\n'.join(svgs))
    open(os.path.join(out, 'tree-templates.html'), 'w').write(html)
    print(f'{len(svgs)} pages written to {out}')
    for i, (r, base) in enumerate(TIERS):
        print(f'tier {i+1}: r {r}, slant {slant(r):.2f}, sector {math.degrees(2*math.pi*r/slant(r)):.0f}°, pixels {PIX[i]}')

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'drawings', 'templates'))
