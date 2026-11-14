import sys, re, json
sys.path.insert(0,'.')
from shape import shape, bounds, to_path, F
import cairosvg
LOGO='/home/user/arwa/clients/otlobny-emaar/04-identity/02-logo/'
AR='شركة اطلبني إعمار المحدودة'; EN='OTLOBNY EMAR COMPANY LTD.'
P=dict(ar_font='tajawal/Tajawal-Bold.ttf', en_font='ibmplexsans-static/IBMPlexSans-SemiBold.ttf',
       right=307.711, width=float(sys.argv[1]) if len(sys.argv)>1 else 222,
       ar_top=float(sys.argv[2]) if len(sys.argv)>2 else 103.258, gap=float(sys.argv[3]) if len(sys.argv)>3 else 4.0,
       en_cap=float(sys.argv[4]) if len(sys.argv)>4 else 8.0)
def layout(P):
    ar=shape(F+P['ar_font'],AR); b=bounds(ar)
    s=P['width']/(b[2]-b[0]); size_ar=s*1000
    ox=P['right']-b[2]*s; base_ar=P['ar_top']+b[3]*s
    ar_d=to_path(ar,size_ar,ox,base_ar); ar_box=(ox+b[0]*s, base_ar-b[3]*s, P['right'], base_ar-b[1]*s)
    en0=shape(F+P['en_font'],EN); capH=698 # IBM Plex Sans cap height
    size_en=P['en_cap']/capH*1000; se=size_en/1000
    b0=bounds(en0); n=len(EN)-1
    # tracking so ink width == arabic ink width
    tr=(P['width']/se-(b0[2]-b0[0]))/n/1000
    en=shape(F+P['en_font'],EN,tr); be=bounds(en)
    oxe=P['right']-be[2]*se
    base_en=ar_box[3]+P['gap']+P['en_cap']
    en_d=to_path(en,size_en,oxe,base_en); en_box=(oxe+be[0]*se, base_en-be[3]*se, P['right'], base_en-be[1]*se)
    return dict(size_ar=size_ar,size_en=size_en,tracking_em=tr,ar_d=ar_d,en_d=en_d,ar_box=ar_box,en_box=en_box,base_ar=base_ar,base_en=base_en)
if __name__=='__main__':
    L=layout(P)
    print(json.dumps({k:v for k,v in L.items() if not k.endswith('_d')},indent=1))
    src=open(LOGO+'otlobny-emaar_logo_wordmark-colour_ar_v01.svg').read()
    paths=re.findall(r'  <path [^>]*/>',src)
    H=max(L['en_box'][3],124.597)
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 307.711 {H:.3f}">'+'<rect width="100%" height="100%" fill="#fff"/>'+''.join(paths)+f'<path fill="#525456" d="{L["ar_d"]}"/><path fill="#525456" d="{L["en_d"]}"/></svg>'
    cairosvg.svg2png(bytestring=svg.encode(),write_to='try.png',output_width=1400)
