import cv2

# Load image

image = cv2.imread('Resources/dribloom.jpg')

# Convert to grayscale

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#Add Blur
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

#Detect Edges
edges = cv2.Canny(blurred, 50, 150)

contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for contour in contours:
    arc_length = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.02 * arc_length, True)
# If the approximated contour has 4 points, we can consider it a rectangle
if len(approx) == 4:
    cv2.drawContours(image, [approx], -1, (0, 255, 0), 3)

cv2.imshow('Detected Rectangles', image)

cv2.waitKey(0)

cv2.destroyAllWindows()
