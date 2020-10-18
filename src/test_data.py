import music
import pathlib

class TestModel:
    def __init__(self, file_path, sounds, tonations, chords):
        self.file_path = file_path
        self.sounds = sounds
        self.tonations = tonations
        self.chords = chords

def get_all_test_models():
    models = get_other_rec_test_models()
    return models

def get_other_rec_test_models():
    result = []
    file_path = pathlib.Path("data\\other_rec\\ach_spij_C.wav")
    sounds = [
        music.Sound(None, 0.0, 0.7),
        music.Sound(0, 0.7, 0.53),
        music.Sound(7, 1.23, 1.09),
        music.Sound(None, 2.32, 0.21),
        music.Sound(4, 2.53, 0.55),
        music.Sound(2, 3.08, 0.52),
        music.Sound(None, 3.6, 0.01),
        music.Sound(7, 3.61, 0.8),
        music.Sound(None, 4.41, 0.3),
        music.Sound(4, 4.71, 0.27),
        music.Sound(5, 4.98, 0.25),
        music.Sound(7, 5.25, 0.26),
        music.Sound(9, 5.51, 0.22),
        music.Sound(7, 5.73, 0.3),
        music.Sound(9, 6.03, 0.26),
        music.Sound(7, 6.29, 0.55),
        music.Sound(4, 6.86, 0.54),
        music.Sound(2, 7.37, 0.55),
        music.Sound(None, 7.92, 0.01),
        music.Sound(7, 7.93, 0.7),
        music.Sound(None, 8.63, 0.34),
        music.Sound(0, 8.97, 0.27),
        music.Sound(2, 9.24, 0.31),
        music.Sound(4, 9.55, 0.62),
        music.Sound(None, 10.17, 0.07),
        music.Sound(4, 10.24, 0.19),
        music.Sound(None, 10.43, 0.06),
        music.Sound(4, 10.49, 0.36),
        music.Sound(None, 10.85, 0.14),
        music.Sound(0, 10.99, 0.26),
        music.Sound(2, 11.26, 0.27),
        music.Sound(4, 11.58, 0.98),
        music.Sound(None, 12.5, 0.02),
        music.Sound(4, 12.52, 0.35),
        music.Sound(None, 12.87, 0.14),
        music.Sound(0, 13.01, 0.25),
        music.Sound(2, 13.28, 0.32),
        music.Sound(4, 13.59, 0.76),
        music.Sound(0, 14.34, 0.6),
        music.Sound(7, 14.94, 0.52),
        music.Sound(None, 15.46, 0.01),
        music.Sound(2, 15.47, 0.55),
        music.Sound(0, 16.02, 0.84),
        music.Sound(None, 16.86, 1.58)
        ]
    tonations = [music.Tonation(0, 0.0, sounds[-1].end_timestamp, "major")]
    result.append(TestModel(file_path, sounds, tonations, None))

    file_path = pathlib.Path("data\\other_rec\\gdy_sliczna_panna_F.wav")
    sounds = [
        music.Sound(None, 0.0, 0.835),
        music.Sound(0, 0.835, 0.93),
        music.Sound(2, 1.765, 0.46),
        music.Sound(4, 2.225, 0.44),
        music.Sound(5, 2.665, 0.67),
        music.Sound(None, 3.335, 0.25),
        music.Sound(5, 3.585, 0.91),
        music.Sound(7, 4.495, 0.48),
        music.Sound(10, 4.975, 0.45),
        music.Sound(9, 5.425, 0.48),
        music.Sound(7, 5.905, 0.43),
        music.Sound(7, 6.335, 0.95),
        music.Sound(5, 7.285, 0.66),
        music.Sound(None, 7.945, 0.3),
        music.Sound(0, 8.245, 0.86),
        music.Sound(2, 9.105, 0.46),
        music.Sound(4, 9.565, 0.43),
        music.Sound(5, 9.995, 0.64),
        music.Sound(None, 10.635, 0.25),
        music.Sound(5, 10.885, 0.9),
        music.Sound(7, 11.785, 0.42),
        music.Sound(10, 12.205, 0.46),
        music.Sound(9, 12.665, 0.5),
        music.Sound(7, 13.165, 0.53),
        music.Sound(7, 13.695, 0.96),
        music.Sound(5, 14.655, 0.78),
        music.Sound(None, 15.435, 0.24),
        music.Sound(9, 15.675, 0.47),
        music.Sound(7, 16.145, 0.46),
        music.Sound(9, 16.605, 0.48),
        music.Sound(5, 17.085, 0.46),
        music.Sound(7, 17.545, 1.09),
        music.Sound(None, 18.635, 1.0),
        music.Sound(4, 19.635, 0.47),
        music.Sound(7, 20.105, 0.47),
        music.Sound(5, 20.575, 0.46),
        music.Sound(4, 21.035, 0.5),
        music.Sound(2, 21.535, 1.02),
        music.Sound(0, 22.555, 0.67),
        music.Sound(None, 23.225, 0.31),
        music.Sound(9, 23.535, 0.49),
        music.Sound(7, 24.025, 0.45),
        music.Sound(9, 24.475, 0.48),
        music.Sound(5, 24.955, 0.71),
        music.Sound(10, 25.665, 1.19),
        music.Sound(None, 26.855, 0.55),
        music.Sound(9, 27.405, 0.46),
        music.Sound(0, 27.865, 0.44),
        music.Sound(10, 28.305, 0.3),
        music.Sound(9, 28.605, 0.2),
        music.Sound(7, 28.805, 0.25),
        music.Sound(5, 29.055, 0.31),
        music.Sound(7, 29.365, 0.98),
        music.Sound(5, 30.345, 0.78),
        music.Sound(None, 31.125, 1.33),
        ]
    tonations = [music.Tonation(5, 0.0, sounds[-1].end_timestamp, "major")]
    result.append(TestModel(file_path, sounds, tonations, None))

    file_path = pathlib.Path("data\\other_rec\\jedzie_pocią_z_daleka_F.wav")
    sounds = [
        music.Sound(None, 0.0, 0.671),
        music.Sound(0, 0.671, 0.43),
        music.Sound(5, 1.101, 0.44),
        music.Sound(9, 1.541, 0.43),
        music.Sound(7, 1.971, 0.44),
        music.Sound(5, 2.411, 0.43),
        music.Sound(4, 2.841, 0.43),
        music.Sound(5, 3.271, 0.64),
        music.Sound(None, 3.911, 0.2),
        music.Sound(0, 4.111, 0.35),
        music.Sound(None, 4.461, 0.13),
        music.Sound(5, 4.591, 0.42),
        music.Sound(9, 5.011, 0.44),
        music.Sound(7, 5.451, 0.46),
        music.Sound(5, 5.911, 0.46),
        music.Sound(4, 6.371, 0.35),
        music.Sound(None, 6.721, 0.12),
        music.Sound(5, 6.841, 0.63),
        music.Sound(None, 7.471, 0.21),
        music.Sound(5, 7.681, 0.48),
        music.Sound(5, 8.161, 0.43),
        music.Sound(9, 8.591, 0.44),
        music.Sound(0, 9.031, 0.33),
        music.Sound(None, 9.361, 0.12),
        music.Sound(10, 9.481, 0.46),
        music.Sound(9, 9.941, 0.35),
        music.Sound(None, 10.291, 0.11),
        music.Sound(10, 10.401, 0.64),
        music.Sound(None, 11.041, 0.2),
        music.Sound(0, 11.241, 0.45),
        music.Sound(0, 11.691, 0.46),
        music.Sound(7, 12.151, 0.39),
        music.Sound(10, 12.541, 0.45),
        music.Sound(9, 12.991, 0.44),
        music.Sound(7, 13.431, 0.42),
        music.Sound(5, 13.851, 0.7),
        music.Sound(None, 14.551, 1.45),
        ]
    tonations = [music.Tonation(5, 0.0, sounds[-1].end_timestamp, "major")]
    result.append(TestModel(file_path, sounds, tonations, None))
    
    file_path = pathlib.Path("data\\other_rec\\lato_lato_C.wav")
    sounds = [
        music.Sound(None, 0.0, 0.554),
        music.Sound(7, 0.554, 0.52),
        music.Sound(7, 1.074, 0.5),
        music.Sound(4, 1.574, 0.25),
        music.Sound(7, 1.824, 0.58),
        music.Sound(None, 2.404, 0.16),
        music.Sound(9, 2.564, 0.49),
        music.Sound(7, 3.054, 0.49),
        music.Sound(5, 3.544, 0.25),
        music.Sound(2, 3.794, 0.63),
        music.Sound(None, 4.424, 0.16),
        music.Sound(5, 4.584, 0.52),
        music.Sound(5, 5.104, 0.46),
        music.Sound(2, 5.564, 0.27),
        music.Sound(5, 5.834, 0.61),
        music.Sound(None, 6.444, 0.13),
        music.Sound(7, 6.574, 0.5),
        music.Sound(5, 7.074, 0.51),
        music.Sound(4, 7.584, 0.25),
        music.Sound(0, 7.834, 0.57),
        music.Sound(None, 8.404, 0.2),
        music.Sound(7, 8.604, 0.38),
        music.Sound(None, 8.984, 0.12),
        music.Sound(7, 9.104, 0.53),
        music.Sound(4, 9.634, 0.25),
        music.Sound(7, 9.884, 0.54),
        music.Sound(None, 10.424, 0.18),
        music.Sound(0, 10.604, 0.52),
        music.Sound(9, 11.124, 0.42),
        music.Sound(None, 11.544, 0.11),
        music.Sound(7, 11.654, 0.74),
        music.Sound(None, 12.394, 0.16),
        music.Sound(5, 12.554, 0.24),
        music.Sound(7, 12.794, 0.24),
        music.Sound(9, 13.034, 0.23),
        music.Sound(5, 13.264, 0.3),
        music.Sound(4, 13.564, 0.33),
        music.Sound(None, 13.894, 0.18),
        music.Sound(0, 14.074, 0.35),
        music.Sound(None, 14.424, 0.15),
        music.Sound(2, 14.574, 0.96),
        music.Sound(None, 15.534, 1.35),
        ]
    tonations = [music.Tonation(0, 0.0, sounds[-1].end_timestamp, "major")]
    result.append(TestModel(file_path, sounds, tonations, None))
    
    file_path = pathlib.Path("data\\other_rec\\opadły_mgły_C.wav")
    sounds = [
        music.Sound(None, 0.0, 0.581),
        music.Sound(0, 0.581, 0.67),
        music.Sound(2, 1.251, 0.45),
        music.Sound(4, 1.701, 0.43),
        music.Sound(4, 2.131, 0.68),
        music.Sound(4, 2.811, 0.47),
        music.Sound(5, 3.281, 1.64),
        music.Sound(4, 4.921, 0.46),
        music.Sound(4, 5.381, 0.36),
        music.Sound(None, 5.741, 0.1),
        music.Sound(4, 5.841, 0.21),
        music.Sound(2, 6.051, 0.26),
        music.Sound(0, 6.311, 0.22),
        music.Sound(2, 6.531, 0.64),
        music.Sound(None, 7.171, 0.13),
        music.Sound(0, 7.301, 0.66),
        music.Sound(2, 7.961, 0.47),
        music.Sound(4, 8.431, 0.27),
        music.Sound(None, 8.701, 0.11),
        music.Sound(4, 8.811, 0.27),
        music.Sound(4, 9.081, 0.48),
        music.Sound(4, 9.561, 0.46),
        music.Sound(5, 10.021, 0.42),
        music.Sound(5, 10.441, 1.2),
        music.Sound(4, 11.641, 0.45),
        music.Sound(4, 12.091, 0.45),
        music.Sound(4, 12.541, 0.23),
        music.Sound(2, 12.771, 0.27),
        music.Sound(0, 13.041, 0.19),
        music.Sound(2, 13.231, 0.69),
        music.Sound(None, 13.921, 0.68),
        music.Sound(2, 14.601, 0.48),
        music.Sound(0, 15.081, 0.28),
        music.Sound(11, 15.361, 0.19),
        music.Sound(0, 15.551, 0.83),
        music.Sound(None, 16.381, 1.58),
        ]
    tonations = [music.Tonation(0, 0.0, sounds[-1].end_timestamp, "major")]
    result.append(TestModel(file_path, sounds, tonations, None))
    
    file_path = pathlib.Path("data\\other_rec\\opadły_mgły_D.wav")
    sounds = [
        music.Sound(None, 0.0, 0.491),
        music.Sound(2, 0.491, 0.68),
        music.Sound(4, 1.171, 0.43),
        music.Sound(6, 1.601, 0.32),
        music.Sound(None, 1.921, 0.11),
        music.Sound(6, 2.031, 0.6),
        music.Sound(None, 2.631, 0.12),
        music.Sound(6, 2.751, 0.35),
        music.Sound(None, 3.101, 0.13),
        music.Sound(7, 3.231, 0.42),
        music.Sound(7, 3.651, 0.59),
        music.Sound(None, 4.241, 0.15),
        music.Sound(7, 4.391, 0.46),
        music.Sound(6, 4.851, 0.46),
        music.Sound(6, 5.311, 0.3),
        music.Sound(None, 5.611, 0.13),
        music.Sound(6, 5.741, 0.31),
        music.Sound(4, 6.051, 0.18),
        music.Sound(2, 6.231, 0.27),
        music.Sound(4, 6.501, 0.54),
        music.Sound(None, 7.041, 0.16),
        music.Sound(2, 7.201, 0.68),
        music.Sound(4, 7.881, 0.44),
        music.Sound(6, 8.321, 0.27),
        music.Sound(None, 8.591, 0.18),
        music.Sound(6, 8.771, 0.23),
        music.Sound(6, 9.001, 0.23),
        music.Sound(None, 9.231, 0.24),
        music.Sound(6, 9.471, 0.33),
        music.Sound(None, 9.801, 0.16),
        music.Sound(7, 9.961, 0.33),
        music.Sound(None, 10.291, 0.1),
        music.Sound(7, 10.391, 0.53),
        music.Sound(None, 10.921, 0.16),
        music.Sound(7, 11.081, 0.35),
        music.Sound(None, 11.431, 0.15),
        music.Sound(6, 11.581, 0.31),
        music.Sound(None, 11.891, 0.13),
        music.Sound(6, 12.021, 0.27),
        music.Sound(None, 12.291, 0.15),
        music.Sound(6, 12.441, 0.28),
        music.Sound(4, 12.721, 0.18),
        music.Sound(2, 12.901, 0.29),
        music.Sound(4, 13.191, 0.51),
        music.Sound(None, 13.701, 0.16),
        music.Sound(4, 13.861, 0.68),
        music.Sound(2, 14.541, 0.26),
        music.Sound(1, 14.801, 0.21),
        music.Sound(2, 15.011, 0.75),
        music.Sound(None, 15.761, 1.14),
        ]
    tonations = [music.Tonation(2, 0.0, sounds[-1].end_timestamp, "major")]
    result.append(TestModel(file_path, sounds, tonations, None))
    
    file_path = pathlib.Path("data\\other_rec\\o_moj_rozmarunie_c.wav")
    sounds = [
        music.Sound(None, 0.0, 0.604),
        music.Sound(0, 0.604, 0.86),
        music.Sound(0, 1.464, 0.35),
        music.Sound(5, 1.814, 0.59),
        music.Sound(3, 2.404, 0.62),
        music.Sound(2, 3.024, 0.68),
        music.Sound(3, 3.704, 0.33),
        music.Sound(2, 4.034, 0.33),
        music.Sound(0, 4.364, 0.81),
        music.Sound(None, 5.174, 0.35),
        music.Sound(7, 5.524, 0.86),
        music.Sound(7, 6.384, 0.3),
        music.Sound(0, 6.684, 0.59),
        music.Sound(10, 7.274, 0.59),
        music.Sound(8, 7.864, 0.53),
        music.Sound(10, 8.394, 0.31),
        music.Sound(9, 8.704, 0.13),
        music.Sound(8, 8.834, 0.17),
        music.Sound(7, 9.004, 0.81),
        music.Sound(None, 9.814, 0.4),
        music.Sound(7, 10.214, 0.54),
        music.Sound(7, 10.754, 0.27),
        music.Sound(7, 11.024, 0.33),
        music.Sound(8, 11.354, 0.58),
        music.Sound(7, 11.934, 0.56),
        music.Sound(5, 12.494, 0.31),
        music.Sound(3, 12.804, 0.23),
        music.Sound(2, 13.034, 0.29),
        music.Sound(3, 13.324, 0.4),
        music.Sound(5, 13.724, 0.55),
        music.Sound(3, 14.274, 0.65),
        music.Sound(2, 14.924, 0.54),
        music.Sound(3, 15.464, 0.3),
        music.Sound(5, 15.764, 0.29),
        music.Sound(7, 16.054, 0.8),
        music.Sound(None, 16.854, 0.35),
        music.Sound(7, 17.204, 0.82),
        music.Sound(7, 18.024, 0.33),
        music.Sound(8, 18.354, 0.54),
        music.Sound(7, 18.894, 0.56),
        music.Sound(5, 19.454, 0.35),
        music.Sound(3, 19.804, 0.23),
        music.Sound(2, 20.034, 0.3),
        music.Sound(3, 20.334, 0.27),
        music.Sound(5, 20.604, 0.54),
        music.Sound(3, 21.144, 0.59),
        music.Sound(2, 21.734, 0.52),
        music.Sound(3, 22.254, 0.32),
        music.Sound(2, 22.574, 0.29),
        music.Sound(0, 22.864, 0.6),
        music.Sound(None, 23.464, 1.46),
        ]
    tonations = [music.Tonation(0, 0.0, sounds[-1].end_timestamp, "minor")]
    result.append(TestModel(file_path, sounds, tonations, None))
    
    file_path = pathlib.Path("data\\other_rec\\o_moj_rozmarunie_e.wav")
    sounds = [
        music.Sound(None, 0.0, 0.633),
        music.Sound(4, 0.633, 0.45),
        music.Sound(4, 1.083, 0.51),
        music.Sound(9, 1.593, 0.5),
        music.Sound(7, 2.093, 0.51),
        music.Sound(6, 2.603, 0.53),
        music.Sound(7, 3.133, 0.29),
        music.Sound(6, 3.423, 0.26),
        music.Sound(4, 3.683, 0.78),
        music.Sound(None, 4.463, 0.29),
        music.Sound(11, 4.753, 1.01),
        music.Sound(4, 5.763, 0.47),
        music.Sound(2, 6.233, 0.53),
        music.Sound(0, 6.763, 0.51),
        music.Sound(2, 7.273, 0.27),
        music.Sound(0, 7.543, 0.24),
        music.Sound(11, 7.783, 0.71),
        music.Sound(None, 8.493, 0.26),
        music.Sound(11, 8.753, 0.47),
        music.Sound(11, 9.223, 0.53),
        music.Sound(0, 9.753, 0.47),
        music.Sound(11, 10.223, 0.49),
        music.Sound(9, 10.713, 0.3),
        music.Sound(7, 11.013, 0.24),
        music.Sound(6, 11.253, 0.2),
        music.Sound(7, 11.453, 0.3),
        music.Sound(9, 11.753, 0.53),
        music.Sound(7, 12.283, 0.51),
        music.Sound(6, 12.793, 0.48),
        music.Sound(7, 13.273, 0.32),
        music.Sound(9, 13.593, 0.21),
        music.Sound(11, 13.803, 0.81),
        music.Sound(None, 14.613, 0.28),
        music.Sound(11, 14.893, 1.0),
        music.Sound(0, 15.893, 0.5),
        music.Sound(11, 16.393, 0.49),
        music.Sound(9, 16.883, 0.28),
        music.Sound(7, 17.163, 0.24),
        music.Sound(6, 17.403, 0.24),
        music.Sound(7, 17.643, 0.31),
        music.Sound(9, 17.953, 0.45),
        music.Sound(7, 18.403, 0.49),
        music.Sound(6, 18.893, 0.5),
        music.Sound(7, 19.393, 0.28),
        music.Sound(6, 19.673, 0.31),
        music.Sound(4, 19.983, 0.67),
        music.Sound(None, 20.653, 1.37),
        ]
    tonations = [music.Tonation(4, 0.0, sounds[-1].end_timestamp, "minor")]
    result.append(TestModel(file_path, sounds, tonations, None))
    
    file_path = pathlib.Path("data\\other_rec\\panie_JanieC.wav")
    sounds = [
        music.Sound(None, 0.0, 0.742),
        music.Sound(0, 0.742, 0.43),
        music.Sound(2, 1.172, 0.43),
        music.Sound(4, 1.602, 0.37),
        music.Sound(0, 1.972, 0.39),
        music.Sound(0, 2.362, 0.4),
        music.Sound(2, 2.762, 0.41),
        music.Sound(4, 3.172, 0.43),
        music.Sound(0, 3.602, 0.31),
        music.Sound(None, 3.912, 0.11),
        music.Sound(4, 4.022, 0.39),
        music.Sound(5, 4.412, 0.42),
        music.Sound(7, 4.832, 0.61),
        music.Sound(None, 5.442, 0.17),
        music.Sound(4, 5.612, 0.38),
        music.Sound(5, 5.992, 0.48),
        music.Sound(7, 6.472, 0.56),
        music.Sound(None, 7.032, 0.21),
        music.Sound(7, 7.242, 0.28),
        music.Sound(9, 7.522, 0.19),
        music.Sound(7, 7.712, 0.19),
        music.Sound(5, 7.902, 0.49),
        music.Sound(4, 8.392, 0.3),
        music.Sound(0, 8.692, 0.3),
        music.Sound(None, 8.992, 0.11),
        music.Sound(7, 9.102, 0.27),
        music.Sound(9, 9.372, 0.19),
        music.Sound(7, 9.562, 0.18),
        music.Sound(5, 9.742, 0.22),
        music.Sound(4, 9.962, 0.4),
        music.Sound(0, 10.362, 0.39),
        music.Sound(0, 10.752, 0.43),
        music.Sound(7, 11.182, 0.44),
        music.Sound(0, 11.622, 0.56),
        music.Sound(None, 12.182, 0.27),
        music.Sound(0, 12.452, 0.49),
        music.Sound(7, 12.942, 0.37),
        music.Sound(0, 13.312, 0.58),
        music.Sound(None, 13.892, 1.31),
        ]
    tonations = [music.Tonation(0, 0.0, sounds[-1].end_timestamp, "major")]
    result.append(TestModel(file_path, sounds, tonations, None))
    
    file_path = pathlib.Path("data\\other_rec\\przybieżeli.wav")
    sounds = [
        music.Sound(None, 0.0, 0.542),
        music.Sound(0, 0.542, 0.28),
        music.Sound(11, 0.822, 0.29),
        music.Sound(0, 1.112, 0.3),
        music.Sound(2, 1.412, 0.32),
        music.Sound(4, 1.732, 0.31),
        music.Sound(2, 2.042, 0.3),
        music.Sound(4, 2.342, 0.29),
        music.Sound(5, 2.632, 0.34),
        music.Sound(7, 2.972, 0.48),
        music.Sound(None, 3.452, 0.18),
        music.Sound(9, 3.632, 0.48),
        music.Sound(None, 4.112, 0.15),
        music.Sound(7, 4.262, 0.85),
        music.Sound(None, 5.112, 0.31),
        music.Sound(0, 5.422, 0.32),
        music.Sound(11, 5.742, 0.27),
        music.Sound(0, 6.012, 0.28),
        music.Sound(2, 6.292, 0.31),
        music.Sound(4, 6.602, 0.29),
        music.Sound(2, 6.892, 0.31),
        music.Sound(4, 7.202, 0.28),
        music.Sound(5, 7.482, 0.32),
        music.Sound(7, 7.802, 0.49),
        music.Sound(None, 8.292, 0.13),
        music.Sound(9, 8.422, 0.45),
        music.Sound(None, 8.872, 0.15),
        music.Sound(7, 9.022, 0.87),
        music.Sound(None, 9.892, 0.43),
        music.Sound(0, 10.322, 0.41),
        music.Sound(None, 10.732, 0.18),
        music.Sound(7, 10.912, 0.62),
        music.Sound(9, 11.532, 0.27),
        music.Sound(7, 11.802, 0.29),
        music.Sound(5, 12.092, 0.31),
        music.Sound(4, 12.402, 0.34),
        music.Sound(5, 12.742, 0.48),
        music.Sound(None, 13.222, 0.13),
        music.Sound(5, 13.352, 0.3),
        music.Sound(9, 13.652, 0.29),
        music.Sound(7, 13.942, 0.29),
        music.Sound(5, 14.232, 0.29),
        music.Sound(4, 14.522, 0.31),
        music.Sound(2, 14.832, 0.31),
        music.Sound(4, 15.142, 0.37),
        music.Sound(None, 15.512, 0.21),
        music.Sound(5, 15.722, 0.47),
        music.Sound(None, 16.192, 0.13),
        music.Sound(7, 16.322, 0.92),
        music.Sound(None, 17.242, 0.32),
        music.Sound(4, 17.562, 0.5),
        music.Sound(None, 18.062, 0.14),
        music.Sound(2, 18.202, 0.61),
        music.Sound(0, 18.812, 1.06),
        music.Sound(None, 19.872, 1.28),
        ]
    tonations = [music.Tonation(0, 0.0, sounds[-1].end_timestamp, "major")]
    result.append(TestModel(file_path, sounds, tonations, None))
    
    file_path = pathlib.Path("data\\other_rec\\płonie_ognisko_c.wav")
    sounds = [
        music.Sound(None, 0.0, 0.74),
        music.Sound(0, 0.74, 0.38),
        music.Sound(2, 1.12, 0.35),
        music.Sound(3, 1.47, 0.7),
        music.Sound(5, 2.17, 0.39),
        music.Sound(3, 2.56, 0.35),
        music.Sound(2, 2.91, 0.7),
        music.Sound(3, 3.61, 0.35),
        music.Sound(2, 3.96, 0.36),
        music.Sound(0, 4.32, 0.7),
        music.Sound(7, 5.02, 0.92),
        music.Sound(None, 5.94, 0.33),
        music.Sound(0, 6.27, 0.75),
        music.Sound(2, 7.02, 0.75),
        music.Sound(7, 7.77, 0.69),
        music.Sound(3, 8.46, 0.68),
        music.Sound(2, 9.14, 0.72),
        music.Sound(0, 9.86, 1.13),
        music.Sound(None, 10.99, 0.5),
        music.Sound(0, 11.49, 0.36),
        music.Sound(2, 11.85, 0.4),
        music.Sound(3, 12.25, 0.63),
        music.Sound(5, 12.88, 0.39),
        music.Sound(3, 13.27, 0.37),
        music.Sound(2, 13.64, 0.71),
        music.Sound(3, 14.35, 0.38),
        music.Sound(2, 14.73, 0.39),
        music.Sound(0, 15.12, 0.69),
        music.Sound(7, 15.81, 1.03),
        music.Sound(None, 16.84, 0.26),
        music.Sound(0, 17.1, 0.74),
        music.Sound(2, 17.84, 0.74),
        music.Sound(8, 18.58, 0.71),
        music.Sound(7, 19.29, 0.92),
        music.Sound(11, 20.21, 0.7),
        music.Sound(0, 20.91, 1.6),
        music.Sound(None, 22.51, 0.33),
        ]
    tonations = [music.Tonation(0, 0.0, sounds[-1].end_timestamp, "minor")]
    result.append(TestModel(file_path, sounds, tonations, None))
    
    file_path = pathlib.Path("data\\other_rec\\sto_lat_C.wav")
    sounds = [
        music.Sound(None, 0.0, 0.813),
        music.Sound(7, 0.813, 0.48),
        music.Sound(4, 1.293, 0.5),
        music.Sound(7, 1.793, 0.39),
        music.Sound(None, 2.183, 0.11),
        music.Sound(4, 2.293, 0.38),
        music.Sound(None, 2.673, 0.13),
        music.Sound(7, 2.803, 0.51),
        music.Sound(9, 3.313, 0.25),
        music.Sound(7, 3.563, 0.23),
        music.Sound(5, 3.793, 0.25),
        music.Sound(4, 4.043, 0.25),
        music.Sound(5, 4.293, 0.69),
        music.Sound(None, 4.983, 0.24),
        music.Sound(5, 5.223, 0.52),
        music.Sound(2, 5.743, 0.48),
        music.Sound(5, 6.223, 0.5),
        music.Sound(2, 6.723, 0.43),
        music.Sound(None, 7.153, 0.1),
        music.Sound(5, 7.253, 0.48),
        music.Sound(7, 7.733, 0.25),
        music.Sound(5, 7.983, 0.24),
        music.Sound(4, 8.223, 0.23),
        music.Sound(2, 8.453, 0.27),
        music.Sound(4, 8.723, 0.76),
        music.Sound(None, 9.483, 0.23),
        music.Sound(7, 9.713, 0.31),
        music.Sound(7, 10.023, 0.22),
        music.Sound(4, 10.243, 0.32),
        music.Sound(None, 10.563, 0.13),
        music.Sound(7, 10.693, 0.53),
        music.Sound(4, 11.223, 0.4),
        music.Sound(None, 11.623, 0.12),
        music.Sound(7, 11.743, 0.5),
        music.Sound(0, 12.243, 0.25),
        music.Sound(11, 12.493, 0.24),
        music.Sound(9, 12.733, 0.21),
        music.Sound(7, 12.943, 0.3),
        music.Sound(9, 13.243, 0.72),
        music.Sound(None, 13.963, 0.22),
        music.Sound(11, 14.183, 0.75),
        music.Sound(None, 14.933, 0.19),
        music.Sound(11, 15.123, 0.42),
        music.Sound(None, 15.543, 0.1),
        music.Sound(11, 15.643, 0.47),
        music.Sound(0, 16.113, 0.95),
        music.Sound(None, 17.063, 1.49),
        ]
    tonations = [music.Tonation(0, 0.0, sounds[-1].end_timestamp, "major")]
    result.append(TestModel(file_path, sounds, tonations, None))
    return result