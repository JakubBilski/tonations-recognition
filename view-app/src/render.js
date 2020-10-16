let input = document.querySelector('#input')
let result = document.querySelector('#result')
let btn = document.querySelector('#btn')

function sendToPython() {
  var { PythonShell } = require('python-shell');

  let options = {
    mode: 'text'
  };
  
  PythonShell.run('././src/tmp_view_app_server.py', options, function (err, results) {
    if (err) throw err;
    // results is an array consisting of messages collected during execution
    console.log('response: ', results);

  });
}

function onclick(){

  fetch(`http://127.0.0.1:5001/${input.value}`).then((data)=>{      
      return data.text();
      
  }).then((text)=>{
    console.log("data: ", text);
    result.textContent = text;
  }).catch(e=>{
    console.log(e);
  })

}
sendToPython();

Python-btn.addEventListener('click', () => {
  onclick();
});

Python-btn.dispatchEvent(new Event('click'))
