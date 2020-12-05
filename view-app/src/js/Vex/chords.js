

const chordChart = [
  {
    description:
      'How to play chords',
    chords: [
      {
        name: 'C Major',
        chord: [[1, 0], [2, 1, '1'], [3, 0], [4, 2, 2], [5, 3, 3]],
        position: 0,
        barres: []
      },
      {
        name: 'D Major',
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
        name: 'E Major',
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
        name: 'G Major',
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
        name: 'A Major',
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
        name: 'D Minor',
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
        name: 'E Minor',
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
        name: 'A Minor',
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

// function createShapeChart(keys, container, shapes, shape) {
//   // for (let i = 0; i < keys.length; i += 1) {
//   //   const key = keys[i];
//   //   const section = createSectionElement({
//   //     section: `${key} Chords (${shape} Shape)`,
//   //     description: `${shape}-Shaped barre chords in the key of ${key}.`
//   //   });

//   //   for (let j = 0; j < shapes.length; j += 1) {
//   //     const chordElem = createChordElement(
//   //       build(key, shape, shapes[j])
//   //     );
//   //     section.append(chordElem);
//   //   }

//   //   container.append(section);
//   // }
// }
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

  chords.forEach(chord => {
    new ChordBox(chord.el, {
      width: 130,
      height: 150,
      defaultColor: '#444'
    }).draw(chord.struct);
  });
}