document.querySelector('#openDialog').addEventListener('click', function (event) {
    window.dialog().showOpenDialog( {
        properties: ['openFile']
      }).then(result => {
        console.log(result.canceled)
        console.log(result.filePaths)
        if(!result.canceled) {
          filePathInfo.textContent = result.filePaths[0];
          filePath = result.filePaths[0];
          if(soundClipContainer.lastChild) {
            soundClipContainer.removeChild(soundClipContainer.lastChild);
          }
          fetchAndDisplayGuitar(isShowingTransposed, isShowingNotes);
        }
      }).catch(err => {
        console.log(err)
      })
});
