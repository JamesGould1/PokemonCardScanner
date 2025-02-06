import pytesseract
from PIL import Image
import cv2

file_name = ""

def main(file_path):
    img = cv2.imread(file_path)
    return load_image(img)

def load_image(img):
    image_cv = img
    #cv2.imread(fr'C:\Users\James.Goulding\PycharmProjects\PokemonProject\flaskr\{name}'))
    return process_image(image_cv)

def process_image(image_cv):
    if len(image_cv.shape) != 2:
        gray_image = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)
    else:
        gray_image = image_cv
    cv2.imwrite('../Output/gray_image.png', gray_image) ####
    th2 = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    cv2.imwrite('../Output/attempt.png', th2) ####
    return scan_image(th2)

def scan_image(processed_image):
    custom_config = r'--psm 12 --oem 3 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyz/1234567890'
    textOnCard = pytesseract.image_to_string(processed_image, config=custom_config)
    print(textOnCard)
    return textOnCard

if __name__ == '__main__':
    main()