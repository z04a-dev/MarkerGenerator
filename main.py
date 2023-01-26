#by z04a
from PIL import Image, ImageDraw, ImageFont
import qrcode, hashlib
from alive_progress import alive_bar
import time, sys

#библиотека и код для ввода параметров при запуске скприта
import argparse
parser = argparse.ArgumentParser(description='mark generator')
parser.add_argument('library', type=str, help='Library name')
parser.add_argument('-l','--legacy', action='store_true', help='use legacy renderer')
parser.add_argument('-b','--blank', action='store_true', help='do not draw arrows')
parser.add_argument('-t','--text', action='store_true', help='disable text')
args = parser.parse_args()

DEFAULT_IDENTIFIER = "3257b0ae1f8d05fed50a757017a93688" #md5 идентификатор приложения

LIBRARY_HASH = hashlib.md5(args.library.encode('utf-8')).hexdigest() #md5 идентификатор библиотеки

def create(room):
    
    #Сборка строки для генерации qr кода

    ROOM_HASH = hashlib.md5(room.encode('utf-8')).hexdigest() #md5 идентификатор кабинета

    FINAL_HASH = DEFAULT_IDENTIFIER + " " + LIBRARY_HASH + " " + ROOM_HASH #сборка в одну строку

    #---------------

    upscaleqr_size = 1150 #разрешение, до которого будет масштабироваться qr код (1150x1150 к примеру)

    width = 2808 #конечная ширина метки
    height = 1984 #конечная высота метки

    
    #создание qr кода
    qrimg = qrcode.make(FINAL_HASH)
    upqr = qrimg.resize((upscaleqr_size,upscaleqr_size),resample=1)

    for i in range(1,3):
        if(i == 2):
            width = 1984
            height = 2808
        #создание фона
        newImg = Image.new(mode = "RGB", size = (width,height), color = (255,255,255))

        #заполнение диагональными полосками ## DEPRECATED. PLEASE DO NOT USE.
        if args.legacy:
            x = 0
            for number in range(40):
                img1 = ImageDraw.Draw(newImg)
                img1.line([(x - width,0),(x,height)], fill="black", width = 12)
                x += width/15
        #----------------

        if not args.legacy:
            
            if(i == 1):
                newImg.paste(diag_hor,(0,0))
            else:
                newImg.paste(diag_ver,(0,0))
            
        
        #вставка qr кода в центр изображения
        newImg.paste(upqr, (int(width/2 - upscaleqr_size/2), int(height/2 - upscaleqr_size/2)))

        #вставка стрелки
        if not args.blank:
            newImg.paste(arrow,(width-320,int(height/2-982/2)),arrow.convert('RGBA'))
            newImg.paste(arrow,(160,int(height/2-982/2)),arrow.convert('RGBA'))

        #вставка названия
        if not args.text:
            vot = Image.new(mode = "RGB", size = (width,80), color = (255, 255, 255))
            newImg.paste(vot, (0,height-80))
            idraw = ImageDraw.Draw(newImg)
            font = ImageFont.truetype("arial.ttf", size=80)
            idraw.text((0,height-80), room, font=font, fill=(0, 0, 0))

        #сохранение
        if i == 1:
            imgName = "result_hor/hor-" + args.library + "-" + room + ".png"
            newImg.save(imgName)
        else:
            imgName = "result_ver/vert-" + args.library + "-" + room + ".png"
            newImg.save(imgName)

#---------------main code---------------#
        
#пробуем открыть текстовый файл        
try:
    room_file = open('library.txt', 'r')
except:
    print('ERR: File not found. Did you put your data in library.txt?')
    sys.exit() # если файл не найден, программа закрывается.

if(args.legacy):
    print('WRN: using LEGACY_RENDERER is deprecated.')

#запись всех строк в список
data = room_file.read()
list_data = data.split("\n")
room_file.close()

try:
    diag_hor = Image.open('src/diag_hor.png')
    diag_ver = Image.open('src/diag_ver.png')
    arrow = Image.open('src/arrow.png').convert('RGBA')
except:
    print('ERR: src images not found')
    sys.exit() # если файл не найден, программа закрывается.

#вывод прогресса
with alive_bar(len(list_data)) as bar: 
    for i in range(0,len(list_data)):
        create(list_data[i])
        bar(i/100 * (100 / len(list_data)))
        

    

           


