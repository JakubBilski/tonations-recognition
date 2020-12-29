from .music.key import Key


POINTS_FOR_NOTE = 10
POINTS_FOR_BEGINING = 10
POINTS_FOR_END = 20


class KeyWithPoints:
    def __init__(self, key, points):
        self.key = key
        self.points = points

    def __str__(self):
        return f"{self.key}\n"\
            f"points: {self.points}\n"


def key_to_scale(key, kind):
    if kind == 'major':
        return [note % 12
                for note in
                [key, key+2, key+4, key+5, key+7, key+9, key+11]]
    return [note % 12
            for note in
            [key, key+2, key+3, key+5, key+7, key+8, key+11]]


def get_key(sounds):
    """Use list of Sounds to recognize a key
    used in the piece

    Parameters:
    sounds (list[Sound])

    Returns:
    (Key) : recognized key
    """
    keys_and_points = []
    for kind in ['major', 'minor']:
        for base_key in range(12):
            scale = key_to_scale(base_key, kind)
            points_from_scale = get_points_from_scale_fit(sounds, scale)
            key = Key(note=base_key, kind=kind)
            keys_and_points.append(KeyWithPoints(
                key, points_from_scale
            ))
    keys_and_points.sort(key=lambda x: x.points, reverse=True)
    return keys_and_points[0].key


def get_points_from_scale_fit(sounds, scale):
    points = 0
    for sound in sounds:
        if sound.note in scale:
            points += 10

    if sounds[0].note == scale[0]:
        points += 10
    if sounds[-1].note == scale[0]:
        points += 20

    return points
