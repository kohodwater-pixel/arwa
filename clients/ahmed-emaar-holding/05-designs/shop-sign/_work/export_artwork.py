import cairosvg, shutil
P='../ahmed-emaar-holding_shop-sign_option-{o}_{k}_ar-en_v01.{e}'
for o in 'ab':
    shutil.copy(f'option-{o}_full.svg', P.format(o=o,k='artwork-1to10',e='svg'))
    cairosvg.svg2pdf(url=f'option-{o}_full.svg', write_to=P.format(o=o,k='artwork-1to10',e='pdf'))
    cairosvg.svg2png(url=f'option-{o}_full.svg', write_to=P.format(o=o,k='preview',e='png'), output_width=2500, output_height=600)
