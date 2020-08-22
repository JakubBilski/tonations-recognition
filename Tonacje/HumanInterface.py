import Tonation

# it is constant
valToNoteMap = {
    1 : "C",
    2 : "C#",
    4 : "D",
    8 : "D#",
    16 : "E",
    32 : "F",
    64 : "F#",
    128 : "G",
    256 : "G#",
    512 : "A",
    1024 : "A#",
    2048 : "H",
    }
# easier:
# notes = ["C", "C#", ..., "H"]
# valToNoteMap = {1<<i: note for i, note in enumerate(notes)}
# it is also easier because reader knows why are you using powers of 2

# it is constant
noteToValMap = {
    "C" : 1,
    "C#" : 2,
    "D" : 4,
    "D#" : 8,
    "E" : 16,
    "F" : 32,
    "F#" : 64,
    "G" : 128,
    "G#" : 256,
    "A" : 512,
    "A#" : 1024,
    "H" : 2048,
    "CIS" : 2,
    "DIS" : 8,
    "EIS" : 32,
    "FIS" : 64,
    "GIS" : 256,
    "AIS" : 1024,
    "HIS" : 1,
    "DES" : 2,
    "ES" : 8,
    "FES" : 32,
    "GES" : 64,
    "AS" : 256,
    "B" : 1024  
    }

def GetAllNotesInMaskAsString(mask):
    val = 1
    result = ""
    for x in range(12):
    # for _ in range(12):
    # use "_" sign if you want to discard result
        if val & mask:
            result += valToNoteMap[val] + " ";
        val = val << 1
    return result

def TonationToString(tonation):
    # better:
    # method __str__(self) in class MajorTonation and MinorTonation
    # then you could just use:
    # str(tonation)
    if isinstance(tonation, Tonation.MajorTonation):
        return valToNoteMap[tonation.key] + "-dur"
    if isinstance(tonation, Tonation.MinorTonation):
        return valToNoteMap[tonation.key] + "-mol"
    else:
        raise Exception("Oj nie nie")