# guitar chords levels
L1 = 0
L2 = 1
L3 = 2
L4 = 3
L5 = 4
L6 = 5

CHORDS_SCORING_MINOR = {
    0: L2,  # c
    1: L5,  # cis
    2: L2,  # d
    3: L5,  # dis
    4: L1,  # e
    5: L3,  # f
    6: L5,  # fis
    7: L2,  # g
    8: L5,  # gis
    9: L1,  # a
    10: L5,  # ais
    11: L2  # b
}

CHORDS_SCORING_MAJOR = {
    0: L2,  # c
    1: L5,  # cis
    2: L2,  # d
    3: L5,  # dis
    4: L1,  # e
    5: L3,  # f
    6: L5,  # fis
    7: L2,  # g
    8: L5,  # gis
    9: L1,  # a
    10: L5,  # ais
    11: L2  # b
}


def simplify(notes, chords, key):
    """Transpose all piece information to a key
    in which the chords would be easier to play
    on a guitar

    Parameters:
    notes (list[Sound])
    chords (list[Chord])
    key (Key)

    Returns:
    (list[Sound]) : Notes after transposition
    (list[Chord]) : Chords after transposition
    (Key) : Chosen easier key
    """
    min_score = 1000000
    min_trans = 0
    min_note = min([x.note+x.octave*12 for x in notes if x.note])
    max_note = max([x.note+x.octave*12 for x in notes if x.note])
    # lowest note that can be played on a guitar is E2, which is _note=16
    min_trans = max([-6, 16-min_note])
    # highest note that can be played on a guitar is E4, which is _note=40
    max_trans = min([6, 40-max_note])

    for i in range(min_trans, max_trans+1):
        score = 0
        for c in chords:
            if 'major' in c.kind:
                score += CHORDS_SCORING_MAJOR[(c.note + i) % 12]
            elif 'minor' in c.kind:
                score += CHORDS_SCORING_MINOR[(c.note + i) % 12]
        if score < min_score:
            min_score = score
            min_trans = i
    key.note = (key.note + min_trans) % 12
    for i in range(len(notes)):
        if notes[i].note is not None:
            notes[i].note = notes[i].note + notes[i].octave * 12 + min_trans
    for i in range(len(chords)):
        chords[i].note = chords[i].note + min_trans
    return notes, chords, key
