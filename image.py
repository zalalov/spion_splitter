import cv2


def get_hist_corr(a, b):
    """
    Get
    :param a: first image
    :param b: second image
    :return: histogram's correlation coefficient
    """
    a_hist = cv2.calcHist([a], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
    b_hist = cv2.calcHist([b], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])

    return cv2.compareHist(a_hist, b_hist, cv2.HISTCMP_CORREL)

