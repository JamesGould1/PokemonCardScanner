from PIL import Image
import cv2
from matplotlib import pyplot as plt
import numpy as np

img_path = r'C:\Users\James.Goulding\PycharmProjects\PokemonProject\Resources\blitzle.jpeg'
img = cv2.imread(img_path)

def main():
    if img is None:
        print('No image found at', img_path)
    else:
        add_image_process(img)

        ##Perhaps use .Canny() for cropping to edges
        img2 = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        print("Image shape:", img2.shape)
        print("Image dtype:", img2.dtype)
        img2 = img2.astype(np.uint8)
        edges = cv2.Canny(img2, 100, 200, 3)
        plt.subplot(122), plt.imshow(edges, cmap='gray')
        plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

        plt.show()

def add_image_process(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (7, 7), 0)

    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 205, 1)
    find_largest_area(thresh)

def find_largest_area(thresh):

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    filtered = []
    for c in contours:
        area = cv2.contourArea(c)
        print(f"Contour area: {area}")
        if area > 10000:
            filtered.append(c)
    xArea = 0
    x = None
    for f in filtered:
        area = cv2.contourArea(f)
        if area > xArea:
            x = f
            print(f"Old largest area: {xArea}")
            xArea = area
            print(f"New largest contour with area: {xArea}")
    filtered = [x]
    crop_image_to_box(filtered)

def crop_image_to_box(filtered):
    print(f"{filtered[0]}")
    rect = cv2.minAreaRect(filtered[0])
    box = cv2.boxPoints(rect)
    print(f"{rect[0]}")
    print(f"{box}")
    pts = order_points(box)
    wrapped_img = four_point_transform(cv2.imread(img_path), pts)
    plt.imshow(wrapped_img)
    # Load the image
    cv2.imwrite("Output/FullImageCropped.png", wrapped_img)
    extract_colour(wrapped_img, 1)
    img = wrapped_img
    # Calculate midpoints
    height = img.shape[0]
    width = img.shape[1]
    bottom_left_corner = img[height//2:, :width//2]
    cv2.imwrite("Output/QuarterCropped.png", bottom_left_corner)
    extract_colour(bottom_left_corner, 2)


def extract_colour(img, i):
    imgHLS = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)

    Lchannel = imgHLS[:, :, 1]

    mask = cv2.inRange(Lchannel, 0, 50)

    result = cv2.bitwise_not(mask)

    cv2.imwrite(f"Output/outTTTTput{i}.png", result)


def order_points(pts):
	# initialzie a list of coordinates that will be ordered
	# such that the first entry in the list is the top-left,
	# the second entry is the top-right, the third is the
	# bottom-right, and the fourth is the bottom-left
	rect = np.zeros((4, 2), dtype = "float32")
	# the top-left point will have the smallest sum, whereas
	# the bottom-right point will have the largest sum
	s = pts.sum(axis = 1)
	rect[0] = pts[np.argmin(s)]
	rect[2] = pts[np.argmax(s)]
	# now, compute the difference between the points, the
	# top-right point will have the smallest difference,
	# whereas the bottom-left will have the largest difference
	diff = np.diff(pts, axis = 1)
	rect[1] = pts[np.argmin(diff)]
	rect[3] = pts[np.argmax(diff)]
	# return the ordered coordinates
	return rect

def four_point_transform(image, pts):
	# obtain a consistent order of the points and unpack them
	# individually
	rect = order_points(pts)
	(tl, tr, br, bl) = rect
	# compute the width of the new image, which will be the
	# maximum distance between bottom-right and bottom-left
	# x-coordiates or the top-right and top-left x-coordinates
	widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
	widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
	maxWidth = max(int(widthA), int(widthB))
	# compute the height of the new image, which will be the
	# maximum distance between the top-right and bottom-right
	# y-coordinates or the top-left and bottom-left y-coordinates
	heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
	heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
	maxHeight = max(int(heightA), int(heightB))
	# now that we have the dimensions of the new image, construct
	# the set of destination points to obtain a "birds eye view",
	# (i.e. top-down view) of the image, again specifying points
	# in the top-left, top-right, bottom-right, and bottom-left
	# order
	dst = np.array([
		[0, 0],
		[maxWidth - 1, 0],
		[maxWidth - 1, maxHeight - 1],
		[0, maxHeight - 1]], dtype = "float32")
	# compute the perspective transform matrix and then apply it
	M = cv2.getPerspectiveTransform(rect, dst)
	warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
	# return the warped image
	return warped

if __name__ == '__main__':
    main()