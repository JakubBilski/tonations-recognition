const VF = vextab.Vex.Flow

const renderer = new VF.Renderer($('#boo')[0],
	VF.Renderer.Backends.SVG);

// Initialize VexTab artist and parser.
const artist = new vextab.Artist(10, 10, 750, { scale: 0.8 });
const tab = new vextab.VexTab(artist);

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

function fetchChords(){
  postData(`http://127.0.0.1:5000/music`, {input_file: localStorage.getItem("filePath")}).then((data)=>{      
      return data;
  }).then((text)=>{
    console.log("data: ", text);
    result.textContent = text;
    tab.reset();
    artist.reset();
    
    for (let i = 0; i < text.notes.length; i++) {
      if(i==0) {
        tab.parse(`tabstave notation=true key=${text.key} time=${text.metrum}\nnotes ${text.notes[i]}`);
      }
      else {
        tab.parse(`tabstave notation=true key=${text.key} \nnotes ${text.notes[i]}`);
      }
    }
    artist.render(renderer);
  }).catch(e=>{
    console.log(e);
  });
}