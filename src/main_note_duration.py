import argparse
import pathlib

import sounds_generation


def parse_args():
    parser = argparse.ArgumentParser(
        description='Convert audio file to notes with time of occurrence')
    parser.add_argument('--input', '-I',
                        required=True,
                        help='Input audio file. Formats: [.mp3, .wav]',
                        type=pathlib.Path)
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()
    sounds = sounds_generation.get_sounds_from_file(args.input)

    print("\n".join([str(sound) for sound in sounds]))
    print("\n".join([f"{sound.duration:.3f}: {sounds_generation.note_to_frequency(sound.note)}" for sound in sounds]))
