#by z04a
from PIL import Image, ImageDraw
import qrcode, hashlib

#библиотека и код для ввода параметров при запуске скприта
import argparse
parser = argparse.ArgumentParser(description='mark generator')
parser.add_argument('library', type=str, help='Library name')
args = parser.parse_args()

DEFAULT_IDENTIFIER = "3257b0ae1f8d05fed50a757017a93688" #md5 идентификатор приложения

def create(room):
    #Сборка строки для генерации qr кода

    LIBRARY_HASH = hashlib.md5(args.library.encode('utf-8')).hexdigest() #md5 идентификатор библиотеки

    ROOM_HASH = hashlib.md5(room.encode('utf-8')).hexdigest() #md5 идентификатор кабинета

    FINAL_HASH = DEFAULT_IDENTIFIER + " " + LIBRARY_HASH + " " + ROOM_HASH #сборка в одну строку
    #---------------

    width = 2808 #конечная ширина метки
    height = 1984 #конечная высота метки
    upscaleqr_size = 1150 #разрешение, до которого будет масштабироваться qr код (1150x1150 к примеру)

    #создание qr кода
    qrimg = qrcode.make(FINAL_HASH)
    upqr = qrimg.resize((upscaleqr_size,upscaleqr_size),resample=1)

    #создание фона
    img = Image.new(mode = "RGB", size = (width,height), color = (255,255,255))

    #заполнение диагональными полосками
    x = 0
    for number in range(40):
        img1 = ImageDraw.Draw(img)
        img1.line([(x - width,0),(x,height)], fill="black", width = 12)
        x += width/15

    #вставка qr кода в центр изображения
    newImg = img.copy()
    newImg.paste(upqr, (int(width/2 - upscaleqr_size/2), int(height/2 - upscaleqr_size/2)))

    #вставка стрелки
    arrow = Image.open('src/arrow.png').convert('RGBA')
    newImg.paste(arrow,(width-320,int(982/2)),arrow.convert('RGBA'))
    newImg.paste(arrow,(160,int(982/2)),arrow.convert('RGBA'))

    #сохранение
    imgName = "result/" + args.library + "-" + room + ".png"
    newImg.save(imgName)
    
with open("library.txt") as file:
    for line in file:
        room = line.rstrip()
        create(room)
