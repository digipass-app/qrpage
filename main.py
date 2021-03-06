from PIL import Image, ImageDraw, ImageFont
import qrcode
import os
import numpy as np
import concat
import pandas
from resizeimage import resizeimage


def filter_xa0(msgList):
    clean_msgList = []
    for msg in msgList:
        clean_msgList.append(str(msg).upper().replace(u'\xa0', u' ').strip())
    return clean_msgList


## CSV data import
raw = pandas.read_csv("data.csv")

db_raw = []

for r in raw:
    if len(r) > 0:
        db_raw.append(r)

bPath = os.path.abspath("border/")
abPath = os.path.abspath("qr/")
tmpPath = os.path.abspath("tmp/")
link = "https://www.digipass.app/"
# db_raw = ["000000","000001","000002","000003","000004","000005","00006","00007","111111","222222","333333","444444","555555","666666","777777"]
# db = []
# for s in db_raw:
#    d  = int(s)
#    db.append(hex(d).split('x')[-1])
db = db_raw

print("--- clearing old files...")

path = 'tmp/'
listing = os.listdir(path)
for infile in listing:
    if infile == "foot.png" or infile == ".DS_Store" or infile == "blank.png":
        continue
    os.remove(tmpPath + "/" + infile)

path = 'qr/'
listing = os.listdir(path)
for infile in listing:
    if infile == "foot.png" or infile == ".DS_Store" or infile == "blank.png" or "longblank.png":
        continue
    os.remove(abPath + "/" + infile)

path = 'qr/horizontal'
listing = os.listdir(path)
for infile in listing:
    os.remove(abPath + "/horizontal/" + infile)

path = 'qr/vertical'
listing = os.listdir(path)
for infile in listing:
    os.remove(abPath + "/vertical/" + infile)

print("--- cleared.")
print("--- rendering QR code for", len(db), "emps...")

named = []
i = 0
# generate qr img
for emp_id in db:
    if i % 100 == 0:
        print(str(i * 100 / len(db)) + "% done..")
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=18,
        border=3
    )
    qr.add_data(link + emp_id)
    qr.make(fit=True)
    img_raw = qr.make_image()

    K = str(db_raw[i])
    while len(K) < 6:
        K = "0" + K
    img = resizeimage.resize_cover(img_raw, [620, 620])
    pathImg = abPath + '/' + K + '.png'
    print(pathImg)
    img.save(pathImg)
    named.append(K)
    i += 1

print("---", len(db), "QR-code rendered.")

print("--- extendig images size...")

ii = 0
write_blank = False
# write text to all files
path = 'qr'
listing = os.listdir(path)
for infile in listing:
    if infile in ["blank.png", "horizontal", "vertical", "longblank.png"]:
        continue
    if ii % 100 == 0:
        print(str(ii * 100 / len(listing)) + "% done..")
    name = infile[:-4]

    while name[0] == "0":
        name = name[1:]

    base = Image.open(path + "/" + infile).convert("RGBA")
    print(base.size)

    txt = Image.new("RGBA", base.size, (255, 255, 255, 0))
    # print(txt)
    # if not write_blank:
    #    txt = Image.new('RGBA', (620, 700), (255, 255, 255, 0))
    #    txt.save(abPath + '/' + "blank.png"
    #    write_blank = True

    w, h = base.size

    draw = ImageDraw.Draw(txt)
    draw.fontmode = "1"

    # python = Image.open("python.png").convert("RGBA")
    # dota = Image.open("dota.png").convert("RGBA")
    # Image.alpha_composite(dota, python).save("haha.png")
    print(base)
    print(txt)
    pathOut = tmpPath + '/' + infile[:-4] + ".png"
    print(pathOut)
    out = Image.alpha_composite(base, txt).save(pathOut)
    # out.save(tmpPath + '/' + infile[:-4] + ".png"
    ii += 1

print("--- concat things up..")
for j in named:
    images = ["tmp/" + j + ".png", "tmp/foot.png"]
    output = concat.concat_n_images(images)

    out = Image.fromarray(output)
    out.save(abPath + '/' + j + ".png")

print("--- done.")
# write text to all files (REAL)
print("--- rendering Emp_Id tagged for", len(db), "emps...")

path = 'qr'
listing = os.listdir(path)
i = 0
for infile in listing:
    if infile in ["blank.png", "horizontal", "vertical", "longblank.png"]:
        continue
    if i % 100 == 0:
        print(str(i * 100 / len(listing)) + "% done..")
    name = infile[:-4]

    base = Image.open(path + "/" + infile).convert('RGBA')
    txt = Image.new('RGBA', base.size, (255, 255, 255, 0))

    W, H = base.size

    while name[0] == "0":
        name = name[1:]

    draw = ImageDraw.Draw(txt)
    draw.fontmode = "1"
    font = ImageFont.truetype("Gotham-Book.ttf", 110)
    w, h = font.getsize(name)
    draw.text(((W - w) / 2, H - 110), name, font=font, fill=(0, 0, 0, 255))

    out = Image.alpha_composite(base, txt)
    out.save(abPath + '/' + infile[:-4] + ".png")
    i += 1

print("---", len(db), "Emp_Id has been tagged.")

bPath = os.path.abspath("border/")
abPath = os.path.abspath("qr/")
tmpPath = os.path.abspath("tmp/")
path = 'qr'
listing = os.listdir(path)

while True:
    try:
        # col_s = input("Please input number of QR-code per line (col) >> ")
        col_s = 13
        col = int(col_s)
        break
    except:
        continue

print("--- creating horizontal images...")

# concat
list_im = []

row = 0
count = 0

saved = []
i = 0
while i < (len(listing)):
    infile = listing[i]
    if infile in ["blank.png", "horizontal", "vertical", "longblank.png"]:
        i += 1
        continue
    if row % 16 == 15:
        list_im.append(bPath + '/botleft.png')
        for _ in range(11):
            list_im.append(bPath + '/down.png')
        list_im.append(bPath + '/botright.png')
        row += 1
    if row % 16 == 0:
        list_im.append(bPath + '/topleft.png')
        for _ in range(11):
            list_im.append(bPath + '/up.png')
        list_im.append(bPath + '/topright.png')
        row += 1
    if count % 13 == 0:
        list_im.append(bPath + '/left.png')
        list_im.append(abPath + '/' + infile)
        count += 2
        i += 1
        continue
    if count % 13 == 12:
        list_im.append(bPath + '/right.png')
        count += 1
        row += 1
        continue
    list_im.append(abPath + '/' + infile)
    count += 1
    i += 1

# Cut here

all_imgs = []
for i in list_im:
    all_imgs.append(Image.open(i))

print("--- done.")
print("--- creating horizontal images...")

# all_imgs = [Image.open(i) for i in list_im]
cc = 0
x = len(all_imgs)
while x % col != 0:
    cc += 1
    x += 1
for _ in range(cc - 1):
    all_imgs.append(Image.open(abPath + '/blank.png'))

all_imgs = all_imgs
all_imgs.append(Image.open(bPath + '/right.png'))
all_imgs.append(Image.open(bPath + '/botleft.png'))
for _ in range(11):
    all_imgs.append(Image.open(bPath + '/down.png'))
all_imgs.append(Image.open(bPath + '/botright.png'))

k = 0
for j in range(0, len(all_imgs), col):
    if k % 10 == 0:
        print(str((j / (len(all_imgs))) * 100) + "% done..")
    imgs = all_imgs[j:j + col]
    min_shape = sorted([(np.sum(i.size), i.size) for i in imgs])[0][1]
    # arra = (np.asarray(i.resize(min_shape)) for i in imgs)

    arra = []
    for i in imgs:
        # print(i)
        arra.append(
            np.asarray(i.resize(min_shape))
        )

    print("-------arra:")
    # print(np.asarray(i.resize(min_shape)))
    print(arra)
    imgs_comba = np.hstack(arra)

    imgs_comb = Image.fromarray(imgs_comba)
    K = str(k)
    while len(K) < 3:
        K = "0" + K
    imgs_comb.save(abPath + '/' + 'horizontal/' + K + '.png')
    k += 1

print("---", k, "horizontal images has been created.")

print("--- concating images to fit A4 size...")

while True:
    try:
        # row_s = input("Please input number of line per page (row) >> ")
        row_s = 16
        row = int(row_s)
        # if row > k:
        # continue
        break
    except:
        continue

path = 'qr/horizontal'
listing2 = os.listdir(path)
list_im = []

for infile in listing2:
    if infile in ["blank.png", "horizontal", "vertical", "longblank.png"]:
        continue
    list_im.append(abPath + '/horizontal/' + infile)

all_imgs = [Image.open(i) for i in list_im]

while len(all_imgs) % row != 0:
    all_imgs.append(Image.open(abPath + '/longblank.png'))

k = 0
for j in range(0, len(all_imgs), row):
    imgs = all_imgs[j:j + row]
    min_shape = sorted([(np.sum(i.size), i.size) for i in imgs])[0][1]

    arra = []
    for i in imgs:
        print(i)
        arra.append(
            np.asarray(i.resize(min_shape))
        )

    imgs_comb = np.hstack(arra)
    # imgs_comb = np.hstack((np.asarray(i.resize(min_shape)) for i in imgs))

    arra = []
    for i in imgs:
        print(i)
        arra.append(
            np.asarray(i.resize(min_shape))
        )

    imgs_comba = np.vstack(arra)
    # imgs_comb = np.vstack((np.asarray(i.resize(min_shape)) for i in imgs))

    imgs_comb = Image.fromarray(imgs_comba)

    K = str(k)
    while len(K) < 3:
        K = "0" + K
    imgs_comb.save(abPath + '/' + 'vertical/' + K + '.png')
    k += 1
    print(k, "images has been created.")
print("---", k, "images has been created.")
print("--- All done!")
