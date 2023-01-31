from paddleocr import PaddleOCR,draw_ocr
from PIL import ImageFont,ImageDraw,Image,ImageOps
import math
import difflib
from annotate import add_annotations
import cv2
from termcolor import colored
import time
'''#in case we need it 
import nltk
nltk.download()
'''

from nltk.corpus import words
word_list = words.words()


IMG_PATH = r"C:\Users\Yann\OneDrive\Bureau\cours\m2\devLogic\test\ppocr_img\ppocr_img\imgs_en\test3.jpg"


def get_final_word(word):
    res = difflib.get_close_matches(word, word_list)
    duplicate = find_duplicate(res)
    #print(res)
    if(res == []):
        return word
    elif(duplicate != None ):
        return duplicate
    return res[0]

def find_duplicate(strings):
    duplicate = None
    frequency = {}
    for string in strings:
        if string in frequency:
            frequency[string] += 1
            duplicate = string
        else:
            frequency[string] = 1
    return duplicate

def splitAndProcess(line):
    #print(line)
    res = ""
    for word in line[0].split():
        res += get_final_word(word)
        res += " "
    return res if line[1]<0.95 else line[0]





# Paddleocr supports Chinese, English, French, German, Korean and Japanese.
# You can set the parameter `lang` as `ch`, `en`, `fr`, `german`, `korean`, `japan`
# to switch the language model in order.
timer = time.time()
ocr = ocr = PaddleOCR(  
    cls_model_dir=r'C:\Users\Yann\Downloads\ch_ppocr_mobile_v2.0_cls_infer',
    rec_model_dir=r'C:\Users\Yann\Downloads\en_PP-OCRv3_rec_infer',
    det_model_dir=r'C:\Users\Yann\Downloads\en_PP-OCRv3_det_infer',
    use_angle_cls=True, lang='en')
result = ocr.ocr(IMG_PATH, cls=True)
for idx in range(len(result)):
    res = result[idx]
    print(colored("delay : "+str(time.time()-timer)+"s",'blue'))
    for item in res:
        print (colored(item, 'red'))
        item[1] = (splitAndProcess(item[1]),item[1][1] )
        print (colored(" ---> "+ item [1][0] , 'green'))
    img = cv2.imread(IMG_PATH)
    add_annotations(img,res)
    cv2.imwrite("img.png", img)

# draw result

result = result[0]
image = Image.open(IMG_PATH).convert('RGB')
boxes = [line[0] for line in result]
txts = [line[1][0] for line in result]
scores = [line[1][1] for line in result]
im_show = draw_ocr(image, boxes, txts, scores, font_path=r'./simfang.ttf')
im_show = Image.fromarray(im_show)
im_show.save('result.jpg')


