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

async function postData(url = '', data = {}) {
  // Default options are marked with *
  const response = await fetch(url, {
    method: 'POST', // *GET, POST, PUT, DELETE, etc.
    headers: {
      'Content-Type': 'application/json'
      // 'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: JSON.stringify(data) // body data type must match "Content-Type" header
  });
  return response.json(); // parses JSON response into native JavaScript objects
}

function onclick(){
  console.log(btn.value);
  postData(`http://127.0.0.1:5000/music`, {input_file: localStorage.getItem("filePath")}).then((data)=>{      
      return data;
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

