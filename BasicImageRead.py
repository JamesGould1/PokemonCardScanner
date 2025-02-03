import pytesseract
from PIL import Image
import cv2

image_cv = cv2.imread('Resources/dribloom.jpg')

x, y, w, h = 787, 3050, 300, 200

cropped_image = image_cv[y:3050+200, x:787+300]
cv2.imwrite('Output/cropped_image.png', cropped_image)

gray_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
cv2.imwrite('Output/gray_image.png', gray_image)

th2 = cv2.adaptiveThreshold(gray_image,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,2)
cv2.imwrite('Output/attempt.png', th2)

# Remove 1 from filter, than you will get I instead (I filter for numbers only)
custom_config = r'--psm 6 --oem 3 -c tessedit_char_whitelist=-.0123456789'


# Convert the processed OpenCV image back to a PIL image
processed_image = Image.fromarray(th2)

tex = pytesseract.image_to_string(cropped_image, config=custom_config)
print(tex)

extracted_text = pytesseract.image_to_string(gray_image)

print(extracted_text)

