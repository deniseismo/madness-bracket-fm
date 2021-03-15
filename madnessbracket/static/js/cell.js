export class Cell {
  constructor(roundIndex, cellIndex, element) {
    this.roundIndex = roundIndex;
    this.callIndex = cellIndex;
    this.element = element; // this cell's DOM element
    this.nextCell = null; // next (further up the bracket, next round) Cell object
    this.song = {
      songName: null,
      artistName: null,
      previewURL: null,
    };
    this.opponent = null; // opponent's Cell object
    this.advanceable = false; // a property of being advanceable further up the bracket
    this.active = false;
    this.albumColors = null;
    this.textColor = "white";
  }
  // sets the next cell object to the given one (next cell is the one this cell can advance to)
  setNextCell(nextCell) {
    this.nextCell = nextCell;
  }
  // gets the next cell
  getNextCell() {
    return this.nextCell;
  }
  // sets the opponent (the cell object)
  setOpponent(opponentCell) {
    this.opponent = opponentCell;
  }
  getOpponent() {
    return this.opponent;
  }
  setCurrentSong(song) {
    this.song["songName"] = song;
  }
  getCurrentSong() {
    return this.song["songName"];
  }
  setArtistName(artistName) {
    this.song["artistName"] = artistName;
  }
  getArtistName() {
    return this.song["artistName"];
  }
  setPreviewURL(url) {
    this.song["previewURL"] = url;
  }
  getPreviewURL() {
    return this.song["previewURL"];
  }
  setSongObject(songObject) {
    this.song = songObject;
  }
  getSongObject() {
    return this.song;
  }
  setAlbumColors(albumColors) {
    console.log("setting album colors");
    this.albumColors = albumColors;
  }
  getAlbumColors() {
    return this.albumColors;
  }
  setTextColor(textColor) {
    this.textColor = textColor;
  }
  getTextColor() {
    return this.textColor;
  }
  applyColors() {
    console.log("applying colors");
    if (this.albumColors) {
      const dominantColor = this.albumColors[0];
      const secondaryColor = this.albumColors[1];
      const tertiaryColor = this.albumColors[2];
      console.log(dominantColor, secondaryColor);
      this.element.style.background = `linear-gradient(to right, ${dominantColor}, ${secondaryColor}`;
      this.element.style.color = this.getTextColor();
    }

    //this.element.style.background = `linear-gradient(47deg, ${dominantColor} 0%, ${secondaryColor} 85%)`;
    //this.element.style.background = `linear-gradient(90deg, ${dominantColor} 0%, ${secondaryColor} 50%, ${tertiaryColor} 100%)`;

    // `linear-gradient(47deg, ${dominantColor} 0%, ${secondaryColor} 85%);`;
    // linear-gradient(47deg, rgba(92,91,78,1) 0%, rgba(229,171,102,1) 60%, rgba(229,171,102,1) 85%);
  }
  // set DOMelement's contents
  setElementText(textContent = null) {
    const songTitleElement = this.element.querySelector(".song-title");
    if (textContent) {
      // this.element.textContent = textContent;
      songTitleElement.textContent = textContent;
    } else {
      // this.element.textContent = this.getCurrentSong();
      // this.element.title = this.getArtistName();
      songTitleElement.textContent = this.getCurrentSong();
      songTitleElement.title = this.getArtistName();
    }
    console.log("setting element text");
  }
  copyAllQualities(cellToCopyFrom) {
    this.setSongObject(cellToCopyFrom.getSongObject());
    this.setAlbumColors(cellToCopyFrom.getAlbumColors());
    this.setTextColor(cellToCopyFrom.getTextColor());
    this.setElementText();
    this.applyColors();
  }
  // advance song further up the bracket (win over its opponent in a matchup and go to the next round)
  advance() {
    console.log("advance method activated");
    // check if this cell can be advanced
    if (this.isAdvanceable()) {
      // make current cell unadvanceable
      this.makeUnadvanceable();
      // deactivate current cell
      this.deactivate();
      // check if this cell has an opponent
      if (this.getOpponent()) {
        // disable opponent
        this.getOpponent().makeUnadvanceable();
        // deactivate opponent
        this.getOpponent().deactivate();
        // add class 'cell_loser'
        this.getOpponent().element.classList.add("cell_loser");
      }
      // activate the next cell
      this.nextCell.activate();
      this.nextCell.element.classList.remove("cell_empty");

      // this.nextCell.setCurrentSong(this.getCurrentSong());
      // this.nextCell.setElementText();
      this.nextCell.copyAllQualities(this);

      // check if the next cell has an opponent
      if (this.nextCell.getOpponent()) {
        // if the next cell already has an opponent ready, make them both advanceable
        if (this.nextCell.getOpponent().active) {
          this.nextCell.makeAdvanceable();
          this.nextCell.getOpponent().makeAdvanceable();
        }
      }
    }
  }
  // makes the current cell being advanceable — that is it can be advanced further up the bracket
  makeAdvanceable() {
    this.advanceable = true;
  }
  // this cell can NO LONGER be advanced further up
  makeUnadvanceable() {
    this.advanceable = false;
  }
  // can this cell be advanced
  isAdvanceable() {
    return this.advanceable;
  }
  // is this cell the 'head' of its chain — is it the farthest active cell in the chain
  activate() {
    this.active = true;
    this.element.classList.add("cell_head");
  }
  // this cell is no longer the 'head' of its chain
  deactivate() {
    this.active = false;
    this.element.classList.remove("cell_head");
  }
}
