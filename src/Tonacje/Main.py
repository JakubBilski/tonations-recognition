import Tonation
import HumanInterface

def main():
    inp = ""
    while inp != "exit":
        inp = input("\nCo chcesz wiedziec? (np.'a-dur', 'C#', 'des')\n")
        if(inp.find("-") != -1):
            key = HumanInterface.noteToValMap[inp[:inp.find("-")].upper()]
            if inp[-3:] == "mol" or inp[-3:] == "MOL":
                displayTonationInfo(key, False)
            elif inp[-3:] == "dur" or inp[-3:] == "DUR":
                displayTonationInfo(key, True)
        elif inp.upper() in HumanInterface.noteToValMap.keys():
            note = HumanInterface.noteToValMap[inp.upper()]
            DisplayNoteInfo(note)


def displayTonationInfo(key, isMajor):
    factory = Tonation.TonationFactory()
    tonation = factory.GetTonation(key, isMajor)
    print("Gama: " + HumanInterface.GetAllNotesInMaskAsString(tonation.scale))
    print("Tonika: " + HumanInterface.GetAllNotesInMaskAsString(tonation.tonic))
    print("Subdominanta: " + HumanInterface.GetAllNotesInMaskAsString(tonation.subdominant))
    print("Dominanta: " + HumanInterface.GetAllNotesInMaskAsString(tonation.dominant))

def DisplayNoteInfo(note):
    factory = Tonation.TonationFactory()
    tonations = factory.GetAllTonations()
    print("W gamach: ")
    for tonation in tonations:
        if tonation.scale & note:
            print("\t" + HumanInterface.TonationToString(tonation) + " (" + HumanInterface.GetAllNotesInMaskAsString(tonation.scale) + ")")
    print("W tonikach: ")
    for tonation in tonations:
        if tonation.tonic & note:
            print("\t" + HumanInterface.TonationToString(tonation) + " (" + HumanInterface.GetAllNotesInMaskAsString(tonation.tonic) + ")")
    print("W subdominantach: ")
    for tonation in tonations:
        if tonation.subdominant & note:
            print("\t" + HumanInterface.TonationToString(tonation) + " (" + HumanInterface.GetAllNotesInMaskAsString(tonation.subdominant) + ")")
    print("W dominantach: ")
    for tonation in tonations:
        if tonation.dominant & note:
            print("\t" + HumanInterface.TonationToString(tonation) + " (" + HumanInterface.GetAllNotesInMaskAsString(tonation.dominant) + ")")

# 0 = C1 (32.7 Hz), czyli na drugiej kresce pod pieciolinia z kluczem basowym

if __name__ == "__main__":
    main()