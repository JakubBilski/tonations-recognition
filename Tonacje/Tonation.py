from BitwiseRotation import rol

class MajorTonation():
    def __init__(self, key):
        self.key = key
        self.keyLog2 = valToLog2Map[key]
        self.scale = rol(2741, self.keyLog2, 12)
        self.tonic = MajorCord(self.keyLog2)
        self.subdominant = MajorCord(self.keyLog2 + 5)
        self.dominant = MajorCord(self.keyLog2 + 7)
        
class MinorTonation():
    def __init__(self, key):
        self.key = key
        self.keyLog2 = valToLog2Map[key]
        self.scale = rol(1453, self.keyLog2, 12)
        self.tonic = MinorCord(self.keyLog2)
        self.subdominant = MinorCord(self.keyLog2 + 5)
        self.dominant = MajorCord(self.keyLog2 + 7) 
    
class TonationFactory:
    def GetTonation(self, keySemitone, isMajor):
        if isMajor:
            return MajorTonation(keySemitone)
        return MinorTonation(keySemitone)

    def GetAllTonations(self):
        return [MajorTonation(key) for key in allKeys] + [MinorTonation(key) for key in allKeys]



def MajorCord(root):
    return rol(145, root, 12)

def MinorCord(root):
    return rol(137, root, 12)

valToLog2Map = {
    1 : 0,
    2 : 1,
    4 : 2,
    8 : 3,
    16 : 4,
    32 : 5,
    64 : 6,
    128 : 7,
    256 : 8,
    512 : 9,
    1024 : 10,
    2048 : 11,
}

allKeys = valToLog2Map.keys()