document.querySelector('#openDialog').addEventListener('click', function (event) {
    window.dialog().showOpenDialog( {
        properties: ['openFile'],
        filters: [
          { name: 'Audio', extensions: ['wav'] }
        ]
      }).then(result => {
        console.log(result.canceled)
        console.log(result.filePaths)
        if(!result.canceled) {
          filePathInfo.textContent = result.filePaths[0];
          filePath = result.filePaths[0];
          if(recordedSoundClipContainer.lastChild) {
            recordedSoundClipContainer.removeChild(recordedSoundClipContainer.lastChild);
          }
          fetchAndDisplayGuitar(isShowingTransposed, isShowingNotes);
        }
      }).catch(err => {
        console.log(err)
      })
});
