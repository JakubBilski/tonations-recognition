NO_BARS_IN_ROW = 3

DURATION_TO_VEXTAB_DURATION = {
    1 : "32",
    2 : "16",
    3 : "16d",
    4 : "8",
    6 : "8d",
    8 : "4",
    12 : "4d",
    16 : "2",
    24 : "2d",
    32 : "1"
}

def generate_vextab_notes(sounds, tonation, metrum):
    key = tonation.symbol
    if tonation.kind == 'minor':
        key = key + 'm'
    result = []
    notes_vextab = ""
    bar_duration = metrum[0]*metrum[1]
    duration_from_start = 0
    no_bars_from_start = 0
    for sound in sounds:
        if sound.symbol == "r":
            notes_vextab += "## "
        else:
            notes_vextab += ":"
            notes_vextab += DURATION_TO_VEXTAB_DURATION[sound.duration]
            notes_vextab += " "
            notes_vextab += sound.symbol
            notes_vextab += "/4 "
        duration_from_start += sound.duration
        if duration_from_start >= bar_duration:
            notes_vextab += "| "
            duration_from_start -= bar_duration
            no_bars_from_start += 1
            if no_bars_from_start >= NO_BARS_IN_ROW:
                result.append(notes_vextab);
                notes_vextab = ""
                no_bars_from_start = 0
    return result;
    
def generate_vextab_key(tonation):
    key = tonation.symbol
    if tonation.kind == 'minor':
        key = key + 'm'
    return key

def generate_vextab_metrum(metrum):   
    metrum_transform = {
        16 : 2,
        8 : 4,
        4 : 8,
        2 : 16
    }
    return str(metrum[0]) + "/" + str(metrum_transform[metrum[1]])
