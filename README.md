﻿"Rozwiązanie będzie napisane z wykorzystaniem języka Python i biblioteki simpleaudio"
https://simpleaudio.readthedocs.io/en/latest/index.html


Ciekawy projekt:
https://github.com/YannickJadoul/Parselmouth
pip3 install praat-parselmouth

Projekt w matlabie, nwm czy działa
https://se.mathworks.com/matlabcentral/fileexchange/73594-piano-guitar-notes-recognition

Stronka do nagrywania
https://online-voice-recorder.com/

Częstotliwości nut
https://pages.mtu.edu/~suits/notefreqs.html

Praca o wykrywaniu akordów:
http://www.eecs.qmul.ac.uk/~markp/2009/StarkPlumbley09-icmc.pdf

Zmiana autora commita:
 git -c user.name="New Author Name" -c user.email=email@address.com commit --amend --reset-author


Testowanie serwera:
``` bash
python3 src/main.py --http
```
i w innym terminalu
```bash
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"input_file":"data/other_rec/ach_spij_C.wav"}' \
  http://localhost:5000/music
```

Automatyczne generowanie dokumentacji:
``` bash
pip install pdoc3
pdoc --html .\path_to_file_or_module
```