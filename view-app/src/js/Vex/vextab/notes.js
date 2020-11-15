const data = `
  tabstave notation=true key=A time=4/4

  notes :q =|: (5/2.5/3.7/4) :8 7-5h6/3 ^3^ 5h6-7/5 ^3^ :q 7V/4 |
  notes :8 t12p7/4 s5s3/4 :8 3s:16:5-7/5 :q p5/4
  text :w, |#segno, ,|, :hd, , #tr
`

const VF = vextab.Vex.Flow

const renderer = new VF.Renderer($('#boo')[0],
	VF.Renderer.Backends.SVG);

// Initialize VexTab artist and parser.
const artist = new vextab.Artist(10, 10, 750, { scale: 0.8 });
const tab = new vextab.VexTab(artist);

tab.parse(data);
artist.render(renderer);
