# Builds the turntable cross-section SVG. 1 cm = S px, x measured from the axle, y from the base floor.
# Usage: python3 turntable-section.py <standalone.svg> <inline-for-page.svg>
S=26; OX=400; OY=560
X=lambda c: round(OX+c*S,1)
Y=lambda c: round(OY-c*S,1)
out=[]
def a(s): out.append(s)
def box(x0,x1,y0,y1,cls,extra=''):
    a(f'<rect class="{cls}" x="{X(x0)}" y="{Y(y1)}" width="{round((x1-x0)*S,1)}" height="{round((y1-y0)*S,1)}"{extra}/>')
def line(x0,y0,x1,y1,cls):
    a(f'<line class="{cls}" x1="{X(x0)}" y1="{Y(y0)}" x2="{X(x1)}" y2="{Y(y1)}"/>')
bubbles=[]
def bub(n,bx,by,tx,ty):
    bubbles.append((n,bx,by,tx,ty))

# base floor and blocks
box(-13,13,-0.5,0,'tt-card')
for x0 in (-6.5,8.0):
    box(x0,x0+1.5,0,0.3,'tt-foam'); box(x0,x0+1.5,0.3,3.7,'tt-wood')
# drive plate, split at the axle
box(-7,-0.45,3.7,4.3,'tt-wood'); box(0.45,9.5,3.7,4.3,'tt-wood')
# KFL08 bearings: flange plate, housing, balls, bolts
for fy0,fy1,hy0,hy1 in ((4.3,4.6,4.6,5.4),(3.4,3.7,2.6,3.4)):
    box(-2.4,2.4,fy0,fy1,'tt-zinc'); box(-1.1,1.1,hy0,hy1,'tt-zinc')
    for bx in (-0.75,0.75):
        a(f'<circle class="tt-ball" cx="{X(bx)}" cy="{Y((hy0+hy1)/2)}" r="{0.22*S}"/>')
    for bx in (-1.9,1.9):
        box(bx-0.12,bx+0.12,min(fy0,3.7)-0.0 if fy0>4 else fy0,fy1 if fy0>4 else 4.3,'tt-bolt')
# slip ring: flange, body, rotor collar, screws
box(-2.2,2.2,0,0.3,'tt-ring'); box(-1.1,1.1,0.3,1.7,'tt-ring'); box(-0.5,0.5,1.7,2.3,'tt-ring')
for bx in (-1.7,1.7): box(bx-0.1,bx+0.1,-0.4,0.3,'tt-bolt')
# stator wires out to the right
a(f'<path class="tt-wr" d="M{X(1.1)} {Y(1.0)} C{X(3)} {Y(1.0)},{X(4)} {Y(0.7)},{X(6.6)} {Y(0.7)}"/>')
a(f'<path class="tt-wk" d="M{X(1.1)} {Y(0.85)} C{X(3)} {Y(0.85)},{X(4)} {Y(0.55)},{X(6.6)} {Y(0.55)}"/>')
a(f'<path class="tt-wy" d="M{X(1.1)} {Y(1.15)} C{X(3)} {Y(1.15)},{X(4)} {Y(0.85)},{X(6.6)} {Y(0.85)}"/>')
# tube with wires inside
box(-0.4,0.4,2.4,8.5,'tt-tube'); box(-0.28,0.28,2.4,8.5,'tt-bore')
for dx,c in ((-0.13,'tt-wr'),(0,'tt-wk'),(0.13,'tt-wy')):
    line(dx,2.2,dx,9.6,c)
# silicone hose over tube end and rotor collar
box(-0.62,0.62,1.85,2.95,'tt-hose')
# 60T pulley: hub below, teeth band, flanges
box(-1.1,1.1,6.0,6.55,'tt-alu'); box(-1.9,1.9,6.6,7.2,'tt-alu'); box(-2.1,2.1,6.5,6.6,'tt-alu'); box(-2.1,2.1,7.2,7.3,'tt-alu')
box(-1.1,-0.9,6.15,6.4,'tt-bolt')
# stepper: standoffs, washers, body, cap, ears, shaft, 20T pulley
MS=5.86
for sx in (4.76,8.56):
    box(sx-0.3,sx+0.3,4.3,4.5,'tt-rub'); box(sx-0.15,sx+0.15,4.5,6.2,'tt-zinc')
box(5.26,8.06,4.6,6.3,'tt-motor',' rx="6"'); box(8.06,8.5,4.8,6.0,'tt-cap')
box(4.56,8.76,6.2,6.32,'tt-zinc')
box(MS-0.45,MS+0.45,6.3,6.45,'tt-zinc'); box(MS-0.25,MS+0.25,6.45,7.8,'tt-shaft')
box(MS-0.64,MS+0.64,6.6,7.2,'tt-alu'); box(MS-0.8,MS+0.8,6.5,6.6,'tt-alu'); box(MS-0.8,MS+0.8,7.2,7.3,'tt-alu'); box(MS-0.75,MS+0.75,7.3,7.8,'tt-alu')
a(f'<text class="tt-in" x="{X(6.66)}" y="{Y(5.3)}" text-anchor="middle">28BYJ-48</text>')
# belt: cut ends plus the front strand between the pulleys
box(-2.05,-1.9,6.62,7.18,'tt-belt'); box(MS+0.64,MS+0.79,6.62,7.18,'tt-belt')
box(1.9,MS-0.64,6.62,7.18,'tt-strand')
# flange coupling with screws into the disc
box(-0.7,0.7,7.5,8.1,'tt-alu'); box(-1.6,1.6,8.1,8.5,'tt-alu')
for bx in (-1.2,1.2): box(bx-0.1,bx+0.1,8.1,9.0,'tt-bolt')
# deck pieces with break marks, rink disc, snow line
box(-13,-11.25,8.5,9.0,'tt-deck'); box(11.25,13,8.5,9.0,'tt-deck')
box(-11,11,8.5,9.0,'tt-disc')
for bx in (-0.12,0.12): pass
# tree: trunk, cone, LEDs, break line
box(-0.9,0.9,9.0,11,'tt-trunk')
import math
top=16.5; r_at=lambda y: 8.2*(27-y)/16
a(f'<polygon class="tt-tree" points="{X(-8.2)},{Y(11)} {X(8.2)},{Y(11)} {X(r_at(top))},{Y(top)} {X(-r_at(top))},{Y(top)}"/>')
zz=' '.join(f'{X(-r_at(top)-0.4+i*((2*r_at(top)+0.8)/10))},{Y(top+(0.25 if i%2 else -0.25))}' for i in range(11))
a(f'<polyline class="tt-break" points="{zz}"/>')
for i,(lx,ly) in enumerate(((-5.5,12.2),(-2,13.6),(3.2,12.6),(6.2,11.6),(-4.4,15.4),(1.4,15.6),(-6.8,11.5))):
    a(f'<circle class="tt-led{i%3}" cx="{X(lx)}" cy="{Y(ly)}" r="{0.22*S}"/>')
# tree wires from the tube up the trunk
line(0.13,9.6,0.13,10.6,'tt-wy')

# callouts
bub(1,-10.5,13.2,-7.6,13.2)
bub(2,-9.4,10.3,-9.4,9.0)
bub(3,-12.2,10.3,-12.2,9.0)
bub(4,-6.5,8.05,-1.6,8.3)
bub(5,-6.5,5.75,-0.4,5.75)
bub(6,-6.5,6.9,-2.1,6.9)
bub(7,3.4,7.85,3.4,7.18)
bub(8,11.2,7.55,MS+0.8,7.55)
bub(9,11.2,5.6,8.5,5.6)
bub(10,11.2,4.4,8.86,4.4)
bub(11,-6.5,4.95,-1.1,4.95)
bub(12,-8.6,3.0,-7.0,3.9)
bub(13,-3.7,3.0,-1.1,3.0)
bub(14,-3.7,2.15,-0.62,2.4)
bub(15,2.6,2.6,0.5,2.0)
bub(16,-3.7,0.9,-1.1,0.9)
bub(17,11.2,2.2,9.5,2.2)
bub(18,-11.2,-1.25,-11.2,-0.5)
bub(19,7.6,1.6,6.6,0.85)
for n,bx,by,tx,ty in bubbles:
    a(f'<line class="tt-lead" x1="{X(bx)}" y1="{Y(by)}" x2="{X(tx)}" y2="{Y(ty)}"/>')
    a(f'<circle class="tt-dot" cx="{X(tx)}" cy="{Y(ty)}" r="2.2"/>')
for n,bx,by,tx,ty in bubbles:
    a(f'<circle class="tt-bub" cx="{X(bx)}" cy="{Y(by)}" r="10"/><text class="tt-n" x="{X(bx)}" y="{Y(by)+4}" text-anchor="middle">{n}</text>')

# key
keys=["Paper tree with LEDs (cut short here)","Rink disc, 22 cm, foil covered","Deck, lifts off over the disc","8 mm flange coupling, screwed to the disc","8 mm brass tube, tree wires inside","GT2 pulley, 60 teeth","GT2 belt, 200 mm, 3:1","GT2 pulley, 20 teeth","28BYJ-48 stepper motor","Rubber washers on standoffs","Upper KFL08 flange bearing","Drive plate, 6 mm plywood","Lower KFL08 flange bearing","Silicone hose, flexible joint","Slip ring rotor, turns with tree","Slip ring body and flange, fixed","Wooden block on foam","Base floor","6 wires to Nano, 5V and GND"]
KX=770; ky=70
a(f'<text class="tt-h" x="{KX}" y="{ky-28}">Parts</text>')
for i,k in enumerate(keys):
    y=ky+i*25
    a(f'<circle class="tt-bub" cx="{KX+10}" cy="{y-4}" r="10"/><text class="tt-n" x="{KX+10}" y="{y}" text-anchor="middle">{i+1}</text><text class="tt-k" x="{KX+28}" y="{y}">{k}</text>')
y=ky+len(keys)*25+12
for t in ("Heights from the floor: plate 4.3 cm,","belt 6.9 cm, deck 9.0 cm.","Axle to motor shaft: 58.6 mm.","Section through the axle, roughly to scale.","Heights change once the slip ring is measured."):
    a(f'<text class="tt-note" x="{KX}" y="{y}">{t}</text>'); y+=20

STYLE='''<style>
.tt-card{fill:#c49a66;stroke:#8c6a42}.tt-wood{fill:#b5844f;stroke:#7d5a33}.tt-foam{fill:#6b7894}
.tt-zinc{fill:#9aa3b2;stroke:#5d6576}.tt-ball{fill:#e4e8ef;stroke:#5d6576}.tt-bolt{fill:#3b4150}
.tt-ring{fill:#2a2d36;stroke:#8d97ab}.tt-in{font:600 11px "IBM Plex Mono",monospace;fill:#efeadf}
.tt-tube{fill:#d8b65a;stroke:#8a7030}.tt-bore{fill:#141a28}.tt-hose{fill:#7cc0a6;fill-opacity:.55;stroke:#7cc0a6}
.tt-alu{fill:#c9d0da;stroke:#6f7889}.tt-motor{fill:#b9c0cb;stroke:#6f7889}.tt-cap{fill:#3a68b5;stroke:#24467f}
.tt-shaft{fill:#e4e8ef;stroke:#6f7889}.tt-rub{fill:#1a1a20}.tt-belt{fill:#2b2f3a;stroke:#efeadf;stroke-width:1}
.tt-strand{fill:#2b2f3a;stroke:#efeadf;stroke-width:1;stroke-dasharray:5 3}
.tt-deck{fill:#efeadf;stroke:#a89c86}.tt-disc{fill:#c3d6ea;stroke:#7d93ad}.tt-trunk{fill:#8c6a42}
.tt-tree{fill:#2f6650;stroke:#244f3e}.tt-break{fill:none;stroke:#efeadf;stroke-width:2}
.tt-led0{fill:#ffbf69}.tt-led1{fill:#ef7663}.tt-led2{fill:#8fd0ff}
.tt-wr{stroke:#ef7663;stroke-width:1.6;fill:none}.tt-wk{stroke:#aab3c6;stroke-width:1.6;fill:none}.tt-wy{stroke:#ffbf69;stroke-width:1.6;fill:none}
.tt-lead{stroke:#efeadf;stroke-width:1;opacity:.8}.tt-dot{fill:#efeadf}
.tt-bub{fill:#ffbf69}.tt-n{font:700 11px "IBM Plex Mono",monospace;fill:#2b1e10}
.tt-h{font:700 20px "Grenze Gotisch",Georgia,serif;fill:#ffbf69}.tt-k{font:400 13px "Atkinson Hyperlegible",system-ui,sans-serif;fill:#efeadf}
.tt-note{font:400 12px "IBM Plex Mono",monospace;fill:#aab3c6}
</style>'''
VB='0 0 1110 650'
ARIA='Cross-section of the turntable. A paper tree stands on a 22 cm rink disc that sits flush in a hole in the deck. A flange coupling joins the disc to an 8 mm brass tube carrying the tree wires. The tube runs through two KFL08 flange bearings on a plywood drive plate. A 60-tooth pulley on the tube is driven by a GT2 belt from a 20-tooth pulley on the 28BYJ-48 stepper beside it, a 3 to 1 reduction. Below the plate, a silicone hose joins the tube to the slip ring rotor. The slip ring body is screwed to the base floor and its six wires run to the Nano and power rail.'
body='\n'.join(out)
inline=f'<svg class="tt" viewBox="{VB}" role="img" aria-label="{ARIA}">\n{STYLE}\n{body}\n</svg>'
standalone=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{VB}" width="1110" height="650" role="img" aria-label="{ARIA}">\n<title>Lantern Square turntable, cross-section</title>\n{STYLE}\n<rect width="1110" height="650" fill="#0f1626"/>\n{body}\n</svg>\n'
import sys
open(sys.argv[1],'w').write(standalone)
open(sys.argv[2],'w').write(inline)
