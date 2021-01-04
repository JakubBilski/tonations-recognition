function fetchAndDisplayGuitar(simplified, showNotes){
  if(simplified) {
    var postPath = `http://127.0.0.1:5000/music_simple`;
  }
  else {
    var postPath = `http://127.0.0.1:5000/music`;
  }
  postJsonData(postPath, {input_file: filePath}).then((data)=>{      
      return data;
  }).then((text)=>{
    drawTabstaves(text, showNotes, true);
    drawVexTabChordsCheatSheet(text);
    unhideMusicInfoSections();
    updateWithChordsSoundClipContainer();
  }).catch(e=>{
    console.log(e);
  });
}

function drawTabstaves(text, showNotes, showTablature) {
    tab.reset();
    artist.reset();
    for (let i = 0; i < text.notes.length; i++) {
      if(i==0) {
        tab.parse(`tabstave notation=${showNotes}
         tablature=${showTablature}
         key=${text.key}
         time=${text.metrum}
         \nnotes ${text.notes[i]}
         \ntext ${text.chords[i]}`
         );
      }
      else {
        tab.parse(`tabstave notation=${showNotes}
         tablature=${showTablature} 
         key=${text.key} 
         \nnotes ${text.notes[i]}
         \ntext ${text.chords[i]}`
         );
      }
    }
    artist.render(renderer);
}

function unhideMusicInfoSections() {
  document.getElementById('choose_section').style.height = chooseSectionHeight;
  document.getElementById('choose_section').style.overflowY = "auto";
  document.getElementById('music_section').style.display = "block";
  document.getElementById('chords_section').style.display = "block";
}

function hideMusicInfoSections() {
  chooseSectionHeight = document.getElementById('choose_section').style.height;
  document.getElementById('choose_section').style.height = "0px";
  document.getElementById('choose_section').style.overflowY = "hidden"; 
  document.getElementById('music_section').style.display = "none";
  document.getElementById('chords_section').style.display = "none";
}

function drawVexTabChordsCheatSheet(text) {
  draw_chords(text.chord_types);
}

function updateWithChordsSoundClipContainer() {
  if (withChordsSoundClipContainer.lastChild) {
    withChordsSoundClipContainer.removeChild(withChordsSoundClipContainer.lastChild);
  }
  const clipContainer = document.createElement('article');
  const audio = document.createElement('audio');
  clipContainer.classList.add('clip');
  audio.setAttribute('controls', '');
  clipContainer.appendChild(audio);
  withChordsSoundClipContainer.appendChild(clipContainer);
  const audioURL = "../../data/temp/output.ogg";
  audio.src = audioURL;
}

hideMusicInfoSections();

const VF = vextab.Vex.Flow
const renderer = new VF.Renderer($('#boo')[0], VF.Renderer.Backends.SVG);
const artist = new vextab.Artist(10, 10, 750, { scale: 0.8 });
const tab = new vextab.VexTab(artist);