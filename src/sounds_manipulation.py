from . import music


def change_tonation(sounds, diff):
    """Transpose all sounds a chosen number
    of halftones up

    Parameters:
    sounds (list[Sound]) : Sounds to transpose
    diff (int) : Chosen number of halftones

    Returns:
    (list[Sound]) : Transposed sounds
    """
    sounds1 = []
    for s in sounds:
        n1 = s.note+diff if s.note is not None else None
        s1 = music.Sound(n1, s.timestamp, s.duration_ms)
        sounds1.append(s1)

    return sounds1
