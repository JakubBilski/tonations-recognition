import pydub


def convert_file(source_file, destination_file):
    sound = pydub.AudioSegment.from_file(source_file)
    sound.export(destination_file, format="wav")
