def counter():
    i = 0

    while True:
        yield i
        i += 1


def generate_video_name():
    c = counter()

    while True:
        yield '{}.mp4'.format(str(next(c)))
