import cv2
import matplotlib.pyplot as plt
from delimiter import Delimiter
from video import SpionRecord

VIDEO_PATH = 'cutted.mp4'
DELIMITER_PATH = 'frames/delimiters/old.png'

d = Delimiter(DELIMITER_PATH)
positions = []

with SpionRecord(VIDEO_PATH) as record:
    positions = record.get_delimiter_positions_ms()


cv2.destroyAllWindows()

