import os
import this
from PIL import Image
import cv2
from matplotlib import pyplot as plt
import numpy as np
import pdb

file_name = ""


def main():
	add_image_process('drifbloomMissingCorner.jpeg')


def add_image_process(name):
	global file_name
	file_name = name
	img = cv2.imread(fr'flaskr\User_Files\{file_name}') #remove flaskr/ when running locally

	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	write_image_to_showcase(1, gray)#!#!

	blur = cv2.GaussianBlur(gray, (5, 5), 0)
	write_image_to_showcase(2, blur)

	#Thresh used for contours
	thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 205, 1)
	write_image_to_showcase(3, thresh)

	return find_largest_area(thresh, img)

def find_largest_area(thresh, originalImg):

	contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	#Saving to showcase
	drawn_image = originalImg.copy(); img_with_all_contours = cv2.drawContours(drawn_image, contours, -1, (0, 255, 0), 5); write_image_to_showcase("ImageWithAllContours", img_with_all_contours)

	filtered = []
	for c in contours:
		area = cv2.contourArea(c)
		if area > 10000:
			filtered.append(c)

	xArea = 0
	x = None
	for f in filtered:
		area = cv2.contourArea(f)
		if area > xArea:
			x = f
			xArea = area
	filtered = [x]

	#Saving to showcase
	drawn_image = originalImg.copy(); img_with_contour = cv2.drawContours(drawn_image, filtered[0], -1, (0, 255, 0), 5); write_image_to_showcase("ImageWithBigContour", img_with_contour)

	return crop_image_to_box(filtered, originalImg)

def crop_image_to_box(filtered, originalImg):
	# Could use .Canny() for cropping to edges
	rect = cv2.minAreaRect(filtered[0])
	box = cv2.boxPoints(rect)

	pts = order_points(box)

	cropped_to_card = four_point_transform(originalImg, pts)

	cv2.imwrite("../Output/FullImageCropped.png", cropped_to_card); write_image_to_showcase(4, cropped_to_card)

	full_crop_no_colour = extract_colour(cropped_to_card)

	cv2.imwrite(f"Processed_Files/{file_name}", full_crop_no_colour); write_image_to_showcase(5, full_crop_no_colour)

	img = cropped_to_card

	height = img.shape[0]
	width = img.shape[1]
	bottom_left_crop = img[height//2:, :width//2]
	cv2.imwrite("Processed_Files/QuarterCropped.png", bottom_left_crop); write_image_to_showcase(6, bottom_left_crop)

	bottom_left_crop_no_colour = extract_colour(bottom_left_crop)
	write_image_to_showcase(7, bottom_left_crop_no_colour)

	height = bottom_left_crop.shape[0]
	width = bottom_left_crop.shape[1]
	cropped_final = bottom_left_crop[height//2:, :width//2]
	cv2.imwrite("../Output/FinalZoom.png", cropped_final); write_image_to_showcase(8, cropped_final)

	cropped_final_no_colour = extract_colour(cropped_final)
	write_image_to_showcase(9, cropped_final_no_colour)

	imageArray = [cropped_final_no_colour, cropped_final, bottom_left_crop_no_colour, bottom_left_crop, full_crop_no_colour, cropped_to_card]

	return imageArray



def extract_colour(img):
	imgHLS = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)

	Lchannel = imgHLS[:, :, 1]

	mask = cv2.inRange(Lchannel, 0, 80)

	result = cv2.bitwise_not(mask)
	print("got here")
	# breakpoint()
	cv2.imwrite(f"Processed_Files/{file_name}", result)
	print("file name is: " +file_name)
	return result


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

def write_image_to_showcase(i, img):
    if not os.path.isdir('Showcase'):
        os.makedirs("Showcase")
    cv2.imwrite(f"Showcase/{i}.png", img)



if __name__ == '__main__':
	main()