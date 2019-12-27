import cv2
# import numpy as np
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
print(ret)
cv2.imwrite('/Users/mirako/opencv_study/write.jpg', frame)
