import parselmouth

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

def main():
    sns.set() # Use seaborn's default style to make attractive graphs

    # TODO: use professional music terminology
    samples = [fileName[:fileName.find(".")] for fileName in os.listdir(".") if fileName.endswith(".mp3")]
    for sample in samples:
        process(sample)


def process(file_prefix):
    snd = parselmouth.Sound(file_prefix + ".mp3")
    plt.figure()
    plt.plot(snd.xs(), snd.values.T)
    plt.xlim([snd.xmin, snd.xmax])
    plt.xlabel("time [s]")
    plt.ylabel("amplitude")
    #plt.show()
    plt.savefig("results/" + file_prefix + "sound.png") # or plt.savefig("sound.pdf")
    plt.close()

    def draw_spectrogram(spectrogram, dynamic_range=70):
        X, Y = spectrogram.x_grid(), spectrogram.y_grid()
        sg_db = 10 * np.log10(spectrogram.values)
        plt.pcolormesh(X, Y, sg_db, vmin=sg_db.max() - dynamic_range, cmap='afmhot')
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
    # plt.show()
    plt.savefig("results/" + file_prefix + "spectrogram.png")
    plt.close()

    def draw_pitch(pitch):
        # Extract selected pitch contour, and
        # replace unvoiced samples by NaN to not plot
        pitch_values = pitch.selected_array['frequency']
        pitch_values[pitch_values==0] = np.nan
        plt.plot(pitch.xs(), pitch_values, 'o', markersize=5, color='w')
        plt.plot(pitch.xs(), pitch_values, 'o', markersize=2)
        plt.grid(False)
        plt.ylim(0, pitch.ceiling)
        plt.ylabel("fundamental frequency [Hz]")

    pitch = snd.to_pitch()
    # for frame in pitch:
    #     print(frame)
    #     for candidate in frame:
    #         print(str(candidate.frequency) + " Hz, strength " + str(candidate.strength))
    print(file_prefix + ": " + get_average_from_pitch(pitch))
    # If desired, pre-emphasize the sound fragment before calculating the spectrogram
    pre_emphasized_snd = snd.copy()
    pre_emphasized_snd.pre_emphasize()
    # allocation error + large file -> give higher window_length
    spectrogram = pre_emphasized_snd.to_spectrogram(window_length=0.01, maximum_frequency=8000)
    plt.figure()
    draw_spectrogram(spectrogram)
    plt.twinx()
    draw_pitch(pitch)
    plt.xlim([snd.xmin, snd.xmax])
    #plt.show()
    plt.savefig("results/" + file_prefix + "spectrogram_0.03.png")
    plt.close()

def get_average_from_pitch(pitch):
    pitchInfo = str(pitch)
    pitchInfo = pitchInfo[pitchInfo.find("Average: "):]
    return pitchInfo[:pitchInfo.find("=")]
    
if __name__ == "__main__":
    main()