
Id CommandLine
  -- -----------
   2 cd .\view-app\
   4 npm install
   6 npm install -g electron-packager --save-dev
  13 electron-packager . tonation --platform=win32 --arch=x64 --overwrite
  14 cd ..
  15 pip install virtualenv
  16 virtualenv env
  17 .\\env\Scripts\activate
  19 pip install -r .\src\requirements.txt
  20 pip install pyinstaller
  41 .\env\Scripts\pyinstaller -F  main.spec
  35 .\dist\main.exe
  10 .view-app\tonation-win32-x64\tonation.exe

  

  datas=[('ffmpeg', 'ffmpeg'), ('fluidsynth', 'fluidsynth'), 
             ('C:\\Users\\Ja\\AppData\\Local\\Programs\\Python\\Python38/Lib/site-packages/librosa/util/example_data', 'librosa/util/example_data'),
             ('C:\\Users\\Ja\\AppData\\Local\\Programs\\Python\\Python38\\Lib\\site-packages\\resampy\\data\\*.npz', 'resampy/data')],