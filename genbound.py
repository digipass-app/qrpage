from PIL import Image, ImageDraw
im = Image.new('RGBA', (620, 700), (255, 255, 255, 0))
draw = ImageDraw.Draw(im)
#draw.line((619,600, 619,700), fill=0,width=5)
#draw.line((520,699, 620,699), fill=0,width=5)
#draw.line((0,600, 0,700), fill=0,width=5)
#draw.line((0,699, 100,699), fill=0,width=5)
#draw.line((0,0, 100,0), fill=0,width=5)

im.show()
im.save('blank.png')
