import argparse
import pathlib

from src import music_server


def parse_args():
    parser = argparse.ArgumentParser(
        description='Add chords to audio file')
    parser.add_argument('--input', '-I',
                        default=None,
                        help='Input audio file. Formats: [.mp3, .wav]',
                        type=pathlib.Path)
    parser.add_argument('--key', '-K',
                        help='Use correct key instead of detected',
                        type=str)
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()
    music_server.start_server(args)
