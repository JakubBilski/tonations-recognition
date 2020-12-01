function onclickRecordButton() {
  if(isRecording) {
    mediaRecorder.stop();
    recordButton.textContent = "Start recording";
    filePathInfo.textContent = "Recorded track";
  }
  else {
    mediaRecorder.start();
    if (soundClipContainer.lastChild) {
      soundClipContainer.removeChild(soundClipContainer.lastChild);
    }
    filePathInfo.textContent = "Recording now";
    recordButton.textContent = "Stop recording";
  }
  isRecording = !isRecording;
}

function onstopMediaRecorder() {
  const clipContainer = document.createElement('article');
  const audio = document.createElement('audio');
  clipContainer.classList.add('clip');
  audio.setAttribute('controls', '');
  clipContainer.appendChild(audio);
  soundClipContainer.appendChild(clipContainer);
  const blob = new Blob(recordedChunks, { 'type' : 'audio/ogg; codecs=opus' } );
  recordedChunks = [];
  const audioURL = window.URL.createObjectURL(blob);
  audio.src = audioURL;
  var formData = new FormData();
  formData.append('recordingTemp', blob);
  postFormData(`http://127.0.0.1:5000/recorded`, formData).then(() => {
    filePath = `.\\data\\uploads\\recordingTemp.wav`;
    fetchAndDisplayGuitar(isShowingTransposed, isShowingNotes);
  });
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
