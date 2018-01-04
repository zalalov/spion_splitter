import cv2
import subprocess
from os import path, mkdir
from delimiter import Delimiter
from common import generate_video_name
import pathlib


class SpionRecord:
    """
    Le Zap De Spion video handler (USE ONLY WITH CONTEXT MANAGER)
    """
    OUTPUT_DIR = './output/'
    CUT_DELTA = 0.3

    def __init__(self, video_path):
        """
        Constructor
        :param path:
        """
        self.path = video_path
        self.output_dir = None

    def __enter__(self):
        """
        Enter context manager function
        :return:
        """
        if not path.exists(self.path):
            raise Exception('Video not exists: {}'.format(self.path))

        self.set_output_dir(path.join(
            self.OUTPUT_DIR,
            path.basename(path.splitext(self.path)[0])
        ))

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

    def clean_ms(self, ms):
        """
        Get clean milliseconds
        :param ms: milliseconds in double
        :return: double num
        """
        if isinstance(ms, float):
            return round(ms, 2)

        return 0

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
        gen = generate_video_name()

        while True:
            ret, frame = self.cap.read()

            curr_msec = self.cap.get(cv2.CAP_PROP_POS_MSEC)

            if not ret:
                # TODO: handle finished clip
                break

            curr_is_del = delimiter.check(frame)

            if not prev_is_del:
                if curr_is_del:
                    period[1] = self.clean_ms(prev_msec)

                    if period[0] < period[1]:
                        filename = next(gen)

                        while path.exists(self.get_output_filepath(filename)):
                            filename = next(gen)

                        self.cut(period[0], period[1] - period[0], self.get_output_filepath(filename))
            else:
                if not curr_is_del:
                    period[0] = self.clean_ms(curr_msec)

            prev_msec = curr_msec
            prev_is_del = curr_is_del

        return timeline

    def set_output_dir(self, output_path):
        """
        Set output directory (create if not exists)
        :param output_path: string output path
        :return:
        """
        pathlib.Path(output_path).mkdir(parents=True, exist_ok=True)

        self.output_dir = output_path

    def get_output_filepath(self, filename):
        """
        Get output file path
        :param filename: filename
        :return: string full path to future file
        """
        return path.join(self.output_dir, filename)

    def cut(self, ms_start, duration, output_path):
        """
        Cut video
        :param ms_start: start position in ms
        :param duration: duration in seconds
        :param output_name: name of output file
        """
        cut_begin = (ms_start / 1000) + self.CUT_DELTA
        cut_end = (duration / 1000) - self.CUT_DELTA

        if cut_end < 0:
            return

        subprocess.call([
            'ffmpeg',
            '-i',
            self.path,
            '-ss',
            str(cut_begin),
            '-strict',
            '-2',
            '-t',
            str(cut_end),
            output_path
        ])
