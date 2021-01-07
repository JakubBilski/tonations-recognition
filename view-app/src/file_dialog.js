document.querySelector('#openDialog').addEventListener('click', function (event) {
    window.dialog().showOpenDialog( {
        properties: ['openFile'],
        filters: [
          { name: 'Audio', extensions: ['wav'] }
        ]
      }).then(result => {
        if(!result.canceled) {
          filePathInfo.textContent = result.filePaths[0];
          filePath = result.filePaths[0];
          hideSaveRecordedButton();
          if(recordedSoundClipContainer.lastChild) {
            recordedSoundClipContainer.removeChild(recordedSoundClipContainer.lastChild);
          }
          clearCache();
          fetchAndDisplayGuitar(isShowingTransposed, isShowingNotes);
        }
      }).catch(err => {
        console.log(err)
      })
});
