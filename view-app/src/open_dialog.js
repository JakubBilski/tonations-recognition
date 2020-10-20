const dialog = require('electron').record;

window.aaaaa = function (event) {
    dialog.showOpenDialog(mainWindow, {
        properties: ['openFile']
      }).then(result => {
        console.log(result.canceled)
        console.log(result.filePaths)
      }).catch(err => {
        console.log(err)
      })
}