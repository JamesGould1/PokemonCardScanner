from PIL import Image
import imagehash
import glob
import matplotlib.pyplot as plt
import cv2
import pandas as pd

# Set image path
image_path = 'fuecocoOnline.jpg'
# Read our image
read_image = Image.open(image_path)
# Generate image hash value
hash_value = imagehash.average_hash(read_image)
# print image hash value
print(hash_value)

dataset_path = "./data_subset/"

#f1c1e5c1f9fcc000
#81e1e3c783838181

#ffbffffefc0060f0
#f884c4fdfff9e0c0
#d81444d1ffff7f00