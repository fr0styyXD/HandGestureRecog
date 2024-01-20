import numpy as np
import cv2
import keras
import tensorflow as tf
from string import ascii_uppercase
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        tf.config.experimental.set_virtual_device_configuration(gpus[0], [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=2048)])
    except RuntimeError as e:
        print(e)

model = keras.models.load_model(r"C:\Users\HP\Desktop\CPP\New\transferlearning2.h5")

cam = cv2.VideoCapture(1)

alpha_dict = {}
j=0
for i in ascii_uppercase:
   alpha_dict[j] = i
   j = j + 1


while True:
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    cv2.rectangle(frame, (319, 9), (620 + 1, 309), (0, 255, 0), 1)
    roi = frame[10:300, 320:620]

    # cv2.imshow("Frame", frame)
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    gaussblur = cv2.GaussianBlur(gray, (5, 5), 2)
    smallthres = cv2.adaptiveThreshold(gaussblur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 9, 2.8)
    ret, final_image = cv2.threshold(smallthres, 70, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    cv2.imshow("BW", final_image)
    final_image = cv2.resize(final_image, (600, 600))

    final_image = np.reshape(final_image, (3, 200, 200, 3))
    pred = model.predict(final_image)
    # print(alpha_dict[np.argmax(pred)])
    cv2.putText(frame,alpha_dict[np.argmax(pred)], (10, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1)
    cv2.imshow("Frame", frame)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cam.release()
cv2.destroyAllWindows()