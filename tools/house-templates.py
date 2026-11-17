# Builds printable 1:1 cutting templates for the chapel, bakery and cottage.
# Sizes match the house() calls in concept/concept-page.html. Units are cm; pages are A4 portrait.
# Usage: python3 tools/house-templates.py [out-dir]   (default: drawings/templates)
#   writes <out-dir>/house-templates-N.svg (one per page) and house-templates.html (all pages, for printing)
import math, os, sys, textwrap

# Materials (user, 2026-11-17). Board only where a clean window cut matters; cheaper corrugated everywhere else.
TB = 0.15    # bookbinding board thickness, cm
TC = 0.3     # single-wall corrugated thickness, cm
BOARD, CORR = 'board 1.5 mm', 'corrugated 3 mm'
BAR = 0.2    # width of the window bars left standing, cm
OVER_EAVE, OVER_GABLE = 0.5, 0.8   # roof overhang past the walls, cm

# ---------- shape helpers (piece coordinates: cm, y up, origin bottom-left) ----------
def rect(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]

def circle(cx, cy, r, n=24):
    return [(cx + r*math.cos(2*math.pi*i/n), cy + r*math.sin(2*math.pi*i/n)) for i in range(n)]

def window(xc, sill, w, h, arch=False, bars=True):
    """Openings to cut. Bars (vertical and horizontal, through the centre) are left standing."""
    r = w/2
    def top(x):
        if not arch: return sill + h
        cy = sill + h - r
        return cy + math.sqrt(max(r*r - (x-xc)**2, 0))
    def pane(xa, xb, ya, yb_is_top, yb=None):
        if not yb_is_top:
            return rect(xa, ya, xb, yb)
        pts = [(xa, ya), (xb, ya)]
        n = 12
        for i in range(n+1):
            x = xb - (xb-xa)*i/n
            pts.append((x, top(x)))
        return pts
    x0, x1 = xc - w/2, xc + w/2
    if not bars:
        return [pane(x0, x1, sill, True)]
    ym = sill + h/2 if not arch else sill + (h - r)/2 + 0.2
    b = BAR/2
    return [pane(x0, xc-b, sill, False, ym-b), pane(xc+b, x1, sill, False, ym-b),
            pane(x0, xc-b, ym+b, True), pane(xc+b, x1, ym+b, True)]

def gable(w, eave, apex):
    return [(0, 0), (w, 0), (w, eave), (w/2, apex), (0, eave)]

def tab(p, q, depth, inset, centre):
    """Two outer corners of a trapezoid glue tab on edge p->q, on the side away from centre."""
    dx, dy = q[0]-p[0], q[1]-p[1]; L = math.hypot(dx, dy); ux, uy = dx/L, dy/L
    nx, ny = -uy, ux
    mx, my = (p[0]+q[0])/2, (p[1]+q[1])/2
    if (mx+nx-centre[0])**2 + (my+ny-centre[1])**2 < (mx-centre[0])**2 + (my-centre[1])**2:
        nx, ny = -nx, -ny
    return [(p[0]+ux*inset+nx*depth, p[1]+uy*inset+ny*depth), (q[0]-ux*inset+nx*depth, q[1]-uy*inset+ny*depth)]

def piece(name, outline, count='cut 1', mat=CORR, holes=(), marks=(), folds=(), dims=(), notes=(), centre=None, labels=()):
    return dict(name=name, outline=outline, count=count, mat=mat, holes=list(holes), marks=list(marks),
                folds=list(folds), dims=list(dims), notes=list(notes), centre=centre, labels=list(labels))

def f(v):
    t = f'{round(v + 1e-9, 2):.2f}'
    return t[:-1] if t.endswith('0') else t

def wall_dims(w, h, apex=None):
    d = [('h', 0, w, -0.7, f(w)), ('v', 0, h, -0.7, f(h))]
    if apex: d.append(('v', 0, apex, w + 0.7, f(apex)))
    return d

def roof_pair(prefix, w, d, h, rh, front=OVER_GABLE):
    slope = math.hypot(w/2, rh)
    L = d + OVER_GABLE + front
    a = slope + OVER_EAVE
    note = [f'Long edge runs along the ridge. Pitch {math.degrees(math.atan2(rh, w/2)):.0f}°.',
            'Flutes run down the slope. The wider panel overlaps the other at the ridge.']
    return [piece(f'{prefix} roof panel A', rect(0, 0, L, a), dims=[('h', 0, L, -0.7, f(L)), ('v', 0, a, -0.7, f(a))], notes=note),
            piece(f'{prefix} roof panel B', rect(0, 0, L, a + TC), dims=[('h', 0, L, -0.7, f(L)), ('v', 0, a + TC, -0.7, f(a + TC))],
                  notes=[f'{TC*10:g} mm wider than panel A. Flutes run down the slope.'] + note[2:])]

def chimney(name, c, xc, w, h, rh, top):
    """Thin-card net for a square chimney of side c, centred xc from the ridge, sitting on the roof slope."""
    a = math.atan2(rh, w/2)
    surf = lambda x: h + rh*(1 - abs(x)/(w/2)) + TC/math.cos(a)
    hu, hd = top - surf(xc - c/2), top - surf(xc + c/2)   # uphill (short) and downhill (tall) faces
    lo = hd - hu
    out = [(0, lo), (c, lo), (2*c, 0), (3*c, 0), (4*c, lo)]
    t1 = tab((4*c, lo), (4*c, hd), 0.5, 0.15, (2*c, hd/2))
    out += [t1[0], t1[1], (4*c, hd), (0, hd)]
    folds = [((x, hd), (x, lo if x in (c, 4*c) else 0)) for x in (c, 2*c, 3*c, 4*c)]
    return piece(name, out, mat='thin card', folds=folds,
                 dims=[('h', 0, c, hd + 0.6, f(c)), ('v', lo, hd, -0.7, f(hu)), ('v', 0, hd, 4*c + 1.2, f(hd))],
                 notes=['Fold into a square tube, glue the tab inside.',
                        'Short face goes uphill, toward the ridge. Cap with cotton snow.'])

# ---------- chapel: w 10, d 12, walls 9, roof rise 6; tower 5.4 x 4.6 x 18.7 + spire 6.2 ----------
def chapel():
    w, d, h, rh = 10, 12, 9, 6
    P = []
    P.append(piece('Chapel gable wall', gable(w, h, h + rh), 'cut 2 (front, back)', dims=wall_dims(w, h, h + rh),
                   notes=['No openings: the tower stands against the front one.']))
    sw = d - 2*TC
    wins = window(sw/2 - 2.5, 3.2, 1.8, 4, arch=True) + window(sw/2 + 2.5, 3.2, 1.8, 4, arch=True)
    P.append(piece('Chapel side wall, right', rect(0, 0, sw, h), mat=BOARD, holes=wins, dims=wall_dims(sw, h),
                   notes=['Faces the village. Windows 1.8 × 4.0 arched, sill 3.2, centres 2.5 either side of middle.',
                          'Drawn as seen from outside: the tower (front) end is on the left.',
                          'Green tissue behind the left window, red behind the right.']))
    P.append(piece('Chapel side wall, left', rect(0, 0, sw, h), dims=wall_dims(sw, h), notes=['No windows.']))
    dv = w - TB - TC
    eL, eR = h + rh*TC/(w/2), h + rh*TB/(w/2)   # roof underside at the inside face of each wall
    P.append(piece('Chapel nave divider', [(0, 0), (dv, 0), (dv, eR), (w/2 - TC, h + rh), (0, eL)],
                   dims=[('h', 0, dv, -0.7, f(dv)), ('v', 0, eL, -0.7, f(eL)), ('v', 0, eR, dv + 0.7, f(eR))],
                   holes=[circle(dv/2, 0.9, 0.5)],
                   notes=['Stands across the middle of the nave so red and green stay apart.',
                          'Not symmetric: the left (taller) edge goes against the corrugated left wall.',
                          'Hole for LED wires: seal it with tape after wiring.']))
    P += roof_pair('Chapel', w, d, h, rh, front=0)
    for q in P[-2:]: q['notes'].append('No overhang at the front: ends flush with the front gable, where the tower stands.')
    tw, td, th = 5.4, 4.6, 18.7
    bel = lambda ww: window(tw/2, 15.0, ww, 3.0, arch=True, bars=False)
    door = [rect(tw/2 - 1.1, 0, tw/2 + 1.1, 3.6)]
    P.append(piece('Tower front', rect(0, 0, tw, th), mat=BOARD, holes=window(tw/2, 6.1, 2.2, 4.6, arch=True) + bel(tw - 1.4),
                   marks=door, dims=wall_dims(tw, th),
                   notes=['Window 2.2 × 4.6 arched, sill 6.1, blue tissue.',
                          'Belfry arch 4.0 wide, 15.0 to 18.0. Door: paint, or glue dark card.']))
    P.append(piece('Tower back', rect(0, 0, tw, th), dims=wall_dims(tw, th),
                   notes=['No belfry arch at the back: it hides the bell servo.']))
    sd = td - TB - TC
    P.append(piece('Tower side', rect(0, 0, sd, th), 'cut 2', mat=BOARD, holes=window(sd/2, 15.0, 3.2, 3.0, arch=True, bars=False),
                   dims=wall_dims(sd, th), notes=['Fits between front and back. Arch 3.2 wide.']))
    P.append(piece('Tower shelf', rect(0, 0, tw - 2*TB, sd), holes=[circle(tw/2 - TB, sd/2, 0.5)],
                   dims=[('h', 0, tw - 2*TB, -0.7, f(tw - 2*TB)), ('v', 0, sd, -0.7, f(sd))],
                   notes=['Glue inside with its top face at 14.6, under the belfry. Bell servo sits on it.']))
    P.append(piece('Tower top plate', rect(0, 0, 6.2, 5.4),
                   dims=[('h', 0, 6.2, -0.7, '6.2'), ('v', 0, 5.4, -0.7, '5.4')],
                   notes=['On top of the tower, 0.4 overhang all round.']))
    # spire: rectangular pyramid, base 6.2 x 5.4, height 6.2
    bx, by, sh = 6.2, 5.4, 6.2
    L = math.sqrt((bx/2)**2 + (by/2)**2 + sh**2)
    bases = [bx, by, bx, by]
    ang = [2*math.asin(b/2/L) for b in bases]
    phi = -math.pi/2 - sum(ang)/2
    pts = [(L*math.cos(phi), L*math.sin(phi))]
    for t_ in ang:
        phi += t_; pts.append((L*math.cos(phi), L*math.sin(phi)))
    apex = (0, 0); cen = (0, -L/2)
    out = [apex, pts[0]]
    for i in range(4):
        out += tab(pts[i], pts[i+1], 0.5, 0.4, apex)
        out.append(pts[i+1])
    out += tab(pts[4], apex, 0.6, 0.5, cen)
    shift = lambda q: (q[0] + L + 0.2, q[1] + L)
    out = [shift(q) for q in out]
    folds = [(shift(apex), shift(p)) for p in pts[1:]] + [(shift(pts[i]), shift(pts[i+1])) for i in range(4)]
    P.append(piece('Chapel spire', out, mat='thin card', folds=folds,
                   notes=['Base 6.2 × 5.4, 6.2 tall. Sloping edges 7.4. Base edges alternate 6.2 and 5.4.',
                          'Fold the base tabs in, glue onto the top plate.']))
    return P

# ---------- bakery: front gable 13 wide, d 9, walls 10, roof rise 5.6 ----------
def bakery():
    w, d, h, rh = 13, 9, 10, 5.6
    P = []
    wins = window(w/2, 1.45, 7.4, 3.1) + window(w/2 - 3.5, 6.5, 2, 2.2) + window(w/2 + 3.5, 6.5, 2, 2.2)
    P.append(piece('Bakery front gable', gable(w, h, h + rh), mat=BOARD, holes=wins, dims=wall_dims(w, h, h + rh),
                   marks=[rect(w/2 - 4.05, 5.45, w/2 + 4.05, 5.55)],
                   notes=['Shop window 7.4 × 3.1, sill 1.45. Upstairs 2.0 × 2.2, sill 6.5, centres 3.5 either side.',
                          'Awning glues on the marked line at 5.5. Tracing paper behind all windows.']))
    P.append(piece('Bakery back gable', gable(w, h, h + rh), dims=wall_dims(w, h, h + rh)))
    sw = d - TB - TC
    P.append(piece('Bakery side wall', rect(0, 0, sw, h), 'cut 2', dims=wall_dims(sw, h)))
    fw, fd = w - 2*TC, d - TB - TC
    P.append(piece('Bakery upstairs floor', rect(0, 0, fw, fd), holes=[circle(fw/2, fd - 1.5, 0.5)],
                   dims=[('h', 0, fw, -0.7, f(fw)), ('v', 0, fd, -0.7, f(fd))],
                   notes=['Top face at 5.6. Separates shop and upstairs light.',
                          'Hole goes at the back, for the upstairs LED wires.',
                          'Glue the front edge to the front gable too (the awning hides the joint).']))
    P.append(piece('Floor support', rect(0, 0, 1.0, 5.6 - TC), 'cut 2',
                   dims=[('h', 0, 1.0, -0.7, '1.0'), ('v', 0, 5.6 - TC, -0.7, f(5.6 - TC))],
                   notes=['Glue in the back corners.']))
    P += roof_pair('Bakery', w, d, h, rh)
    # awning: 7 stripes of 1.16, face 1.8, glue strip 0.6 on top, scalloped lower edge
    aw, ad, gl, n = 8.1, 1.8, 0.6, 7
    out = []
    for i in range(n):
        for k in range(9):
            x = aw - (i + k/8)*aw/n
            out.append((x, 0.35*math.sin(math.pi*k/8)*-1 + 0.35))
    out = [(aw, 0.35)] + out[1:] + [(0, 0.35), (0, 0.35 + ad + gl), (aw, 0.35 + ad + gl)]
    out = list(reversed(out))
    P.append(piece('Bakery awning', out, mat='thin card', folds=[((0, 0.35 + ad), (aw, 0.35 + ad))],
                   marks=[[(i*aw/n, 0.35), (i*aw/n, 0.35 + ad)] for i in range(1, n)],
                   dims=[('h', 0, aw, -0.7, '8.1')],
                   notes=['Paint alternate stripes green and cream. Fold the top strip back and glue it on the line.']))
    P.append(chimney('Bakery chimney', 1.7, 3.8, w, h, rh, 16.2))
    return P

# ---------- cottage: front gable 12 wide, d 7.6, walls 7, roof rise 5 ----------
def cottage():
    w, d, h, rh = 12, 7.6, 7, 5
    P = []
    wins = window(w/2 - 3.2, 2.9, 2, 2.2) + window(w/2 + 3.2, 2.9, 2, 2.2) + window(w/2, 1.3, 1.8, 1.6, bars=False)
    P.append(piece('Cottage front gable', gable(w, h, h + rh), mat=BOARD, holes=wins, dims=wall_dims(w, h, h + rh),
                   marks=[rect(w/2 - 0.9, 3.05, w/2 + 0.9, 3.55)],
                   notes=['Windows 2.0 × 2.2, sill 2.9, centres 3.2 either side. Tracing paper.',
                          'Hearth 1.8 × 1.6, sill 1.3, amber paper. Mantel: dark card strip on the mark.']))
    P.append(piece('Cottage back gable', gable(w, h, h + rh), dims=wall_dims(w, h, h + rh)))
    sw = d - TB - TC
    P.append(piece('Cottage side wall', rect(0, 0, sw, h), 'cut 2', dims=wall_dims(sw, h)))
    P += roof_pair('Cottage', w, d, h, rh)
    # hearth box: tab | side 2.0 | back 2.6 | side 2.0 | tab, 3.4 tall, lid on the back panel
    s, b, hh, tb = 2.0, 2.6, 3.4, 0.5
    xs = [0, tb, tb + s, tb + s + b, tb + 2*s + b, 2*tb + 2*s + b]
    out = [(xs[0], 0.15), (xs[1], 0), (xs[4], 0), (xs[5], 0.15), (xs[5], hh - 0.15), (xs[4], hh),
           (xs[3], hh), (xs[3], hh + s), (xs[2], hh + s), (xs[2], hh), (xs[1], hh), (xs[0], hh - 0.15)]
    P.append(piece('Cottage hearth box', out, mat='thin card',
                   folds=[((x, 0), (x, hh)) for x in xs[1:5]] + [((xs[2], hh), (xs[3], hh))],
                   dims=[('h', xs[2], xs[3], -0.7, f(b)), ('h', xs[1], xs[2], -0.7, f(s)), ('v', 0, hh, -0.7, f(hh))],
                   notes=['Line with foil. Fold the end tabs outward and glue them inside the front gable, around the hearth.',
                          'Red and yellow flicker LEDs go inside, over their own deck hole. Window LEDs stay outside.']))
    P.append(chimney('Cottage chimney', 1.8, 3.6, w, h, rh, 12.7))
    return P

# ---------- page layout ----------
PW, PH, MX, TOP, BOT = 210, 297, 12, 34, 290
LH = 3.6  # note line height, mm

def frame(p):
    xs = [q[0] for q in p['outline']]; ys = [q[1] for q in p['outline']]
    bb = (min(xs), min(ys), max(xs), max(ys))
    has_r = any(dm[0] == 'v' and dm[3] > bb[2] for dm in p['dims'])
    has_t = any(dm[0] == 'h' and dm[3] > bb[3] for dm in p['dims'])
    ml, mr = 11, (13 if has_r else 4)
    mt = 9 + (6 if has_t else 0)
    w = max((bb[2]-bb[0])*10 + ml + mr, 62)
    p['lines'] = [l for n in p['notes'] for l in textwrap.wrap(n, int(w/1.4))]
    mb = 14 + LH*len(p['lines'])
    return bb, ml, mt, w, (bb[3]-bb[1])*10 + mt + mb

def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def render(p, ox, oy, bb, ml, mt):
    X = lambda x: round(ox + ml + (x - bb[0])*10, 2)
    Y = lambda y: round(oy + mt + (bb[3] - y)*10, 2)
    path = lambda pts, close=True: 'M' + ' L'.join(f'{X(a)} {Y(b)}' for a, b in pts) + (' Z' if close else '')
    o = []
    o.append(f'<text class="nm" x="{X(bb[0])}" y="{Y(bb[3]) - mt + 5}">{esc(p["name"])}'
             f'<tspan class="ct"> · {esc(p["count"])} · {esc(p["mat"])}</tspan></text>')
    o.append(f'<path class="cut" d="{path(p["outline"])}"/>')
    for h in p['holes']:
        o.append(f'<path class="hole" d="{path(h)}"/>')
    for m in p['marks']:
        o.append(f'<path class="mark" d="{path(m, len(m) > 2)}"/>')
    for a_, b_ in p['folds']:
        o.append(f'<path class="fold" d="{path([a_, b_], False)}"/>')
    for dm in p['dims']:
        if dm[0] == 'h':
            _, x0, x1, y, lab = dm
            yy = Y(y)
            o.append(f'<path class="dim" d="M{X(x0)} {yy} H{X(x1)} M{X(x0)} {yy-1.5} v3 M{X(x1)} {yy-1.5} v3"/>')
            o.append(f'<text class="dt" x="{(X(x0)+X(x1))/2}" y="{yy + (3.6 if y < bb[1] + 0.01 else -1.2)}" text-anchor="middle">{lab}</text>')
        else:
            _, y0, y1, x, lab = dm
            xx = X(x)
            o.append(f'<path class="dim" d="M{xx} {Y(y0)} V{Y(y1)} M{xx-1.5} {Y(y0)} h3 M{xx-1.5} {Y(y1)} h3"/>')
            cy = (Y(y0) + Y(y1))/2
            o.append(f'<text class="dt" x="{xx - 1.4}" y="{cy}" text-anchor="middle" transform="rotate(-90 {xx-1.4} {cy})">{lab}</text>')
    for x, y, lab in p.get('labels', []):
        o.append(f'<text class="dt" x="{X(x)}" y="{Y(y) + 1}" text-anchor="middle">{esc(lab)}</text>')
    ny = Y(bb[1]) + 13
    for n in p['lines']:
        o.append(f'<text class="nt" x="{X(bb[0]) - ml + 1}" y="{ny}">{esc(n)}</text>'); ny += LH
    return o

STYLE = '''<style>
.cut{fill:#fff;stroke:#000;stroke-width:.35}
.hole{fill:#cfd8e6;stroke:#000;stroke-width:.3}
.fold{fill:none;stroke:#1a5fb4;stroke-width:.3;stroke-dasharray:2 1.2}
.mark{fill:none;stroke:#888;stroke-width:.3;stroke-dasharray:.6 .8}
.dim{fill:none;stroke:#c01c28;stroke-width:.22}
text{font-family:Arial,Helvetica,sans-serif;fill:#222}
.dt{font-size:2.9px;fill:#c01c28}
.nm{font-size:3.4px;font-weight:bold}
.ct{font-weight:normal;fill:#555}
.nt{font-size:2.7px;fill:#444}
.h1{font-size:5px;font-weight:bold}
.lg{font-size:2.8px;fill:#444}
</style>'''

LEGEND = f'Print at 100 % (actual size). All sizes in cm. Board {TB*10:g} mm, corrugated {TC*10:g} mm (cut walls with the flutes upright).'

def page_svg(title, body, n, total, head='house templates', legend=LEGEND):
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{PW}mm" height="{PH}mm" viewBox="0 0 {PW} {PH}">', STYLE,
         f'<rect width="{PW}" height="{PH}" fill="#fff"/>',
         f'<text class="h1" x="{MX}" y="16">Lantern Square {head}: {esc(title)}</text>',
         f'<text class="lg" x="{PW-MX}" y="16" text-anchor="end">page {n} of {total}</text>',
         f'<text class="lg" x="{MX}" y="22.5">{esc(legend)}</text>',
         f'<path class="cut" d="M{MX} 26 h12"/><text class="lg" x="{MX+14}" y="27">cut</text>',
         f'<path class="hole" d="M{MX+24} 24.6 h6 v3 h-6 Z"/><text class="lg" x="{MX+32}" y="27">cut out (window)</text>',
         f'<path class="fold" d="M{MX+58} 26 h12"/><text class="lg" x="{MX+72}" y="27">fold or score</text>',
         f'<path class="mark" d="M{MX+94} 26 h12"/><text class="lg" x="{MX+108}" y="27">mark only</text>',
         f'<path class="dim" d="M{PW-MX-50} 26 h50 M{PW-MX-50} 24.5 v3 M{PW-MX} 24.5 v3"/>',
         f'<text class="dt" x="{PW-MX-25}" y="24" text-anchor="middle">check: 5.0 cm</text>']
    return '\n'.join(o + body + ['</svg>'])

def layout(groups):
    """Shelf packing, first fit: each page keeps a list of rows (y, height, next free x)."""
    pages = []  # (title, [svg lines])
    for title, pieces in groups:
        mine = []  # [lines, rows, next free y]
        fr = [(p, frame(p)) for p in pieces]
        fr.sort(key=lambda q: -q[1][4])
        for p, (bb, ml, mt, w, h) in fr:
            spot = None
            for pg in mine:
                for r in pg[1]:
                    if h <= r[1] + 0.1 and r[2] + w <= PW - MX:
                        spot = (pg, r); break
                if spot: break
                if pg[2] + h <= BOT:
                    r = [pg[2], h, MX]; pg[1].append(r); pg[2] += h + 4; spot = (pg, r); break
            if not spot:
                pg = [[], [], TOP]; mine.append(pg)
                r = [TOP, h, MX]; pg[1].append(r); pg[2] += h + 4; spot = (pg, r)
            pg, r = spot
            pg[0].extend(render(p, r[2], r[0], bb, ml, mt)); r[2] += w + 6
        pages += [(title, pg[0]) for pg in mine]
    return pages

def main(out):
    os.makedirs(out, exist_ok=True)
    pages = layout([('Chapel', chapel()), ('Bakery', bakery()), ('Cottage', cottage())])
    svgs = [page_svg(t, b, i + 1, len(pages)) for i, (t, b) in enumerate(pages)]
    for i, s in enumerate(svgs):
        open(os.path.join(out, f'house-templates-{i+1}.svg'), 'w').write(s)
    html = ('<!doctype html><meta charset="utf-8"><title>House templates</title>'
            '<style>@page{size:A4;margin:0}body{margin:0}svg{display:block;page-break-after:always}</style>\n'
            + '\n'.join(svgs))
    open(os.path.join(out, 'house-templates.html'), 'w').write(html)
    print(f'{len(svgs)} pages written to {out}')

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'drawings', 'templates'))
