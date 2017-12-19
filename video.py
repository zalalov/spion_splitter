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
        if not path.exists(self.path):
            raise Exception('Video not exists: {}'.format(self.path))

        self.cap = cv2.VideoCapture(self.path)

        return self

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

        skip = False
        prev_msec = 0
        curr_msec = 0
        timeline = []
        prev_is_del = False
        curr_is_del = False
        period = [0, 0]

        while True:
            ret, frame = self.cap.read()

            if not ret:
                break

            curr_msec = self.cap.get(cv2.CAP_PROP_POS_MSEC)
            curr_is_del = delimiter.check(frame)

            if not prev_is_del and not curr_is_del:
                continue

            # delimiter started
            if not prev_is_del and curr_is_del:
                period[1] = prev_msec

                if period[0] < period[1]:
                    timeline.append(period)

                    print(timeline)

            # delimiter ended
            if prev_is_del and not curr_is_del:
                period[0] = curr_msec

            print(period)

            # debug
            cv2.imshow('frame', frame)
            cv2.waitKey(10)

            prev_msec = curr_msec
            prev_is_del = curr_is_del

        return timeline
