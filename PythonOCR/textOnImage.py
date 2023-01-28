import math
from PIL import ImageDraw
from PIL import Image, ImageFont
import cv2
import ast
import json

input = [[[[2879.0, 365.0], [3398.0, 57.0], [3466.0, 177.0], [2946.0, 485.0]],
          ('UniveRsi', 0.8513504862785339)],
         [[[1482.0, 894.0], [2944.0, 288.0], [3031.0, 507.0], [1569.0,
                                                               1113.0]],
          ('I WosKaFFhe ', 0.8089697957038879)],
         [[[1688.0, 1217.0], [2376.0, 1041.0], [2441.0, 1307.0],
           [1753.0, 1483.0]], ('Hello', 0.9300691485404968)],
         [[[2435.0, 1268.0], [3120.0, 1206.0], [3138.0, 1421.0],
           [2454.0, 1483.0]], ('Univesity', 0.947674036026001)],
         [[[1933.0, 1533.0], [2222.0, 1502.0], [2280.0, 2080.0],
           [1990.0, 2110.0]], ('Work', 0.6628354787826538)],
         [[[2738.0, 1701.0], [3570.0, 1743.0], [3556.0, 2019.0],
           [2725.0, 1977.0]], ('Weanesday', 0.9160200953483582)],
         [[[1318.0, 2330.0], [2746.0, 2202.0], [2765.0, 2421.0],
           [1336.0, 2548.0]], ('my name is yamn', 0.9382486343383789)],
         [[[2304.0, 2560.0], [3158.0, 2612.0], [3143.0, 2874.0],
           [2289.0, 2822.0]], ('Something', 0.9717532396316528)]]


def parseInput(input):
    '''
    Cette fonction prend en entrée le résultat de la fonction 
    pytesseract.image_to_osd et retourne les points des bounding boxes 
    et le texte associé
    '''
    new_input = []
    for element in input:
        points = element[0]
        points = [tuple(x) for x in points]
        new_input.append((element[1][0], points))

    return new_input


def processInput(points, text, image):
    '''
    Cette fonction prend en entrée les points des bounding boxes 
    et le texte associé et retourne une image avec le texte dessus
    '''
    height = int(abs(points[2][1] - points[0][1]))
    #draw.polygon(points, fill=None, outline="blue")

    x1, y1 = points[0]
    x3, y3 = points[2]
    slope = (y3 - y1) / (x3 - x1)

    angle = math.degrees(math.atan(slope))
    fontSize = cv2.getFontScaleFromHeight(cv2.FONT_HERSHEY_SIMPLEX, height, 2)
    #font = PILasOPENCV.truetype("arial.ttf", size=int(fontsize))
    addRotatedText(image,
                   abs(int(angle)), (points[0][0], points[0][1]),
                   text,
                   "black",
                   fontSize=int(fontSize * 5))

    text_image = Image.new('RGB', image.size, (255, 255, 255))
    text_draw = ImageDraw.Draw(text_image)
    text_draw.text((points[0][0], points[0][1]),
                   "Your text here",
                   fill="black")

    text_image = text_image.rotate(angle,
                                   resample=Image.BICUBIC,
                                   expand=True,
                                   center=points[0])

    mask = Image.new('1', text_image.size, 1)
    draws = ImageDraw.Draw(mask)
    draws.rectangle([(0, 0), text_image.size], fill=0)

    image.paste(text_image, (0, 0), mask)


def addRotatedText(image, angle, xy, text, fill, fontSize):
    '''
    Appliquer la rotation sur le texte en le dessinant sur une image vide
    et après appliquer la rotation sur l'image et la mettre sur l'image originale
    ce qui est faite pour chaque bounding box detecté par le modèle
    '''
    width, height = image.size
    max_dim = max(width, height)

    mask_size = (max_dim * 2, max_dim * 2)
    mask = Image.new('L', mask_size, 0)

    draw = ImageDraw.Draw(mask)
    draw.text((max_dim, max_dim),
              text,
              255,
              font=ImageFont.truetype("arial.ttf", fontSize))
    if angle % 90 == 0:
        rotated_mask = mask.rotate(angle)
    else:
        bigger_mask = mask.resize((max_dim * 8, max_dim * 8),
                                  resample=Image.BICUBIC)
        rotated_mask = bigger_mask.rotate(angle).resize(mask_size,
                                                        resample=Image.LANCZOS)
    mask_xy = (max_dim - xy[0], max_dim - xy[1])
    b_box = mask_xy + (mask_xy[0] + width, mask_xy[1] + height)
    mask = rotated_mask.crop(b_box)
    color_image = Image.new('RGBA', image.size, fill)
    image.paste(color_image, mask)


def fit_text_width(text, height):
    font = ImageFont.truetype("arial.ttf", 20)
    font_size = 1
    text_length = font.getlength(text)
    bbox = font.getbbox(text)
    text_height = bbox[3] - bbox[1]
    #text_height = textbbox[3] - textbbox[1]
    while text_length < height:
        font_size += 1
        textbbox2 = font.getbbox(text)
        text_height = textbbox2[3] - textbbox2[1]

    fontsize = cv2.getFontScaleFromHeight(cv2.FONT_HERSHEY_SIMPLEX, height, 2)
    font_scale = 1
    text_size = cv2.getTextSize(text, font, font_scale, 2)[0]
    text_height = text_size[1]

    return font_size


def createNewImage(new_input, originalImageName):
    '''
    Cette fonction prend en entrée le résultat de la fonction parseInput
    et retourne une image avec le texte dessus
    '''
    originalImage = Image.open(originalImageName)
    width, height = originalImage.size
    image = Image.new('RGB', (width, height), (255, 255, 255))
    for element in new_input:
        points = element[1]
        text = element[0]
        processInput(points, text, image)
    image.save("result.png")


new_input = parseInput(input)
createNewImage(new_input, "IMG_2999.jpg")