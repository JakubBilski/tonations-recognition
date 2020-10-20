const dialog = require('electron').remote.dialog;

window.dialog = function(){
  return dialog;
}
