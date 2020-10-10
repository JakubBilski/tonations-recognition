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
    dir_path = parse_args().input
    files = [
        file_name for file_name in dir_path.iterdir() if file_name.suffix in [".mp3", ".wav"]]
    for file in files:
        print(file)
        sounds = sounds_generation.get_sounds_from_file(file)
        print("\n".join([str(sound) for sound in sounds]))
