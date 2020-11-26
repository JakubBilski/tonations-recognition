let result = document.querySelector('#result')
let transposeButton = document.querySelector('#transpose_btn')
let hideNotesButton = document.querySelector('#hide_notes_btn')
let isShowingTransposed = false
let isShowingNotes = true

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

