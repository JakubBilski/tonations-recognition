import music


def change_tonation(sounds, diff):
    sounds1 = []
    for s in sounds:
        n1 = s.note+diff if s.note is not None else None
        s1 = music.Sound(n1, s.timestamp, s.duration_ms)
        sounds1.append(s1)

    return sounds1
