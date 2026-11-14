import uharfbuzz as hb, sys, json
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
F='/home/user/arwa/assets/fonts/'
def shape(path, text, tracking_em=0.0):
    data=open(path,'rb').read()
    face=hb.Face(data); font=hb.Font(face)
    buf=hb.Buffer(); buf.add_str(text); buf.guess_segment_properties()
    hb.shape(font,buf,{"kern":True,"liga":True})
    tt=TTFont(path); gs=tt.getGlyphSet(); order=tt.getGlyphOrder(); upem=tt['head'].unitsPerEm
    glyphs=[]; x=0
    n=len(buf.glyph_infos)
    for i,(info,pos) in enumerate(zip(buf.glyph_infos,buf.glyph_positions)):
        name=order[info.codepoint]
        glyphs.append((name,x+pos.x_offset,pos.y_offset,info.cluster))
        x+=pos.x_advance
        if tracking_em and i<n-1: x+=tracking_em*upem
    return dict(glyphs=glyphs,gs=gs,upem=upem,direction=buf.direction,advance=x,tt=tt)
def bounds(sh):
    bp=BoundsPen(sh['gs'])
    for name,x,y,_ in sh['glyphs']:
        sh['gs'][name].draw(TransformPen(bp,(1,0,0,1,x,y)))
    return bp.bounds
def to_path(sh,size,ox,baseline):
    s=size/sh['upem']
    pen=SVGPathPen(sh['gs'],ntos=lambda v: ('%.3f'%v).rstrip('0').rstrip('.'))
    for name,x,y,_ in sh['glyphs']:
        sh['gs'][name].draw(TransformPen(pen,(s,0,0,-s,ox+x*s,baseline-y*s)))
    return pen.getCommands()
if __name__=='__main__':
    sh=shape(F+'tajawal/Tajawal-Bold.ttf','شركة اطلبني إعمار المحدودة')
    print(sh['direction'],[(g[0],g[3]) for g in sh['glyphs']])
    print(bounds(sh), sh['upem'])
