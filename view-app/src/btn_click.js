let filePathInfo = document.querySelector('#result')

document.querySelector('#openDialog').addEventListener('click', function (event) {
    window.dialog().showOpenDialog( {
        properties: ['openFile']
      }).then(result => {
        console.log(result.canceled)
        console.log(result.filePaths)
        if(!result.canceled) {
          filePathInfo.textContent = result.filePaths;
          localStorage.setItem("filePath", result.filePaths);
        }
        fetchChords();
      }).catch(err => {
        console.log(err)
      })
});