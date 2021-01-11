let responseCached = "";
let simplifiedResponseCached = "";

function fetchAndDisplayGuitar(simplified, showNotes){
  if(simplified) {
    hideMusicInfoSections();
    unhideLoadingSection();
    if(simplifiedResponseCached === "") {
      var postPath = `http://127.0.0.1:5000/music_simple`;
      postJsonData(postPath, {input_file: filePath}).then((response) => {
        if (!response.ok) {
          throw new Error('Error in post simplified');
        }
        else {
          return response.json();
        }
      }).then((text) => {
        simplifiedResponseCached = text;
        drawEverything(simplifiedResponseCached, showNotes);
        hideLoadingSection();
        unhideMusicInfoSections();
      }).catch(error => {
        hideLoadingSection();
        unhideInvalidFileSection();
      });
    }
    else {
      drawEverything(simplifiedResponseCached, showNotes);
      hideLoadingSection();
      unhideMusicInfoSections();
    }
  }
  else {
    hideMusicInfoSections();
    unhideLoadingSection();
    if(responseCached === "") {
      hideChoosePanel();
      var postPath = `http://127.0.0.1:5000/music`;
      postJsonData(postPath, {input_file: filePath}).then((response) => {
        if (!response.ok) {
          throw new Error('Error in post');
        }
        else {
          return response.json();
        }
      }).then((text) => {
        responseCached = text;
        drawEverything(responseCached, showNotes);
        unhideChoosePanel();
        unhideMusicInfoSections();
        hideLoadingSection();
      }).catch(error => {
        hideLoadingSection();
        unhideInvalidFileSection();
    });
    }
    else {
      drawEverything(responseCached, showNotes);
      unhideMusicInfoSections();
      hideLoadingSection();
    }
  }
}

function drawEverything(vextabInput, showNotes) {
  drawTabstaves(vextabInput, showNotes, true);
  drawVexTabChordsCheatSheet(vextabInput);
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

function unhideChoosePanel() {
  document.getElementById('choose_section').style.height = chooseSectionHeight;
  document.getElementById('choose_section').style.overflowY = "auto";
}

function hideChoosePanel() {
  if(document.getElementById('choose_section').style.height != "0px") {
    chooseSectionHeight = document.getElementById('choose_section').style.height;
    document.getElementById('choose_section').style.height = "0px";
  }
}

function unhideMusicInfoSections() {
  document.getElementById('music_section').style.display = "block";
  document.getElementById('chords_section').style.display = "block";
  document.getElementById('arrow_button').style.display = "block";
}

function hideMusicInfoSections() {
  document.getElementById('choose_section').style.overflowY = "hidden"; 
  document.getElementById('music_section').style.display = "none";
  document.getElementById('chords_section').style.display = "none";
  document.getElementById('arrow_button').style.display = "none";
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

hideChoosePanel();
hideMusicInfoSections();

const VF = vextab.Vex.Flow
const renderer = new VF.Renderer($('#boo')[0], VF.Renderer.Backends.SVG);
const artist = new vextab.Artist(10, 10, 750, { scale: 0.8 });
const tab = new vextab.VexTab(artist);