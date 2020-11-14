import argparse
import pathlib

import sounds_generation


def parse_args():
    parser = argparse.ArgumentParser(
        description='Convert auio file to notes with time of occurrence')
    parser.add_argument('--input', '-I',
                        required=True,
                        help='Directory with audio files. Formats: [.mp3, .wav]',
                        type=pathlib.Path)
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    file_path = parse_args().input
    sounds = sounds_generation.get_sounds_from_file(file_path)
    # temporary, makes it easier to create test cases
    for sound in sounds:
        print(f"music.Sound({sound.note}, {round(sound.timestamp,3)}, {round(sound.duration_ms,3)}),")
