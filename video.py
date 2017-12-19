import cv2
from os import path
from delimiter import Delimiter


class SpionRecord:
    """
    Le Zap De Spion video handler (USE ONLY WITH CONTEXT MANAGER)
    """
    def __init__(self, video_path):
        """
        Constructor
        :param path:
        """
        self.path = video_path

    def __enter__(self):
        """
        Enter context manager function
        :return:
        """
        if not path.exists(self.video_path):
            raise Exception('Video not exists: {}'.format(self.video_path))

        self.cap = cv2.VideoCapture(self.video_path)

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit context manager function
        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return:
        """
        self.cap.release()

    def shape(self):
        """
        Get Video shape
        :return:
        """
        return int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    def get_delimiter_positions_ms(self, delimiter):
        """
        Get delimiter positions in milliseconds
        :param delimiter:
        :return:
        """
        if not isinstance(delimiter, Delimiter):
            raise Exception('Invalid delimiter param.')

        delimiter.adjust_size(self.shape())

        # TODO: return lists of milliseconds
        # while True:
        #     ret, frame = self.cap.read()
        #
        #     print(self.cap.get(cv2.CAP_PROP_POS_MSEC))
        #
        #     if not ret:
        #         break

        return []
