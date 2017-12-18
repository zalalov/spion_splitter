import cv2
from image import get_hist_corr
import matplotlib.pyplot as plt
from time import sleep
from sklearn import compare_ssim


VIDEO_PATH = 'cutted.mp4'
DELIMITER_PATH = 'frames/delimiters/old.png'

cap = cv2.VideoCapture(VIDEO_PATH)
cap_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
cap_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

# get video frame sizes
SIZE_TO_COMPARE = (int(cap_width), int(cap_height))

delimiter = cv2.imread(DELIMITER_PATH, cv2.COLOR_BGR2GRAY)
delimiter = cv2.resize(delimiter, SIZE_TO_COMPARE)

corrs = list()

while True:
    ret, frame = cap.read()

    if not ret:
        break

    image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # corrs.append(get_hist_corr(delimiter, image))

    score, diff = compare_ssim(delimiter, image, full=True)

    print(score)
    sleep(1)

# plt.plot(corrs)
# plt.show()

cap.release()
cv2.destroyAllWindows()

