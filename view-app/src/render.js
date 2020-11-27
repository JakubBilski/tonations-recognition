const recordButton = document.querySelector('#record_btn');
const soundClipContainer = document.querySelector('#soundClipContainer');
const filePathInfo = document.querySelector('#result')
const result = document.querySelector('#result')
const transposeButton = document.querySelector('#transpose_btn')
const hideNotesButton = document.querySelector('#hide_notes_btn')
isShowingTransposed = false
isShowingNotes = true
isRecording = false

function onclickTransposeButton(){
  if(isShowingTransposed) {
    transposeButton.textContent = "Transpose to easier tonation";
    transposeButton.className = "main-stroked-button"
    fetchAndDisplayGuitar(false, isShowingNotes);
  } else {
    transposeButton.textContent = "Transpose to original tonation";
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

transposeButton.addEventListener('click', () => {
  onclickTransposeButton();
});
hideNotesButton.addEventListener('click', () => {
  onclickHideNotesButton();
});

