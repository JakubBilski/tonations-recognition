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

function fetchAndDisplaySimplifiedGuitar(){
  postData(`http://127.0.0.1:5000/music`, {input_file: localStorage.getItem("filePath")}).then((data)=>{      
      return data;
  }).then((text)=>{
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
    console.log("Ehhh");
    document.getElementById('choose').style.display = "initial";
    document.getElementById('music').style.display = "initial";
    document.getElementById('chords').style.display = "initial";
    document.getElementById('play').style.display = "initial";
    console.log(text.chord_types);
    init_some(text.chord_types);
  }).catch(e=>{
    console.log(e);
  });
}

function fetchAndDisplayGuitar(simplified, showNotes){
  if(simplified) {
    var postPath = `http://127.0.0.1:5000/music_simple`;
  }
  else {
    var postPath = `http://127.0.0.1:5000/music`;
  }
  postData(postPath, {input_file: localStorage.getItem("filePath")}).then((data)=>{      
      return data;
  }).then((text)=>{
    drawTabstaves(text, showNotes, true);
    drawVexTabChordsCheetSheet(text);
    unhideMusicInfoSections();
  }).catch(e=>{
    console.log(e);
  });
}

function drawTabstaves(text, showNotes, showTablature) {
    tab.reset();
    artist.reset();
    for (let i = 0; i < text.notes.length; i++) {
      if(i==0) {
        tab.parse(`tabstave notation=${showNotes} tablature=${showTablature} key=${text.key} time=${text.metrum}\nnotes ${text.notes[i]}`);
      }
      else {
        tab.parse(`tabstave notation=${showNotes} tablature=${showTablature} key=${text.key} \nnotes ${text.notes[i]}`);
      }
    }
    artist.render(renderer);
}

function unhideMusicInfoSections() {
  document.getElementById('choose').style.display = "initial";
  document.getElementById('music').style.display = "initial";
  document.getElementById('chords').style.display = "initial";
  document.getElementById('play').style.display = "initial";
}

function hideMusicInfoSections() {
  document.getElementById('choose').style.display = "none";
  document.getElementById('music').style.display = "none";
  document.getElementById('chords').style.display = "none";
  document.getElementById('play').style.display = "none";
}

function drawVexTabChordsCheetSheet(text) {
  init_some(text.chord_types);
}

hideMusicInfoSections();

const VF = vextab.Vex.Flow
const renderer = new VF.Renderer($('#boo')[0],
	VF.Renderer.Backends.SVG);
// Initialize VexTab artist and parser.
const artist = new vextab.Artist(10, 10, 750, { scale: 0.8 });
const tab = new vextab.VexTab(artist);