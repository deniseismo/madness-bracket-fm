export class Cell {
    constructor(roundIndex, cellIndex, element) {
      this.roundIndex = roundIndex;
      this.callIndex = cellIndex;
      this.element = element;  // this cell's DOM element
      this.nextCell = null; // next (further up the bracket, next round) Cell object
      this.song = {
        "songName": null,
        "artistName": null
      }
      this.opponent = null; // opponent's Cell object
      this.advanceable = false; // a property of being advanceable further up the bracket
      this.active = false;
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
      console.log('setting opponen to ' + opponentCell)
    }
    getOpponent() {
      return this.opponent;
    }
    setCurrentSong(song) {
      this.song['songName'] = song;
    }
    getCurrentSong() {
      return this.song['songName'];
    }
    // set DOMelement's contents
    setElementText(textContent = null) {
      if (textContent) {
        this.element.textContent = textContent;
      }
      else {
        this.element.textContent = this.getCurrentSong();
      }
      console.log('setting element text')
    }
    advance() {
      console.log('advance method activated');
      if (this.isAdvanceable()) {
        this.makeunAdvanceable();
        this.deactivate();
        if (this.getOpponent()) {
          this.getOpponent().makeunAdvanceable();
          this.getOpponent().deactivate();
        }
        this.nextCell.setCurrentSong(this.getCurrentSong());
        this.nextCell.setElementText();
        this.nextCell.activate();
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
    makeunAdvanceable() {
      this.advanceable = false;
    }
     // can this cell be advanced
    isAdvanceable() {
      return this.advanceable;
    }
    // is this cell the 'head' of its chain — is it the farthest active cell in the chain
    activate() {
      this.active = true;
    }
    // this cell is no longer the 'head' of its chain
    deactivate() {
      this.active = false;
    }
  }