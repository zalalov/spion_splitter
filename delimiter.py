import cv2
from os import path
from hist import get_hist_corr


class Delimiter:
    # Delimiter check threshold
    THRESHOLD = 0.05

    def __init__(self, delimiter_image_path):
        """
        Constructor
        :param path:
        """
        if not path.exists(delimiter_image_path):
            raise Exception('Image not exists: {}'.format(delimiter_image_path))

        self.image = cv2.imread(delimiter_image_path)

    def adjust_size(self, size):
        """
        Adjust delimiter size
        :param size: future size
        :return:
        """
        if not isinstance(size, (tuple, list)) and len(size) != 2:
            raise Exception('Invalid size param.')

        self.image = cv2.resize(self.image, size)

    def check(self, image):
        """
        Check if image is a delimiter frame
        :param image: image to compare
        :return: true/false if image is a delimiter
        """
        return get_hist_corr(self.image, image) >= self.THRESHOLD
