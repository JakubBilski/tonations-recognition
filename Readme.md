# Review

1. File names of python scripts should be in snake_case (eg bitwide_rotation.py)
2. Function names should be also snake_case
3. Class names ahould be CamelCase, so it is okey :P
4. Constants should be all upper case and usually in seperate file.

# Idea

I wouldn't use bits to represent notes. I would just use list of strings and 
one class (or even just functions) for finding notes in list and to make rotations etc.
notes = ["C", "C#", ..., "H"]

MajorTonation.key would be just string, like
    MajorTonation.key = "C"

and chords would be list of strings
    major_cord(note):
        return [note, get_note(note, 4), get_note(note, 7)]

and there would be just one conversion table to simplify note strings, like:
    SIMPLIFY_NOTES = {
        "CIS" : "C#",
        "DIS" : "D#",
        ...
        "B" : "A#"  
    }