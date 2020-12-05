

const chordChart = [
  {
    description:
      'Open chords',
    chords: [
      {
        name: 'CMaj',
        chord: [[1, 0], [2, 1, '1'], [3, 0], [4, 2, 2], [5, 3, 3]],
        position: 0,
        barres: []
      },
      {
        name: 'DMaj',
        chord: [
          [1, 2, 2],
          [2, 3, 3],
          [3, 2, '1'],
          [4, 0, 'D'],
          [5, 'x'],
          [6, 'x']
        ],
        position: 0,
        barres: []
      },
      {
        name: 'EMaj',
        chord: [
          [1, 0, 'E'],
          [2, 0],
          [3, 1, 1],
          [4, 2, 3],
          [5, 2, 2],
          [6, 0, 'E']
        ],
        position: 0,
        barres: []
      },
      {
        name: 'GMaj',
        chord: [
          [1, 3, 4],
          [2, 3, 3],
          [3, 0, 'G'],
          [4, 0],
          [5, 2, 1],
          [6, 3, 2]
        ],
        position: 0,
        barres: []
      },
      {
        name: 'AMaj',
        chord: [
          [1, 0],
          [2, 2, 3],
          [3, 2, 2],
          [4, 2, 1],
          [5, 0, 'A'],
          [6, 'x']
        ],
        position: 0,
        barres: []
      },
      {
        name: 'Dm',
        chord: [
          [1, 1, 1],
          [2, 3, 3],
          [3, 2, 2],
          [4, 0, 'D'],
          [5, 'x'],
          [6, 'x']
        ],
        position: 0,
        barres: []
      },
      {
        name: 'Em',
        chord: [
          [1, 0],
          [2, 0],
          [3, 0],
          [4, 2, 3],
          [5, 2, 2],
          [6, 0, 'E']
        ],
        position: 0,
        barres: []
      },
      {
        name: 'Am',
        chord: [
          [1, 0],
          [2, 1, 1],
          [3, 2, 3],
          [4, 2, 2],
          [5, 0, 'A'],
          [6, 'x']
        ],
        position: 0,
        barres: []
      },
      {
        name: 'C7',
        chord: [
          [1, 0],
          [2, 1, 1],
          [3, 3, 4],
          [4, 2, 2],
          [5, 3, 3],
          [6, 'x']
        ],
        position: 0,
        barres: []
      },
      {
        name: 'D7',
        chord: [
          [1, 2, 3],
          [2, 1, 1],
          [3, 2, 2],
          [4, 0, 'D'],
          [5, 'x'],
          [6, 'x']
        ],
        position: 0,
        barres: []
      },
      {
        name: 'E7',
        chord: [
          [1, 0],
          [2, 3, 4],
          [3, 1, 1],
          [4, 0],
          [5, 2, 2],
          [6, 0, 'E']
        ],
        position: 0,
        barres: []
      },
      {
        name: 'G7',
        chord: [[1, 1, 1], [2, 0], [3, 0], [4, 0], [5, 2, 2], [6, 3, 3]],
        position: 0,
        barres: []
      },
      {
        name: 'A7',
        chord: [
          [1, 0],
          [2, 2, 3],
          [3, 0],
          [4, 2, 2],
          [5, 0, 'A'],
          [6, 'x']
        ],
        position: 0,
        barres: []
      },
      {
        name: 'Dm7',
        chord: [[3, 2, 2], [4, 0], [5, 'x'], [6, 'x']],
        position: 0,
        barres: [{ fromString: 2, toString: 1, fret: 1 }]
      },
      {
        name: 'Em7',
        chord: [
          [1, 0],
          [2, 3, 4],
          [3, 0],
          [4, 0],
          [5, 2, 1],
          [6, 0, 'E']
        ],
        position: 0,
        barres: []
      },
      {
        name: 'Am7',
        chord: [
          [1, 0],
          [2, 1, 1],
          [3, 0],
          [4, 2, 2],
          [5, 0, 'A'],
          [6, 'x']
        ],
        position: 0,
        barres: []
      }
    ]
  }
];

const chords = [];

function createChordElement(chordStruct) {
  const chordbox = $('<div>').addClass('chord');
  const chordcanvas = $('<div>').addClass('chord');
  const chordname = $('<div>').addClass('chordname');

  chordbox.append(chordcanvas);
  chordbox.append(chordname);
  chordname.append(chordStruct.name);

  chords.push({
    el: chordcanvas[0],
    struct: chordStruct
  });

  return chordbox;
}

function createSectionElement(sectionStruct) {
  const section = $('<div>').addClass('section_chord');
  const sectionTitle = $('<div>').addClass('title');
  const sectionDesc = $('<div>').addClass('description');

  section.append(sectionTitle);
  section.append(sectionDesc);
  sectionTitle.append(sectionStruct.section);
  sectionDesc.append(sectionStruct.description);

  return section;
}

function createShapeChart(keys, container, shapes, shape,chordNames) {
  for (let i = 0; i < keys.length; i += 1) {
    const key = keys[i];
    for (let j = 0; j < shapes.length; j += 1) {
      var section=build(key, shape, shapes[j]);
      
      const chordElem = createChordElement(section);
      if(chordNames.includes(section.name)) {
        container.append(chordElem);
      }
    }
  }
}
var keys_EG = ['G'];
var shapes_EG = [
  'm E',
  'dim E',
  'm7 E'
];
var keys_E = ['F', 'F#', 'Gb', 'G#', 'Ab',  'A#', 'B', 'C'];
var keys_A = ['C#', 'Db', 'D#', 'Eb'];
var shapes_E = [
  'M E',
  'm E',
  '7 E',
  'dim E',
  'm7 E'
];
var shapes_A = [
  'M A',
  'm A',
  '7 A',
  'dim A',
  'm7 A'
];

function draw_chords(chordNames) {
  var container = $('#container-chords');
  container.empty();


  // Display preset chords (open chords)
  for (var i = 0; i < chordChart.length; ++i) {
      var section_struct = chordChart[i];
      var section = createSectionElement(section_struct);
  
      for (var j = 0; j < section_struct.chords.length; ++j) {
        if(chordNames.includes(section_struct.chords[j].name)) {
        section.append(createChordElement(section_struct.chords[j]));
        }
      }
  
      container.append(section);

  }
  createShapeChart(keys_E, container, shapes_E, 'E',chordNames);
  createShapeChart(keys_A, container, shapes_A, 'A',chordNames);  
  createShapeChart(keys_EG, container, shapes_EG, 'E',chordNames);
  chords.forEach(chord => {
    new ChordBox(chord.el, {
      width: 130,
      height: 150,
      defaultColor: '#444'
    }).draw(chord.struct);
  });
}