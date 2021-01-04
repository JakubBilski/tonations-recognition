function onclickRecordButton() {
  if(isRecording) {
    mediaRecorder.stop();
    recordButton.textContent = "Start recording";
    filePathInfo.textContent = "Recorded track";
    unhideSaveRecordedButton();
  }
  else {
    mediaRecorder.start();
    if (recordedSoundClipContainer.lastChild) {
      recordedSoundClipContainer.removeChild(recordedSoundClipContainer.lastChild);
    }
    filePathInfo.textContent = "Recording now";
    recordButton.textContent = "Stop recording";
    hideSaveRecordedButton();
  }
  isRecording = !isRecording;
}

function onstopMediaRecorder() {
  const clipContainer = document.createElement('article');
  const audio = document.createElement('audio');
  clipContainer.classList.add('clip');
  audio.setAttribute('controls', '');
  clipContainer.appendChild(audio);
  recordedSoundClipContainer.appendChild(clipContainer);
  const blob = new Blob(recordedChunks, { 'type' : 'audio/ogg; codecs=opus' } );
  recordedChunks = [];
  const audioURL = window.URL.createObjectURL(blob);
  audio.src = audioURL;
  var formData = new FormData();
  formData.append('recordingTemp', blob);
  postFormData(`http://127.0.0.1:5000/recorded`, formData).then((data)=>{      
    return data;
    }).then((text)=>{
      filePath = text.filename;
      clearCache();
      fetchAndDisplayGuitar(isShowingTransposed, isShowingNotes);
  });
}

function unhideSaveRecordedButton() {
  document.getElementById('save_recorded_btn').style.display = "initial";
}

function hideSaveRecordedButton() {
  document.getElementById('save_recorded_btn').style.display = "none";
}

let recordedChunks = [];

if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
  console.log('getUserMedia supported.');
  navigator.mediaDevices.getUserMedia (
     {
        audio: true
     })
     .then(function(stream) {
        mediaRecorder = new MediaRecorder(stream);
        mediaRecorder.ondataavailable = function(e) {
          recordedChunks.push(e.data);
        }
        mediaRecorder.onstop = function(e) {
          onstopMediaRecorder();
        }
     })
     .catch(function(err) {
        console.log('The following getUserMedia error occured: ' + err);
     }
  );
} else {
  console.log('getUserMedia not supported on your browser!');
}

recordButton.addEventListener('click', () => {
  onclickRecordButton();
});

hideSaveRecordedButton();