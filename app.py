import cv2
from delimiter import Delimiter
from video import SpionRecord

VIDEO_PATH = 'cutted.mp4'
DELIMITER_PATH = 'frames/delimiters/old.png'

d = Delimiter(DELIMITER_PATH)
timeline = []

with SpionRecord(VIDEO_PATH) as record:
    timeline = record.get_delimiter_positions_ms(d)


cv2.destroyAllWindows()

