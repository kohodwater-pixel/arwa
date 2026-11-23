import sys; sys.path.insert(0,'.')
from mark import mark_paths
import cairosvg, io, numpy as np
from PIL import Image
S=8
ps=''.join(f'<path d="{p}"/>' for p in mark_paths())
svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{160*S}" height="{140*S}"><rect width="100%" height="100%" fill="black"/><g transform="scale({S}) translate(-130,-60)" fill="white">{ps}</g></svg>'
v=np.asarray(Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode()))).convert('L'))>128
r=np.asarray(Image.open('ref_mark_mask.png'))>128
print('IoU',(v&r).sum()/(v|r).sum())
o=np.zeros(v.shape+(3,),'uint8'); o[r&v]=(200,200,200); o[r&~v]=(255,60,60); o[v&~r]=(60,140,255)
Image.fromarray(o).save('mark_overlay_diff.png')
