import cv2
from ultralytics import YOLO

model = YOLO("yolov8m.pt")
img = "Assignment 2_image.jpg"

result = model(img, conf=0.5, verbose=False)[0]
annotated_frame = result.plot()

#save img 
cv2.imwrite("HW2_3-1_1_result.jpg", annotated_frame)