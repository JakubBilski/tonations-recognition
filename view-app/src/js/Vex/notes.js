let responseCached = "";
let simplifiedResponseCached = "";

function fetchAndDisplayGuitar(simplified, showNotes){
  if(simplified) {
    if(simplifiedResponseCached === "") {
      var postPath = `http://127.0.0.1:5000/music_simple`;
      postJsonData(postPath, {input_file: filePath}).then((text) => {
        simplifiedResponseCached = text;
        drawEverything(simplifiedResponseCached, showNotes);
      });
    }
    else {
      drawEverything(simplifiedResponseCached, showNotes);
    }
  }
  else {
    if(responseCached === "") {
      var postPath = `http://127.0.0.1:5000/music`;
      postJsonData(postPath, {input_file: filePath}).then((text) => {
        responseCached = text;
        drawEverything(responseCached, showNotes);
      });
    }
    else {
      drawEverything(responseCached, showNotes);
    }
  }
}

function drawEverything(vextabInput, showNotes) {
  drawTabstaves(vextabInput, showNotes, true);
  drawVexTabChordsCheatSheet(vextabInput);
  unhideMusicInfoSections();
  updateWithChordsSoundClipContainer(vextabInput.preview_file);
}

function clearCache() {
  responseCached = "";
  simplifiedResponseCached = "";
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
  document.getElementById('arrow_button').style.display = "block";
}

function hideMusicInfoSections() {
  chooseSectionHeight = document.getElementById('choose_section').style.height;
  document.getElementById('choose_section').style.height = "0px";
  document.getElementById('choose_section').style.overflowY = "hidden"; 
  document.getElementById('music_section').style.display = "none";
  document.getElementById('chords_section').style.display = "none";
  document.getElementById('arrow_button').style.display = "none";
  document.getElementById('check').style.display = "none";
}

function drawVexTabChordsCheatSheet(text) {
  draw_chords(text.chord_types);
}

function updateWithChordsSoundClipContainer(audioURL) {
  if (withChordsSoundClipContainer.lastChild) {
    withChordsSoundClipContainer.removeChild(withChordsSoundClipContainer.lastChild);
  }
  const clipContainer = document.createElement('article');
  const audio = document.createElement('audio');
  clipContainer.classList.add('clip');
  audio.setAttribute('controls', '');
  clipContainer.appendChild(audio);
  withChordsSoundClipContainer.appendChild(clipContainer);
  audio.src = audioURL;
  audio.load();
}

hideMusicInfoSections();

const VF = vextab.Vex.Flow
const renderer = new VF.Renderer($('#boo')[0], VF.Renderer.Backends.SVG);
const artist = new vextab.Artist(10, 10, 750, { scale: 0.8 });
const tab = new vextab.VexTab(artist);