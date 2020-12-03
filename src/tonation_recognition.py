import enum

from music.tonation import Tonation


POINTS_SCALE_FIT = 10
POINTS_CADENCE = 200
POINTS_GREAT_AUTHENTIC_CADENCE = 80
POINTS_AUTHENTIC_CADENCE = 40
POINTS_PLAGAL_CADENCE = 40
POINTS_HALF_CADENCE = 20
POINTS_DECEPTIVE_CADENCE = 10
POINTS_TONIC_AT_THE_END = 50


class ChordType(enum.Enum):
    TONIC = 1
    SUBDOMINANT = 2
    DOMINANT = 3
    OTHER = 4


class TonationWithPoints:
    def __init__(self, tonation, points_from_scale,
                 points_from_chord_patterns,
                 points_from_tail):
        self.tonation = tonation
        self.points_from_scale = points_from_scale
        self.points_from_chord_patterns = points_from_chord_patterns
        self.points_from_tail = points_from_tail
        self.points = points_from_scale + \
            points_from_chord_patterns + \
            points_from_tail

    def __str__(self):
        return f"{self.tonation}\n"\
            f"points: {self.points}\n"\
            f"points_from_scale: {self.points_from_scale}\n"\
            f"points_from_chord_patterns: {self.points_from_chord_patterns}\n"\
            f"points_from_tail: {self.points_from_tail}"


def tonation_to_scale(key, kind):
    if kind == 'major':
        return [note % 12
                for note in
                [key, key+2, key+4, key+5, key+7, key+9, key+11]]
    return [note % 12
            for note in
            [key, key+2, key+3, key+5, key+7, key+8, key+10]]


def tonation_to_tonic(key, kind):
    if kind == 'major':
        return [note % 12 for note in [key, key+4, key+7]]
    return [note % 12 for note in [key, key+3, key+7]]


def tonation_to_subdominant(key, kind):
    if kind == 'major':
        return [note % 12 for note in [key+5, key+8, key]]
    return [note % 12 for note in [key+5, key+9, key]]


def tonation_to_dominant(key, kind):
    return [note % 12 for note in [key+7, key+11, key+2]]


def get_tonation(sounds):
    """Use list of Sounds to recognize a key
    used in the piece

    Parameters:
    sounds (list[Sound])

    Returns:
    (Tonation) : recognized key
    """
    tonations_and_points = []
    for kind in ['major', 'minor']:
        for base_key in range(12):
            scale = tonation_to_scale(base_key, kind)
            tonic = tonation_to_tonic(base_key, kind)
            subdominant = tonation_to_subdominant(base_key, kind)
            dominant = tonation_to_dominant(base_key, kind)
            chord_types = get_aligned_chord_types(
                sounds, tonic, subdominant, dominant)
            # chord_types = remove_solitary_chords(chord_types)
            chord_types = join_same_consecutive_chords(chord_types)
            points_from_scale = get_points_from_scale_fit(sounds, scale)
            points_from_chord_patterns = get_points_from_chord_patterns_fit(
                chord_types)
            points_from_tail = get_extra_points_for_tail(chord_types)
            tonation = Tonation(note=base_key, kind=kind)
            tonations_and_points.append(TonationWithPoints(
                tonation, points_from_scale,
                points_from_chord_patterns,
                points_from_tail
            ))
    tonations_and_points.sort(key=lambda x: x.points, reverse=True)
    # do we want to return best tonations, or chances with tonation candidates?
    return tonations_and_points[0].tonation


def get_aligned_chord_types(sounds, tonic, subdominant, dominant):
    # handles first-in-tonic = last-in-subdominant uncertainty
    tend_to_tonic = True
    chord_types = []
    for sound in sounds:
        chord_type = sound_to_chord_type(
            sound, tonic, subdominant, dominant, tend_to_tonic)
        tend_to_tonic = chord_type != ChordType.SUBDOMINANT
        chord_types.append(chord_type)
    return chord_types


def sound_to_chord_type(sound, tonic, subdominant, dominant, tend_to_tonic):
    if sound.note in dominant:
        return ChordType.DOMINANT
    if sound.note in tonic:
        if tend_to_tonic or sound.note not in subdominant:
            return ChordType.TONIC
        return ChordType.SUBDOMINANT
    if sound.note in subdominant:
        return ChordType.SUBDOMINANT
    return ChordType.OTHER


def remove_solitary_chords(chord_types):
    if len(chord_types) < 2:
        return chord_types
    result = []
    if chord_types[0] == chord_types[1]:
        result.append(chord_types[0])
    for i in range(1, len(chord_types)-1):
        chord = chord_types[i]
        if chord_types[i-1] == chord or chord == chord_types[i+1]:
            result.append(chord)
    if chord_types[-1] == chord_types[-2]:
        result.append(chord_types[-1])
    return result


def join_same_consecutive_chords(chord_types):
    if len(chord_types) < 2:
        return chord_types
    result = []
    last_chord = chord_types[0]
    result.append(last_chord)
    for chord in chord_types:
        if chord != last_chord:
            last_chord = chord
            result.append(chord)
    return result


def get_points_from_scale_fit(sounds, scale):
    points = 0
    for sound in sounds:
        if sound.note in scale:
            points += 10
    return points


class ChordSequencePattern:
    def __init__(self, sequence, points):
        self.sequence = sequence
        self.points = points


def get_points_from_chord_patterns_fit(chords):
    patterns = []
    patterns.append(ChordSequencePattern(
        [ChordType.TONIC, ChordType.SUBDOMINANT,
            ChordType.DOMINANT, ChordType.TONIC],
        POINTS_CADENCE
    ))
    patterns.append(ChordSequencePattern(
        [ChordType.SUBDOMINANT, ChordType.DOMINANT, ChordType.TONIC],
        POINTS_GREAT_AUTHENTIC_CADENCE
    ))
    patterns.append(ChordSequencePattern(
        [ChordType.TONIC, ChordType.DOMINANT, ChordType.TONIC],
        POINTS_AUTHENTIC_CADENCE
    ))
    patterns.append(ChordSequencePattern(
        [ChordType.TONIC, ChordType.SUBDOMINANT, ChordType.TONIC],
        POINTS_PLAGAL_CADENCE
    ))
    patterns.append(ChordSequencePattern(
        [ChordType.SUBDOMINANT, ChordType.DOMINANT],
        POINTS_HALF_CADENCE
    ))
    patterns.append(ChordSequencePattern(
        [ChordType.TONIC, ChordType.DOMINANT],
        POINTS_HALF_CADENCE
    ))
    # we don't use deceptive cadence, as it was not in the book
    points = 0
    for pattern in patterns:
        no_occurences = get_no_pattern_occurences(chords, pattern.sequence)
        points += no_occurences * pattern.points
    return points


def get_no_pattern_occurences(sequence, pattern):
    len_seq = len(sequence)
    len_pat = len(pattern)
    if len_seq < len_pat:
        return 0
    no_occurences = len_seq-len_pat+1
    for i in range(len_seq-len_pat+1):
        for j in range(len_pat):
            if pattern[j] != sequence[i+j]:
                no_occurences -= 1
                break
    return no_occurences


def get_extra_points_for_tail(chords):
    if chords[-1] == ChordType.TONIC:
        return POINTS_TONIC_AT_THE_END
    return 0
