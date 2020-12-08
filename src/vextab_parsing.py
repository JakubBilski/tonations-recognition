from .utils import constants
from .music.chord import Chord


NO_BARS_IN_ROW = 3

DURATION_TO_VEXTAB_DURATION = {
    1: "32",
    2: "16",
    3: "16d",
    4: "8",
    6: "8d",
    8: "4",
    12: "4d",
    16: "2",
    24: "2d",
    32: "1"
}

STRINGS = {
    6: (constants.REVERSE_SYMBOLS["E"], 2),
    5: (constants.REVERSE_SYMBOLS["A"], 2),
    4: (constants.REVERSE_SYMBOLS["D"], 3),
    3: (constants.REVERSE_SYMBOLS["G"], 3),
    2: (constants.REVERSE_SYMBOLS["B"], 3),
    1: (constants.REVERSE_SYMBOLS["E"], 4)
}
# print(STRINGS)


def sound_to_string(sound):
    # return f"{sound.symbol}/4"
    sound.height = 3
    i = 6
    while i > 1 and (STRINGS[i-1][1] < sound.height or
                     (STRINGS[i-1][1] == sound.height and
                      STRINGS[i-1][0] < sound.note)):
        i -= 1
    fret = (STRINGS[i][1] - sound.height)*12 + STRINGS[i][0] - sound.note
    return f"{fret}/{i}"


def chord_to_string(chord):
    if chord.kind == "major":
        return f"{chord.symbol} "
    elif chord.kind == "major7":
        return f"{chord.symbol}7"
    elif chord.kind == "diminished":
        return f"{chord.symbol}dim"
    else:
        return f"{chord.symbol}m"


def decompose_chord(chord):
    result = []
    duration = chord.duration
    legal_durations = DURATION_TO_VEXTAB_DURATION.keys()
    legal_durations = sorted(legal_durations, reverse=True)
    while(duration > 0):
        max_fit = [ld for ld in legal_durations if ld <= duration][0]
        new_chord = Chord(chord.note, chord.symbol, max_fit, chord.kind)
        result.append(new_chord)
        duration -= max_fit
    return result


def generate_vextab_notes(sounds, metrum_upper, metrum_lower):
    """Use information about the piece
    to create notes in an input format
    suitable for the vextab javascript library
    http://vexflow.com/vextab/

    Returns:
    (list[str]) : List of strings with music information
        for the consecutive lines of music notation
    """
    result = []
    notes_vextab = ""
    bar_duration = metrum_upper*metrum_lower
    duration_from_start = 0
    no_bars_from_start = 0
    for sound in sounds:
        if sound.symbol == "r":
            notes_vextab += "## "
        else:
            notes_vextab += ":"
            notes_vextab += DURATION_TO_VEXTAB_DURATION[sound.duration]
            notes_vextab += " "
            notes_vextab += sound_to_string(sound)
            notes_vextab += " "
        duration_from_start += sound.duration
        if duration_from_start >= bar_duration:
            notes_vextab += "| "
            duration_from_start -= bar_duration
            no_bars_from_start += 1
            if no_bars_from_start >= NO_BARS_IN_ROW:
                result.append(notes_vextab)
                notes_vextab = ""
                no_bars_from_start = 0
    return result


def generate_vextab_chords(chords, metrum_upper, metrum_lower):
    """Use information about the piece
    to create chords information in an input format
    suitable for the vextab javascript library
    http://vexflow.com/vextab/

    Returns:
    (list[str]) : List of strings with chords information
        for the consecutive lines of music notation
    """
    result = []
    chords_vextab = ""
    bar_duration = metrum_upper*metrum_lower
    duration_from_start = 0
    no_bars_from_start = 0
    cleared_chords = [dc for chord in chords for dc in decompose_chord(chord)]
    prev_chord = None
    chords_vextab += ".1"

    for chord in cleared_chords:
        chords_vextab += ",:"
        chords_vextab += DURATION_TO_VEXTAB_DURATION[chord.duration]
        chords_vextab += ","
        if chord_to_string(chord) == prev_chord:
            chords_vextab += " "
        else:
            chords_vextab += chord_to_string(chord)
            prev_chord = chord_to_string(chord)
        duration_from_start += chord.duration
        if duration_from_start >= bar_duration:
            chords_vextab += ",|"
            duration_from_start -= bar_duration
            no_bars_from_start += 1
            if no_bars_from_start >= NO_BARS_IN_ROW:
                result.append(chords_vextab)
                chords_vextab = ".1"
                no_bars_from_start = 0
    return result


def generate_vextab_key(key):
    """Use information about the piece
    to create key information in an input format
    suitable for the vextab javascript library
    http://vexflow.com/vextab/

    Returns:
    (str)
    """
    key_vextab = key.symbol
    if key_vextab == 'D#':
        key_vextab = 'Eb'
    if key.kind == 'minor':
        key_vextab = key_vextab + 'm'
    return key_vextab


def generate_vextab_metrum(metrum_upper, metrum_lower):
    """Use information about the piece
    to create metrum information in an input format
    suitable for the vextab javascript library
    http://vexflow.com/vextab/

    Returns:
    (str)
    """
    metrum_transform = {
        16: 2,
        8: 4,
        4: 8,
        2: 16
    }
    return str(metrum_upper) + "/" + str(metrum_transform[metrum_lower])


def generate_vextab_chord_types(chords):
    """Use information about the piece
    to create information about all
    chords used in the piece
    in an input format
    suitable for the vextab javascript library
    http://vexflow.com/vextab/

    Returns:
    (list[str])
    """
    chord_types = []
    for chord in chords:
        if chord.kind == "major":
            chord_types.append(f"{chord.symbol}Maj")
        elif chord.kind == "major7":
            chord_types.append(f"{chord.symbol}7")
        elif chord.kind == "diminished":
            chord_types.append(f"{chord.symbol}dim")
        else:
            chord_types.append(f"{chord.symbol}m")
    return chord_types
