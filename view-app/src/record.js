function onclickRecordButton() {
  if(isRecording) {
    mediaRecorder.stop();
    recordButton.textContent = "Start recording";
    filePathInfo.textContent = "Recorded track";
    fetchAndDisplayGuitar(isShowingTransposed, isShowingNotes);
  }
  else {
    mediaRecorder.start();
    filePathInfo.textContent = "Recording now";
    recordButton.textContent = "Stop recording";
  }
  isRecording = !isRecording;
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
          console.log("recorder stopped");
          const clipContainer = document.createElement('article');
          const audio = document.createElement('audio');
                   
          clipContainer.classList.add('clip');
          audio.setAttribute('controls', '');
        
          clipContainer.appendChild(audio);
          if(soundClipContainer.lastChild) {
            soundClipContainer.replaceChild(clipContainer, soundClipContainer.lastChild);
          }
          else {
            soundClipContainer.appendChild(clipContainer);
          }
        
          const blob = new Blob(recordedChunks, { 'type' : 'audio/ogg; codecs=opus' });
          recordedChunks = [];
          const audioURL = window.URL.createObjectURL(blob);
          audio.src = audioURL;
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