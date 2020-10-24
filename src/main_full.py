from pydub import AudioSegment
import argparse
import pathlib

import tonations_generation
import sounds_generation
import chords_generation
import meter_recognition
import music_synthesis
import sounds_manipulation


def parse_args():
    parser = argparse.ArgumentParser(
        description='Add chords to audio file')
    parser.add_argument('--input', '-I',
                        required=True,
                        help='Input audio file. Formats: [.mp3, .wav]',
                        type=pathlib.Path)
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()
    sounds = sounds_generation.get_sounds_from_file(args.input)
    sounds = sounds_manipulation.change_tonation(sounds, 2)

    tempo, beats = meter_recognition.get_meter(args.input, sounds)
    sounds = meter_recognition.update_sounds1(tempo, beats, sounds)
    print(f"Tempo: {tempo}")

    print("Sounds:")
    print("\n".join([f"{sound.timestamp:.3f}: {sound.symbol}\t{sound.duration:.3f}" for sound in sounds]))  # noqa

    tonation = tonations_generation.get_tonations_from_sounds(sounds)
    tonation = tonation[0]
    chords = chords_generation.get_chords(sounds, tonation, tempo,
                                          sounds[0].timestamp)

    print("Chords:")
    print("\n".join([f"{chord.timestamp:.3f}: {chord}\t{chord.duration:.3f}" for chord in chords]))  # noqa

    music_synthesis.midi_from_sounds(sounds, 'sounds')
    music_synthesis.midi_from_chords(chords, 'chords')

    sound1 = AudioSegment.from_file("sounds.wav")
    sound2 = AudioSegment.from_file("chords.wav")

    # change volume
    sound2 = sound2 - 8

    # mix sounds and chords
    combined = sound1.overlay(sound2)

    combined.export("result.wav", format='wav')
