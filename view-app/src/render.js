//let input = document.querySelector('#Python_btn')
let result = document.querySelector('#result')
let btn = document.querySelector('#Python_btn')
// let { PythonShell } = require('python-shell');

function sendToPython() {
  

  let options = {
    mode: 'text'
  };
  
  // PythonShell.run('././src/tmp_view_app_server.py', options, function (err, results) {
  //   if (err) throw err;
  //   // results is an array consisting of messages collected during execution
  //   console.log('response: ', results);

  // });
}

function onclick(){
  console.log(btn.value);
  fetch(`http://127.0.0.1:5001/${btn.value}`).then((data)=>{      
      return data.text();
      
  }).then((text)=>{
    console.log("data: ", text);
    result.textContent = text;
  }).catch(e=>{
    console.log(e);
  })

}
sendToPython();

btn.addEventListener('click', () => {
  onclick();
});

