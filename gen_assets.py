from PIL import Image, ImageDraw
import os, math

OUT = "/sessions/keen-sweet-fermi/mnt/outputs/sweet_land_assets"
os.makedirs(OUT, exist_ok=True)

SCALE = 4
ASSETS = {}  # store native images for sheet

# ─── PALETTE (candy land warm pastel) ───────────────────────────────────────
T   = (0,0,0,0)
BK  = (35,20,10,255)
WH  = (252,248,240,255)
CR  = (245,228,195,255)

CA1 = (228,175,98,255);  CA2 = (198,140,68,255);  CA3 = (158,102,42,255)
CH1 = (145,88,42,255);   CH2 = (108,62,22,255);   CH3 = (75,40,12,255)

PK1 = (255,200,220,255); PK2 = (242,158,188,255); PK3 = (212,108,148,255)
PK4 = (168,68,108,255)

TL1 = (178,235,218,255); TL2 = (122,198,178,255); TL3 = (78,158,138,255)
PU1 = (218,192,238,255); PU2 = (170,140,205,255); PU3 = (125,92,165,255)
RD1 = (248,132,142,255); RD2 = (218,82,98,255);   RD3 = (165,48,65,255)
YL1 = (255,238,108,255); YL2 = (248,208,58,255);  YL3 = (198,152,22,255)
GR1 = (158,212,132,255); GR2 = (102,168,88,255);  GR3 = (65,122,55,255)
MM1 = (252,242,230,255); MM2 = (245,220,220,255); MM3 = (230,192,198,255)
LL1 = (228,85,100,255);  LL2 = (252,235,220,255)

# ─── CORE DRAW HELPERS ───────────────────────────────────────────────────────
def ni(w,h): return Image.new('RGBA',(w,h),T)

def sv(img, name):
    ASSETS[name] = img
    s = img.resize((img.width*SCALE, img.height*SCALE), Image.NEAREST)
    s.save(f"{OUT}/{name}.png")
    print(f"  ✓ {name}.png  ({img.width}×{img.height})")

def px(img,x,y,c):
    if 0<=x<img.width and 0<=y<img.height:
        img.putpixel((x,y),c)

def hl(img,x0,x1,y,c):
    for x in range(x0,x1+1): px(img,x,y,c)

def vl(img,x,y0,y1,c):
    for y in range(y0,y1+1): px(img,x,y,c)

def fr(img,x0,y0,x1,y1,c):       # filled rect
    for y in range(y0,y1+1):
        for x in range(x0,x1+1): px(img,x,y,c)

def fo(img,cx,cy,rx,ry,c):        # filled oval
    if rx<=0 or ry<=0: return
    for y in range(cy-ry, cy+ry+1):
        for x in range(cx-rx, cx+rx+1):
            if ((x-cx)/rx)**2+((y-cy)/ry)**2<=1.0:
                px(img,x,y,c)

def oo(img,cx,cy,rx,ry,fill,bord): # outlined oval
    fo(img,cx,cy,rx,ry,fill)
    for y in range(cy-ry-1, cy+ry+2):
        for x in range(cx-rx-1, cx+rx+2):
            din  = ((x-cx)/(rx+0.01))**2+((y-cy)/(ry+0.01))**2
            dout = ((x-cx)/(rx+1.4))**2+((y-cy)/(ry+1.4))**2
            if din>1.0 and dout<=1.0:
                px(img,x,y,bord)

# ─────────────────────────────────────────────────────────────────────────────
# 1. COOKIE — IDLE  32×32
# ─────────────────────────────────────────────────────────────────────────────
def cookie_idle():
    img = ni(32,32)
    # ── hat ──
    fr(img,11,2,21,8,WH)
    fr(img,9,8,23,10,WH)
    fr(img,11,8,21,8,PK2)        # pink band
    hl(img,11,21,1,BK); hl(img,9,23,10,BK)
    vl(img,10,2,10,BK); vl(img,22,2,10,BK)
    px(img,9,9,BK); px(img,23,9,BK)
    # hat top corners soften
    px(img,11,2,CR); px(img,21,2,CR)
    # ── face ──
    oo(img,16,15,7,6,CR,BK)
    # eyes
    fr(img,12,12,13,14,BK); fr(img,19,12,20,14,BK)
    px(img,12,12,WH); px(img,19,12,WH)          # highlights
    px(img,13,13,(200,80,80,255)); px(img,20,13,(200,80,80,255))  # pupil tint
    # cheeks
    fo(img,11,17,2,1,PK1); fo(img,21,17,2,1,PK1)
    # smile
    for sx,sy in [(14,19),(15,20),(16,20),(17,20),(18,19)]: px(img,sx,sy,BK)
    # ── body ──
    oo(img,16,25,8,6,CA1,BK)
    fo(img,14,26,4,3,CA2)
    # cookie chip dots
    for dx,dy in [(11,23),(16,22),(21,23),(12,27),(20,27),(16,28)]:
        px(img,dx,dy,CA3)
    # ── arms ──
    oo(img,8,24,3,2,CA1,BK); oo(img,24,24,3,2,CA1,BK)
    # ── legs ──
    fr(img,12,29,14,31,CA2); fr(img,18,29,20,31,CA2)
    fr(img,11,31,15,32,CA3); fr(img,17,31,21,32,CA3)
    return img
sv(cookie_idle(),"cookie_idle")

# ─────────────────────────────────────────────────────────────────────────────
# 2. COOKIE — RUN  (4 frames)
# ─────────────────────────────────────────────────────────────────────────────
def cookie_run(f):
    img = ni(32,32)
    # hat
    fr(img,11,1,21,7,WH); fr(img,9,7,23,9,WH); fr(img,11,7,21,7,PK2)
    hl(img,11,21,0,BK); hl(img,9,23,9,BK)
    vl(img,10,1,9,BK); vl(img,22,1,9,BK)
    # face
    oo(img,16,14,7,6,CR,BK)
    fr(img,12,11,13,13,BK); fr(img,19,11,20,13,BK)
    px(img,12,11,WH); px(img,19,11,WH)
    fo(img,11,16,2,1,PK1); fo(img,21,16,2,1,PK1)
    for sx,sy in [(14,18),(15,19),(16,19),(17,19),(18,18)]: px(img,sx,sy,BK)
    # body
    oo(img,16,24,8,6,CA1,BK); fo(img,14,25,4,3,CA2)
    for dx,dy in [(11,22),(16,21),(21,22),(12,26),(20,26)]: px(img,dx,dy,CA3)
    # arms & legs per frame
    leg_configs = [
        # (lx,ly,rx,ry, arm_l_cx,arm_l_cy, arm_r_cx,arm_r_cy)
        (11,29,20,29, 7,22, 25,26),
        (12,29,19,30, 8,24, 24,24),
        (13,28,18,28, 25,22, 7,26),
        (12,29,19,29, 9,22, 23,26),
    ]
    lx,ly,rx,ry,alx,aly,arx,ary = leg_configs[f]
    fr(img,lx,ly,lx+2,ly+3,CA2); fr(img,rx,ry,rx+2,ry+3,CA2)
    fr(img,lx-1,ly+3,lx+3,ly+4,CA3); fr(img,rx-1,ry+3,rx+3,ry+4,CA3)
    oo(img,alx,aly,3,2,CA1,BK); oo(img,arx,ary,3,2,CA1,BK)
    return img
for i in range(4): sv(cookie_run(i),f"cookie_run{i+1}")

# ─────────────────────────────────────────────────────────────────────────────
# 3. COOKIE — JUMP  32×32
# ─────────────────────────────────────────────────────────────────────────────
def cookie_jump():
    img = ni(32,32)
    fr(img,11,1,21,7,WH); fr(img,9,7,23,9,WH); fr(img,11,7,21,7,PK2)
    hl(img,11,21,0,BK); hl(img,9,23,9,BK)
    vl(img,10,1,9,BK); vl(img,22,1,9,BK)
    oo(img,16,14,7,6,CR,BK)
    # wide surprised eyes
    fr(img,11,11,13,13,BK); fr(img,19,11,21,13,BK)
    px(img,11,11,WH); px(img,19,11,WH)
    # O mouth
    oo(img,16,18,2,2,BK,BK); fo(img,16,18,1,1,RD1)
    fo(img,11,16,2,1,PK1); fo(img,21,16,2,1,PK1)
    # body stretched (squash & stretch)
    oo(img,16,25,7,7,CA1,BK); fo(img,14,26,3,4,CA2)
    for dx,dy in [(10,23),(16,21),(22,23),(12,28),(20,28)]: px(img,dx,dy,CA3)
    # legs tucked
    oo(img,12,30,4,2,CA2,BK); oo(img,20,30,4,2,CA2,BK)
    # arms raised
    oo(img,7,20,3,2,CA1,BK); oo(img,25,20,3,2,CA1,BK)
    return img
sv(cookie_jump(),"cookie_jump")

# ─────────────────────────────────────────────────────────────────────────────
# 4. ENEMY: DONUT ROLLER  24×24
# ─────────────────────────────────────────────────────────────────────────────
def enemy_donut():
    img = ni(24,24)
    # outer ring
    oo(img,12,12,10,10,CA2,BK)
    # pink frosting on top half
    fo(img,12,10,9,6,PK2)
    # frosting drips
    for dx,dy in [(8,14),(12,15),(16,14),(10,13),(14,13)]:
        fo(img,dx,dy,1,2,PK2)
    # punch hole
    fo(img,12,12,4,4,T)
    # hole shadow ring
    for y in range(7,17):
        for x in range(7,17):
            d_in  = ((x-12)/3.5)**2+((y-12)/3.5)**2
            d_out = ((x-12)/5.0)**2+((y-12)/5.0)**2
            if d_in<=1.0: px(img,x,y,T)
            elif d_out<=1.0 and d_in>1.0:
                pass  # already filled with CA2
    # inner shadow
    for y in range(8,16):
        for x in range(8,16):
            if ((x-12)/4)**2+((y-12)/4)**2<=1.0:
                if ((x-12)/3)**2+((y-12)/3)**2>1.0:
                    px(img,x,y,CH2)
    # sprinkles
    for sx,sy,sc in [(9,8,TL2),(13,7,YL2),(16,9,GR2),(7,11,RD1),(16,12,PU2),(11,6,PK3)]:
        px(img,sx,sy,sc); px(img,sx+1,sy,sc)
    # face (below hole)
    fr(img,9,14,10,15,BK); fr(img,14,14,15,15,BK)
    # angry brows
    hl(img,8,10,13,BK); hl(img,14,16,13,BK)
    # grumpy mouth
    for mx,my in [(10,17),(11,18),(12,18),(13,17)]: px(img,mx,my,BK)
    return img
sv(enemy_donut(),"enemy_donut")

# ─────────────────────────────────────────────────────────────────────────────
# 5. ENEMY: LOLLIPOP FAIRY  20×28
# ─────────────────────────────────────────────────────────────────────────────
def enemy_lollipop_fairy():
    img = ni(20,28)
    # wings
    oo(img,4,17,4,6,TL1,BK); oo(img,16,17,4,6,TL1,BK)
    fo(img,4,17,2,4,TL2); fo(img,16,17,2,4,TL2)
    # dress body
    oo(img,10,21,5,5,PU1,BK); fo(img,10,22,3,3,PU2)
    # head
    oo(img,10,10,6,6,CR,BK)
    # pink hair
    oo(img,10,5,5,4,PK2,BK); oo(img,5,8,3,3,PK2,BK); oo(img,15,8,3,3,PK2,BK)
    # eyes
    fr(img,7,9,8,10,BK); fr(img,12,9,13,10,BK)
    px(img,7,9,WH); px(img,12,9,WH)
    fo(img,5,12,2,1,PK1); fo(img,15,12,2,1,PK1)
    # smile
    for sx,sy in [(8,14),(9,15),(10,15),(11,15),(12,14)]: px(img,sx,sy,BK)
    # crown
    for cx,cy in [(6,5),(10,3),(14,5)]:
        fo(img,cx,cy,1,2,YL1); px(img,cx,cy-2,BK)
    hl(img,6,14,6,YL2)
    # lollipop wand (right side)
    fr(img,17,14,18,26,CH1)
    oo(img,17,10,4,4,LL2,BK)
    # swirl on lollipop
    draw = ImageDraw.Draw(img)
    draw.pieslice([13,6,21,14], start=0,   end=180, fill=LL1,  outline=None)
    draw.pieslice([13,6,21,14], start=180, end=360, fill=LL2,  outline=None)
    draw.pieslice([14,7,20,13], start=90,  end=270, fill=LL1,  outline=None)
    oo(img,17,10,4,4,T,BK)  # re-outline only
    oo(img,17,10,4,4,T,BK)
    # re-draw outline properly
    for y in range(6,14):
        for x in range(13,21):
            d = ((x-17)/4.5)**2+((y-10)/4.5)**2
            if d>1.0 and ((x-17)/5.4)**2+((y-10)/5.4)**2<=1.0:
                px(img,x,y,BK)
    fo(img,17,10,1,1,WH)
    return img
sv(enemy_lollipop_fairy(),"enemy_lollipop_fairy")

print("  [캐릭터 완료] ───────────────────────────────")

# ─────────────────────────────────────────────────────────────────────────────
# 6. TILE: COOKIE PLATFORM  16×16
# ─────────────────────────────────────────────────────────────────────────────
def tile_cookie():
    img = ni(16,16)
    fr(img,0,0,15,15,CA1)
    # top highlight
    hl(img,0,15,0,(240,200,125,255))
    hl(img,0,15,1,(235,188,110,255))
    # right/bottom shadow
    vl(img,15,1,15,CA3); hl(img,0,15,15,CA3)
    vl(img,14,2,14,(180,118,52,255))
    # left side
    vl(img,0,0,14,CA2)
    # cookie chip dots
    for dx,dy in [(3,4),(7,3),(12,5),(5,9),(10,8),(2,12),(8,12),(14,11),(6,6),(11,13)]:
        px(img,dx,dy,CA3)
    # pink frosting drip on top
    for fx in [1,2,5,6,7,10,11,14]: px(img,fx,0,PK2)
    for fx,fy in [(2,1),(6,1),(6,2),(11,1)]: px(img,fx,fy,PK1)
    return img
sv(tile_cookie(),"tile_cookie_platform")

# ─────────────────────────────────────────────────────────────────────────────
# 7. TILE: MARSHMALLOW  16×16
# ─────────────────────────────────────────────────────────────────────────────
def tile_marshmallow():
    img = ni(16,16)
    fr(img,0,0,15,15,MM1)
    fr(img,0,11,15,15,MM2)
    fr(img,0,14,15,15,MM3)
    # top shine
    fr(img,2,1,13,3,WH)
    fr(img,3,1,12,1,(255,255,255,200))
    # soft texture ridges
    for y in [5,10]:
        for x in range(2,14):
            if x%3!=0: px(img,x,y,MM2)
    # outline
    hl(img,0,15,0,BK); hl(img,0,15,15,(180,155,162,255))
    vl(img,0,0,15,BK); vl(img,15,0,15,BK)
    # bounce arrow hint
    for bx,by in [(7,4),(8,4),(6,5),(9,5),(7,6),(8,6)]: px(img,bx,by,PK3)
    return img
sv(tile_marshmallow(),"tile_marshmallow")

# ─────────────────────────────────────────────────────────────────────────────
# 8. TILE: COTTON CANDY  16×16
# ─────────────────────────────────────────────────────────────────────────────
def tile_cotton():
    img = ni(16,16)
    fo(img,4,7,4,5,PU1); fo(img,8,5,5,5,PK1); fo(img,12,7,4,5,PU1)
    fo(img,6,9,4,4,PK1); fo(img,10,9,4,4,PU1)
    fr(img,0,9,15,15,PK2)
    # highlights
    fo(img,4,6,2,2,WH); fo(img,9,4,2,2,WH); fo(img,13,6,2,2,WH)
    hl(img,0,15,15,PK3); hl(img,0,15,14,(220,130,168,255))
    return img
sv(tile_cotton(),"tile_cotton_candy")

# ─────────────────────────────────────────────────────────────────────────────
# 9. TILE: ITEM BLOCK  16×16
# ─────────────────────────────────────────────────────────────────────────────
def tile_item_block():
    img = ni(16,16)
    fr(img,0,0,15,15,YL2)
    hl(img,0,15,0,BK); hl(img,0,15,15,BK)
    vl(img,0,0,15,BK); vl(img,15,0,15,BK)
    fr(img,1,1,14,2,YL1); fr(img,1,1,2,14,YL1)
    fr(img,1,14,14,14,YL3); fr(img,14,1,14,14,YL3)
    # "?" mark
    fr(img,7,3,9,5,PK3); fr(img,6,4,10,4,PK3)
    fr(img,9,4,10,7,PK3); fr(img,7,7,9,8,PK3)
    fr(img,7,10,9,11,PK3)
    return img
sv(tile_item_block(),"tile_item_block")

# ─────────────────────────────────────────────────────────────────────────────
# 10. ITEM: CANDY COIN  16×16
# ─────────────────────────────────────────────────────────────────────────────
def item_candy_coin():
    img = ni(16,16)
    oo(img,8,8,7,7,YL2,BK)
    fo(img,8,8,5,5,YL1)
    fo(img,8,8,3,3,YL2)
    fo(img,8,8,1,1,WH)
    # shine
    fo(img,5,5,1,1,WH); px(img,4,4,(255,255,255,180))
    # candy C logo on coin
    for sx,sy in [(6,7),(6,8),(6,9),(7,6),(7,10),(8,6),(9,7),(9,9)]:
        px(img,sx,sy,YL3)
    return img
sv(item_candy_coin(),"item_candy_coin")

# ─────────────────────────────────────────────────────────────────────────────
# 11. ITEM: SUGAR STAR  16×16
# ─────────────────────────────────────────────────────────────────────────────
def item_sugar_star():
    img = ni(16,16)
    draw = ImageDraw.Draw(img)
    cx,cy,ro,ri = 8,8,7,3
    pts_out=[]; pts_in=[]
    for i in range(10):
        a = math.pi*i/5 - math.pi/2
        r = ro if i%2==0 else ri
        pts_out.append((cx+r*math.cos(a), cy+r*math.sin(a)))
        r2 = (ro-2) if i%2==0 else max(1,ri-1)
        pts_in.append((cx+r2*math.cos(a), cy+r2*math.sin(a)))
    draw.polygon(pts_out, fill=YL2,  outline=None)
    draw.polygon(pts_in,  fill=YL1,  outline=None)
    draw.polygon(pts_out, fill=None, outline=BK)
    fo(img,8,8,2,2,WH); fo(img,8,8,1,1,PK1)
    px(img,6,5,WH); px(img,5,4,(255,255,255,180))
    return img
sv(item_sugar_star(),"item_sugar_star")

# ─────────────────────────────────────────────────────────────────────────────
# 12. ITEM: CAKE SLICE  16×16
# ─────────────────────────────────────────────────────────────────────────────
def item_cake_slice():
    img = ni(16,16)
    # layers bottom→top
    fr(img,2,12,14,14,CA1); hl(img,2,14,14,CA2)
    fr(img,2,9,14,11,WH)
    fr(img,2,6,14,8,CA1)
    fr(img,2,3,14,5,WH)
    # frosting top
    fr(img,1,1,15,2,PK2)
    for bx in range(1,15,3): fo(img,bx,1,1,2,PK1)
    # cherry
    oo(img,8,0,3,3,RD2,BK); fo(img,7,0,1,1,RD1)
    px(img,9,0,BK)
    # stem
    for sx,sy in [(8,-2),(9,-3),(10,-4)]: px(img,sx,sy,GR3)
    # outline sides
    vl(img,1,1,14,BK); vl(img,15,1,14,BK); hl(img,2,14,15,BK)
    # strawberry deco
    oo(img,9,12,2,2,RD1,RD3); px(img,9,10,GR2)
    # cream highlight
    fr(img,3,9,5,10,(255,252,245,255)); fr(img,3,3,5,4,(255,252,245,255))
    return img
sv(item_cake_slice(),"item_cake_slice")

# ─────────────────────────────────────────────────────────────────────────────
# 13. ITEM: RAINBOW CANDY  16×16
# ─────────────────────────────────────────────────────────────────────────────
def item_rainbow_candy():
    img = ni(16,16)
    oo(img,8,8,7,7,YL1,BK)
    stripe_colors = [RD2,(255,165,50,255),YL2,GR2,TL2,PU2]
    for i,c in enumerate(stripe_colors):
        y0 = 1+i*2; y1 = y0+2
        for y in range(max(1,y0), min(15,y1+1)):
            for x in range(1,15):
                if ((x-8)/7.5)**2+((y-8)/7.5)**2<=1.0:
                    px(img,x,y,c)
    # re-outline
    for y in range(0,16):
        for x in range(0,16):
            d = ((x-8)/7.5)**2+((y-8)/7.5)**2
            if d>1.0 and ((x-8)/8.8)**2+((y-8)/8.8)**2<=1.0:
                px(img,x,y,BK)
    # twist ends
    fo(img,2,8,2,1,YL2); fo(img,14,8,2,1,YL2)
    px(img,1,7,BK); px(img,1,9,BK); px(img,15,7,BK); px(img,15,9,BK)
    # shine
    fo(img,5,4,2,2,(255,255,255,160))
    return img
sv(item_rainbow_candy(),"item_rainbow_candy")

# ─────────────────────────────────────────────────────────────────────────────
# 14 & 15. UI: HEARTS  16×16
# ─────────────────────────────────────────────────────────────────────────────
HEART_FILL = [
    (4,3),(5,3),(9,3),(10,3),(11,3),
    (3,4),(4,4),(5,4),(6,4),(7,4),(8,4),(9,4),(10,4),(11,4),(12,4),
    (3,5),(4,5),(5,5),(6,5),(7,5),(8,5),(9,5),(10,5),(11,5),(12,5),
    (3,6),(4,6),(5,6),(6,6),(7,6),(8,6),(9,6),(10,6),(11,6),(12,6),
    (3,7),(4,7),(5,7),(6,7),(7,7),(8,7),(9,7),(10,7),(11,7),(12,7),
    (4,8),(5,8),(6,8),(7,8),(8,8),(9,8),(10,8),(11,8),
    (5,9),(6,9),(7,9),(8,9),(9,9),(10,9),
    (6,10),(7,10),(8,10),(9,10),
    (7,11),(8,11),
]
HEART_OUTLINE = [
    (3,3),(6,3),(8,3),(12,3),
    (2,4),(3,5),(2,5),(2,6),(2,7),(13,4),(13,5),(13,6),(13,7),
    (3,8),(13,8),(4,9),(12,9),(5,10),(11,10),(6,11),(10,11),(7,12),(8,12),(9,12),
]

def ui_heart(full):
    img = ni(16,16)
    c = RD2 if full else (180,150,155,255)
    h1= RD1 if full else (210,185,188,255)
    for hx,hy in HEART_FILL: px(img,hx,hy,c)
    if full:
        for hx,hy in [(4,4),(5,4),(4,5),(9,4),(10,4),(12,4)]: px(img,hx,hy,h1)
    for ox,oy in HEART_OUTLINE: px(img,ox,oy,BK if full else (150,130,135,255))
    return img
sv(ui_heart(True), "ui_heart_full")
sv(ui_heart(False),"ui_heart_empty")

print("  [타일·아이템·UI 완료] ──────────────────────")

# ─────────────────────────────────────────────────────────────────────────────
# 16. PROP: CUPCAKE HOUSE  48×64
# ─────────────────────────────────────────────────────────────────────────────
def prop_cupcake_house():
    img = ni(48,64)
    # ── cup/base (brick) ──
    fr(img,3,38,45,63,CA2)
    for row in range(5):
        y = 38+row*5
        off = (row%2)*8
        for bx in range(0-off,50,16):
            x0=max(4,bx); x1=min(44,bx+14)
            if x1>x0: fr(img,x0,y,x1,y+3,CA1)
    # brick grout lines
    for row in range(5):
        hl(img,4,44,38+row*5+4,CH2)
    # door arch
    fr(img,18,47,29,63,CH2)
    fo(img,24,47,6,6,CH2); fo(img,24,47,5,5,CH3)
    # door knob
    oo(img,27,54,1,1,YL2,BK)
    # windows
    for wx in [7,36]:
        fr(img,wx,45,wx+7,52,TL1)
        fr(img,wx,45,wx+3,48,TL2)
        vl(img,wx+3,45,52,BK)
        hl(img,wx,wx+7,44,CA3); hl(img,wx,wx+7,53,CA3)
        vl(img,wx-1,44,53,CA3); vl(img,wx+8,44,53,CA3)
        px(img,wx+1,46,WH)
    # ── frosting dome ──
    oo(img,24,32,22,18,WH,BK)
    fo(img,24,32,20,16,PK1)
    fo(img,24,27,15,12,WH)
    fo(img,24,24,10,8,(255,250,248,255))
    # drips
    for dx,dl in [(5,4),(9,7),(14,5),(19,8),(24,3),(29,7),(34,4),(39,6),(43,3)]:
        fr(img,dx,36,dx+1,36+dl,PK1)
        fo(img,dx,36+dl+1,1,1,PK2)
    # sprinkles
    for sx,sy,sc in [(13,22,TL2),(19,18,YL2),(26,16,GR2),(32,19,RD1),(17,28,PU2),(31,26,TL3),(22,25,YL1),(28,30,PK3)]:
        fr(img,sx,sy,sx+2,sy,sc)
    # ── cherry on top ──
    oo(img,24,12,5,5,RD2,BK)
    fo(img,22,10,2,2,RD1)
    px(img,24,7,GR3); px(img,25,6,GR3); px(img,26,5,GR3)
    # ── candy cane decoration ──
    fr(img,39,15,41,35,WH)
    for sy in range(15,35,4): fr(img,39,sy,41,sy+2,RD2)
    oo(img,39,13,3,3,WH,BK)
    for y in range(13,16): vl(img,38,y,y,BK); vl(img,42,y,y,BK)
    # ── base outline ──
    hl(img,3,45,37,BK); vl(img,2,37,63,BK); vl(img,46,37,63,BK)
    hl(img,3,45,63,BK)
    return img
sv(prop_cupcake_house(),"prop_cupcake_house")

# ─────────────────────────────────────────────────────────────────────────────
# 17. PROP: LOLLIPOP TREE  32×56
# ─────────────────────────────────────────────────────────────────────────────
def prop_lollipop_tree():
    img = ni(32,56)
    # stick
    fr(img,14,28,18,55,WH)
    for sy in range(28,55,6): fr(img,14,sy,18,sy+2,RD2)
    vl(img,13,28,55,BK); vl(img,19,28,55,BK)
    hl(img,14,18,55,BK)
    # candy circle — alternating LL1/LL2 wedge sectors
    draw = ImageDraw.Draw(img)
    for i in range(6):
        start = i*60-90; end = start+60
        fc = LL1 if i%2==0 else LL2
        draw.pieslice([1,1,31,31], start=start, end=end, fill=fc, outline=None)
    # outline
    for y in range(0,32):
        for x in range(0,32):
            d  = ((x-16)/15.5)**2+((y-16)/15.5)**2
            d2 = ((x-16)/17.0)**2+((y-16)/17.0)**2
            if d>1.0 and d2<=1.0: px(img,x,y,BK)
            elif d>1.0: px(img,x,y,T)
    # center
    fo(img,16,16,4,4,WH); fo(img,16,16,3,3,WH)
    oo(img,16,16,3,3,WH,BK)
    fo(img,16,16,1,1,(220,180,180,255))
    # shine
    fo(img,10,9,3,3,(255,255,255,140))
    return img
sv(prop_lollipop_tree(),"prop_lollipop_tree")

# ─────────────────────────────────────────────────────────────────────────────
# 18. PROP: GOAL FLAG  16×48
# ─────────────────────────────────────────────────────────────────────────────
def prop_goal_flag():
    img = ni(16,48)
    # pole
    fr(img,7,4,9,47,(200,200,200,255))
    vl(img,6,4,47,(160,160,160,255)); vl(img,10,4,47,WH)
    hl(img,7,9,47,BK)
    # top ball
    oo(img,8,4,3,3,YL2,BK); px(img,7,3,YL1)
    # flag
    fr(img,9,5,15,15,PK2)
    fr(img,9,5,15,8,PK3)
    # star
    for sx,sy in [(12,10),(11,10),(13,10),(12,9),(12,11)]: px(img,sx,sy,YL1)
    hl(img,9,15,4,BK); hl(img,9,15,16,BK)
    vl(img,15,4,16,BK)
    return img
sv(prop_goal_flag(),"prop_goal_flag")

# ─────────────────────────────────────────────────────────────────────────────
# 19. BG: CLOUD  32×20
# ─────────────────────────────────────────────────────────────────────────────
def bg_cloud():
    img = ni(32,20)
    CL=(255,248,240,255); CL2=(252,240,228,255); CLS=(235,210,200,255)
    fo(img,8,12,7,6,CL); fo(img,16,10,9,8,CL); fo(img,24,12,7,6,CL)
    fo(img,16,15,14,5,CL2)
    fo(img,13,8,4,3,WH)
    fo(img,16,17,12,3,CLS)
    return img
sv(bg_cloud(),"bg_cloud")

# ─────────────────────────────────────────────────────────────────────────────
# 20. BG: COTTON CANDY TREE  24×40
# ─────────────────────────────────────────────────────────────────────────────
def bg_cotton_tree():
    img = ni(24,40)
    # trunk
    fr(img,10,24,14,39,GR3); vl(img,9,24,39,GR2); vl(img,15,24,39,(48,98,40,255))
    hl(img,10,14,39,BK)
    # fluffy top
    fo(img,12,14,10,10,GR1)
    fo(img,7,12,7,8,GR1); fo(img,17,12,7,8,GR1)
    fo(img,12,18,8,6,GR2)
    # highlights
    fo(img,9,8,3,3,WH); fo(img,15,7,2,3,(200,240,180,255))
    return img
sv(bg_cotton_tree(),"bg_cotton_tree")

# ─────────────────────────────────────────────────────────────────────────────
# 21. ENEMY: CARAMEL BLOB (World 3)  20×20
# ─────────────────────────────────────────────────────────────────────────────
def enemy_caramel_blob():
    img = ni(20,20)
    oo(img,10,11,9,8,YL2,BK)
    fo(img,10,10,7,6,YL1)
    # drip top
    fo(img,10,3,4,4,YL2); oo(img,10,3,4,4,YL2,BK)
    fo(img,10,5,2,2,YL1)
    # evil eyes
    fr(img,6,9,7,10,BK); fr(img,13,9,14,10,BK)
    px(img,6,9,WH); px(img,13,9,WH)
    # angry brows
    hl(img,5,8,8,BK); hl(img,12,8,15,BK)
    px(img,5,7,BK); px(img,15,7,BK)
    # mean mouth
    for mx,my in [(7,14),(8,15),(9,15),(10,15),(11,15),(12,15),(13,14)]: px(img,mx,my,BK)
    hl(img,8,12,16,CA3)
    return img
sv(enemy_caramel_blob(),"enemy_caramel_blob")

print("  [배경 오브젝트 완료] ───────────────────────")

# ─────────────────────────────────────────────────────────────────────────────
# 22. MASTER SPRITE SHEET
# ─────────────────────────────────────────────────────────────────────────────
print("\n📋 스프라이트 시트 합성 중...")

sheet_assets = [
    ("cookie_idle",          "쿠키 대기"),
    ("cookie_run1",          "달리기 1"),
    ("cookie_run2",          "달리기 2"),
    ("cookie_run3",          "달리기 3"),
    ("cookie_run4",          "달리기 4"),
    ("cookie_jump",          "점프"),
    ("enemy_donut",          "도넛 롤러"),
    ("enemy_lollipop_fairy", "롤리팝 요정"),
    ("enemy_caramel_blob",   "캐러멜 블롭"),
    ("tile_cookie_platform", "쿠키 발판"),
    ("tile_marshmallow",     "마시멜로"),
    ("tile_cotton_candy",    "솜사탕"),
    ("tile_item_block",      "아이템 블록"),
    ("item_candy_coin",      "캔디 코인"),
    ("item_sugar_star",      "슈거 스타"),
    ("item_cake_slice",      "케이크 조각"),
    ("item_rainbow_candy",   "레인보우 캔디"),
    ("ui_heart_full",        "하트 (HP)"),
    ("ui_heart_empty",       "하트 (빈)"),
    ("prop_cupcake_house",   "컵케이크 건물"),
    ("prop_lollipop_tree",   "롤리팝 나무"),
    ("bg_cotton_tree",       "솜사탕 나무"),
    ("prop_goal_flag",       "골 깃발"),
    ("bg_cloud",             "구름"),
]

CELL   = 80
COLS   = 6
ROWS   = math.ceil(len(sheet_assets)/COLS)
PAD    = 12
TITLE_H= 50
SW = COLS*CELL + PAD*2
SH = ROWS*CELL + PAD*2 + TITLE_H

sheet = Image.new('RGBA',(SW,SH),(22,14,32,255))
draw  = ImageDraw.Draw(sheet)

# title bar gradient feel
draw.rectangle([0,0,SW,TITLE_H], fill=(40,22,55,255))
draw.rectangle([0,TITLE_H-2,SW,TITLE_H], fill=(212,108,148,255))
draw.text((PAD, 10), "SWEET LAND ADVENTURE", fill=(255,200,220,255))
draw.text((PAD, 28), "PIXEL ASSET SHEET  v1.0  |  32×32 native  ×4 display", fill=(180,160,200,255))

for i,(name,label) in enumerate(sheet_assets):
    col = i%COLS; row = i//COLS
    cx  = PAD + col*CELL
    cy  = TITLE_H + PAD + row*CELL

    # cell bg
    draw.rectangle([cx,cy,cx+CELL-4,cy+CELL-4], fill=(32,20,45,255), outline=(60,38,80,255))

    if name in ASSETS:
        sprite = ASSETS[name]
        max_d  = CELL - 24
        ratio  = min(max_d/sprite.width, max_d/sprite.height)
        nw = max(1, int(sprite.width*ratio))
        nh = max(1, int(sprite.height*ratio))
        disp = sprite.resize((nw,nh), Image.NEAREST)
        ox = cx + (CELL - nw)//2 - 2
        oy = cy + (CELL - nh - 14)//2
        sheet.paste(disp,(ox,oy),disp)

    # label
    draw.text((cx+4, cy+CELL-16), label, fill=(200,178,215,255))

sheet.save(f"{OUT}/sprite_sheet.png")
print(f"  ✓ sprite_sheet.png  ({SW}×{SH})")
print(f"\n✅ 총 {len(sheet_assets)+1}개 에셋 저장 완료 → {OUT}")
