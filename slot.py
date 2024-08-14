import cv2
import csv

def drawRectangle(image, a, b, c, d, low_threshold, high_threshold, min_pix, max_pix):
    sub_image = image[b:b + d, a:a + c]
    edges = cv2.Canny(sub_image, low_threshold, high_threshold)
    pix = cv2.countNonZero(edges)
    if min_pix <= pix <= max_pix:
        cv2.rectangle(image, (a, b), (a + c, b + d), (0, 255, 0), 3)
        Spots.location += 1
    else:
        cv2.rectangle(image, (a, b), (a + c, b + d), (0, 0, 255), 3)

def callback(foo):
    pass

class Spots:
    location = 0

video = cv2.VideoCapture('lot.mp4')
if not video.isOpened():
    print("Error: Could not open video.")
    exit()

source, image = video.read()
if not source:
    print("Error: Could not read video.")
    video.release()
    exit()

# Resize the image
height, width, layers = image.shape
image = cv2.resize(image, (int(width * 0.35), int(height * 0.35)))

# ROI Selection and saving to CSV
r = cv2.selectROI('Selector', image, showCrosshair=False, fromCenter=False)
rlist = list(r)
cv2.destroyAllWindows()

with open('rois1.csv', 'a', newline='') as outf:
    csvw = csv.writer(outf)
    csvw.writerow(rlist)

# Load ROI data
roi_data = []
with open('rois1.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        roi_data.append([int(r) for r in row])

cv2.namedWindow('parameters')
cv2.createTrackbar('Threshold1', 'parameters', 186, 700, callback)
cv2.createTrackbar('Threshold2', 'parameters', 122, 700, callback)
cv2.createTrackbar('Min pixels', 'parameters', 100, 1500, callback)
cv2.createTrackbar('Max pixels', 'parameters', 534, 1500, callback)

while video.isOpened():
    Spots.location = 0
    ret, image = video.read()
    
    if not ret:
        break
        
    image = cv2.resize(image, (int(width * 0.35), int(height * 0.35)))
    min_pix = cv2.getTrackbarPos('Min pixels', 'parameters')
    max_pix = cv2.getTrackbarPos('Max pixels', 'parameters')
    low_threshold = cv2.getTrackbarPos('Threshold1', 'parameters')
    high_threshold = cv2.getTrackbarPos('Threshold2', 'parameters')

    for a, b, c, d in roi_data:
        drawRectangle(image, a, b, c, d, low_threshold, high_threshold, min_pix, max_pix) 

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(image, 'Available Spots: ' + str(Spots.location),
                (10, 30), font, 1, (0, 255, 0), 3)
    cv2.imshow('Frame', image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()