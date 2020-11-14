import parselmouth

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt 
import numpy as np
import seaborn as sns
import pathlib
import argparse
import librosa


def parse_args():
    parser = argparse.ArgumentParser(
        description='Draw graphs for audio file')
    parser.add_argument('--input', '-I',
                        required=True,
                        help='Input audio file. Formats: [.mp3, .wav]',
                        type=pathlib.Path)
    args = parser.parse_args()
    return args


def main():
    sns.set()  # Use seaborn's default style to make attractive graphs
    args = parse_args()

    snd = parselmouth.Sound(str(args.input))
    plt.figure()
    plt.plot(snd.xs(), snd.values.T)
    plt.xlim([snd.xmin, snd.xmax])
    plt.xlabel("time [s]")
    plt.ylabel("amplitude")

    plt.savefig(args.input.stem+"_1.png")
    plt.close()


    def draw_spectrogram(spectrogram, dynamic_range=70):
        X, Y = spectrogram.x_grid(), spectrogram.y_grid()
        sg_db = 10 * np.log10(spectrogram.values)
        plt.pcolormesh(X, Y, sg_db, vmin=sg_db.max() -
                       dynamic_range, cmap='afmhot')
        plt.ylim([spectrogram.ymin, spectrogram.ymax])
        plt.xlabel("time [s]")
        plt.ylabel("frequency [Hz]")

    def draw_intensity(intensity):
        plt.plot(intensity.xs(), intensity.values.T, linewidth=3, color='w')
        plt.plot(intensity.xs(), intensity.values.T, linewidth=1)
        plt.grid(False)
        plt.ylim(0)
        plt.ylabel("intensity [dB]")

    intensity = snd.to_intensity()
    spectrogram = snd.to_spectrogram()
    plt.figure()
    draw_spectrogram(spectrogram)
    plt.twinx()
    draw_intensity(intensity)
    plt.xlim([snd.xmin, snd.xmax])
    plt.savefig(args.input.stem+"_2.png")
    plt.close()


    def draw_pitch(pitch):
        # Extract selected pitch contour, and
        # replace unvoiced samples by NaN to not plot
        pitch_values = pitch.selected_array['frequency']
        pitch_values[pitch_values == 0] = np.nan
        plt.plot(pitch.xs(), pitch_values, 'o', markersize=5, color='w')
        plt.plot(pitch.xs(), pitch_values, 'o', markersize=2)
        plt.grid(False)
        plt.ylim(0, pitch.ceiling)
        plt.ylabel("fundamental frequency [Hz]")

    pitch = snd.to_pitch()
    # If desired, pre-emphasize the sound fragment before calculating the spectrogram
    pre_emphasized_snd = snd.copy()
    pre_emphasized_snd.pre_emphasize()
    # allocation error + large file -> give higher window_length
    spectrogram = pre_emphasized_snd.to_spectrogram(
        window_length=0.01, maximum_frequency=8000)
    plt.figure()
    draw_spectrogram(spectrogram)
    plt.twinx()
    draw_pitch(pitch)
    plt.xlim([snd.xmin, snd.xmax])
    plt.savefig(args.input.stem+"_3.png")
    plt.close()


    intensity = snd.to_intensity()
    y, sr = librosa.load(str(args.input))
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr, units='time')
    plt.figure()
    plt.plot(intensity.xs(), intensity.values.T)
    for b in beats:
        plt.axvline(x=b, color='r')
    plt.savefig(args.input.stem+"_4.png")
    plt.close()




if __name__ == "__main__":
    main()
