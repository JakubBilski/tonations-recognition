const recordButton = document.querySelector('#record_btn');
const recordedSoundClipContainer = document.querySelector('#recordedSoundClipContainer');
const withChordsSoundClipContainer = document.querySelector('#withChordsSoundClipContainer');
const filePathInfo = document.querySelector('#result')
const result = document.querySelector('#result')
const transposeButton = document.querySelector('#transpose_btn')
const hideNotesButton = document.querySelector('#hide_notes_btn')
const saveWithChordsButton = document.querySelector('#save_with_chords_btn')
const saveRecordedButton = document.querySelector('#save_recorded_btn')

isShowingTransposed = false
isShowingNotes = true
isRecording = false

function unhideLoadingSection() {
  document.getElementById('loading_section').style.display = "block";
}

function hideLoadingSection() {
  document.getElementById('loading_section').style.display = "none";
}

function unhideInvalidFileSection() {
  document.getElementById('invalid_file_section').style.display = "block";
}

function hideInvalidFileSection() {
  document.getElementById('invalid_file_section').style.display = "none";
}

function onclickTransposeButton(){
  if(isShowingTransposed) {
    transposeButton.textContent = "Transpose to easier key";
    transposeButton.className = "main-stroked-button"
    fetchAndDisplayGuitar(false, isShowingNotes);
  } else {
    transposeButton.textContent = "Transpose to original key";
    transposeButton.className = "main-filled-button";
    fetchAndDisplayGuitar(true, isShowingNotes);
  }
  isShowingTransposed = !isShowingTransposed;
}

function onclickHideNotesButton() {
  if(isShowingNotes) {
    hideNotesButton.textContent = "Show notes";
    hideNotesButton.className = "main-filled-button";
    fetchAndDisplayGuitar(isShowingTransposed, false);
  } else {
    hideNotesButton.textContent = "Hide notes";
    hideNotesButton.className = "main-stroked-button"
    fetchAndDisplayGuitar(isShowingTransposed, true);
  }
  isShowingNotes = !isShowingNotes;
}

function onclickSaveWithChordsButton(){
  window.dialog().showSaveDialog( {
    defaultPath: 'resultWithChords.wav'
  }).then(result => {
    if(!result.canceled) {
      var postPath = `http://127.0.0.1:5000/saveWithChords`;
      postJsonData(postPath, {output_file: result.filePath});
    }
  }).catch(err => {
    console.log(err)
  })
}

function onclickSavRecordedButton(){
  window.dialog().showSaveDialog( {
    defaultPath: 'recordedTrack.wav'
  }).then(result => {
    var postPath = `http://127.0.0.1:5000/saveRecorded`;
    postJsonData(postPath, {output_file: result.filePath});
  }).catch(err => {
    console.log(err)
  })
}

transposeButton.addEventListener('click', () => {
  onclickTransposeButton();
});
hideNotesButton.addEventListener('click', () => {
  onclickHideNotesButton();
});
saveWithChordsButton.addEventListener('click', () => {
  onclickSaveWithChordsButton();
});
saveRecordedButton.addEventListener('click', () => {
  onclickSavRecordedButton();
});

hideLoadingSection();
hideInvalidFileSection();
