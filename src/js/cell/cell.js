import { getSVGIcon } from "../misc/svgGenerator.js";
import { playButtonSVGData, PlayButton } from "../music/playButton.js";
import { createElement } from "../misc/utilities.js";

// Cell is responsible for holding all the data about the song and the corresponding DOM element (the cell in the bracket)
export class Cell {
  constructor(roundIndex, cellIndex, element) {
    this.roundIndex = roundIndex;
    this.cellIndex = cellIndex;
    this.element = element; // this cell's DOM element
    this.nextCell = null; // next (further up the bracket, next round) Cell object
    this.song = {
      songName: null,
      artistName: null,
      previewURL: null,
    };
    this.opponent = null; // opponent's Cell object
    this.advanceable = false; // a quality of being advanceable further up the bracket
    this.active = false;
    this.albumColors = null;
    this.textColor = "white";
    this.trackID = null;
    this.loser = false;
    this.tooltip = null;
    this.defaultCellColor = "#26624c";
  }
  setTrackID(trackID) {
    this.trackID = trackID;
  }
  getTrackID() {
    return this.trackID;
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
  // gets the opponent (cell) of the current cell
  getOpponent() {
    return this.opponent;
  }
  // sets this cell's current song (song name/title)
  setCurrentSong(song) {
    this.song["songName"] = song;
  }
  // gets this cell's current song (song name/title)
  getCurrentSong() {
    return this.song["songName"];
  }
  // sets this cell's current artist (artist's name)
  setArtistName(artistName) {
    this.song["artistName"] = artistName;
  }
  // gets this cell's current artist (artist's name)
  getArtistName() {
    return this.song["artistName"];
  }
  // sets preview url for the song (Spotify's 30-second preview URL)
  setPreviewURL(url) {
    this.song["previewURL"] = url;
  }
  // gets preview url
  getPreviewURL() {
    return this.song["previewURL"];
  }
  // set all song properties at once (song title, artist's name, preview url)
  setSongObject(songObject) {
    this.song["songName"] = songObject["songName"];
    this.song["artistName"] = songObject["artistName"];
    this.song["previewURL"] = songObject["previewURL"];
  }
  // gets song properties (song title, artist's name, preview url)
  getSongObject() {
    return this.song;
  }
  // sets album colors (two dominant colors of the album cover art)
  setAlbumColors(albumColors) {
    console.log("setting album colors");
    this.albumColors = albumColors;
  }
  // gets album colors
  getAlbumColors() {
    return this.albumColors;
  }
  // sets text color
  setTextColor(textColor) {
    this.textColor = textColor;
  }
  // gets text color
  getTextColor() {
    return this.textColor;
  }
  // apply colors to the corresponding DOM element
  applyColors() {
    console.log("applying colors");
    // (if there are album colors)
    if (this.albumColors) {
      const dominantColor = this.albumColors[0];
      const secondaryColor = this.albumColors[1];
      // const tertiaryColor = this.albumColors[2];
      console.log(dominantColor, secondaryColor);
      this.element.style.background = `linear-gradient(to right, ${dominantColor}, ${secondaryColor}`;
      this.element.style.color = this.getTextColor();
    } else {
      this.element.style.color = this.defaultCellColor;
    }
  }
  // set DOM element contents
  setElementText(textContent = null) {
    console.log("setting element text");
    const songTitleElement = this.element.querySelector(".song-title");
    if (textContent) {
      songTitleElement.textContent = textContent;
    } else {
      console.log(songTitleElement);
      songTitleElement.textContent = this.getCurrentSong();
      songTitleElement.title = this.getArtistName();
      console.log("setting to ", songTitleElement.textContent);
    }
  }
  // copies all properties from the given cell object
  copyAllQualities(cellToCopyFrom) {
    this.setSongObject(cellToCopyFrom.getSongObject());
    this.setAlbumColors(cellToCopyFrom.getAlbumColors());
    this.setTextColor(cellToCopyFrom.getTextColor());
    this.setTrackID(cellToCopyFrom.getTrackID());
    this.setElementText();
    this.applyColors();
  }
  // resets cell
  resetCell() {
    console.log("resetting cell:", this);
    this.setTrackID(null);
    this.setCurrentSong("");
    this.setElementText();
    this.makeUnadvanceable();
    this.deactivate();
    this.resetStyleClasses();
  }
  resetStyleClasses() {
    ["cell_loser", "cell_winner"].forEach((className) => {
      this.element.classList.remove(className);
    });
    this.element.classList.add("cell_empty");
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
        // add class 'cell_loser' and a status 'loser'
        this.getOpponent().lose();
      }
      // activate the next cell
      this.nextCell.activate();
      this.nextCell.removeClassEmpty();

      // this.nextCell.setCurrentSong(this.getCurrentSong());
      // this.nextCell.setElementText();
      this.nextCell.copyAllQualities(this);
      console.log(this);
      console.log(this.nextCell);

      // check if the next cell has an opponent
      if (this.nextCell.getOpponent()) {
        // if the next cell already has an opponent ready, make them both advanceable
        if (this.nextCell.getOpponent().active) {
          this.nextCell.makeAdvanceable();
          this.nextCell.getOpponent().makeAdvanceable();
        }
      } else {
        // if next cell has no opponent — it's the winner's cell
        const trophyIcon = document.querySelector(".trophy-icon");
        trophyIcon.classList.add("trophy-icon_active");
      }
    }
  }
  removeClassEmpty() {
    this.element.classList.remove("cell_empty");
  }
  lose() {
    this.loser = true;
    this.element.classList.add("cell_loser");
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
  // adds play button the current cell's DOM element
  addPlayButton() {
    this.removePlayButton();
    const playIcon = getSVGIcon(playButtonSVGData["play"]);
    playIcon.classList.add("play-icon");
    const playButtonElement = createElement("button", [
      "play-button",
      "play-icon_standby",
    ]);
    playButtonElement.appendChild(playIcon);
    playButtonElement.dataset.status = "standby";
    const playButton = new PlayButton(
      playButtonElement,
      this.song["previewURL"]
    );
    playButtonElement.addEventListener("click", function (event) {
      event.preventDefault();
      event.stopPropagation();
      playButton.playPause();
    });
    this.element.appendChild(playButtonElement);
  }
  // removes play button
  removePlayButton() {
    const playButton = this.element.querySelector(".play-button");
    if (playButton) {
      playButton.remove();
    }
  }
  setTooltip(tooltip) {
    if (this.tooltip) {
      this.tooltip.destroy();
    }
    this.tooltip = tooltip;
  }
  getTooltip() {
    return this.tooltip;
  }
}
