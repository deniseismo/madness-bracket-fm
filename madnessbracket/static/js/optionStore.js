// a storage for bracket options
export class optionStore {
  constructor() {
    // bracket type: artist/charts
    this.currentBracketType = null;
    // max bracket size: max number of tracks (4, 8, 16, 32)
    this.trackLimit = 16;
    // artist's name as per user's input
    this.inputValue = null;
    this.tracks = null;
  }
  // sets the current bracket type: artist or charts
  setCurrentBracketType(bracketType) {
    this.currentBracketType = bracketType;
  }
  // gets the current bracket type
  getCurrentBracketType() {
    return this.currentBracketType;
  }
  // sets max number of tracks in a bracket
  setBracketMaxSize(trackLimit) {
    this.trackLimit = trackLimit;
  }
  // gets max number of tracks in a bracket
  getBracketMaxSize() {
    return this.trackLimit;
  }
  // saves user's input
  setInputValue(inputValue) {
    this.inputValue = inputValue;
  }
  // gets user's input
  getInputValue() {
    return this.inputValue;
  }
  setCurrentTracks(tracks) {
    this.tracks = tracks;
  }
  getCurrentTracks() {
    return this.tracks;
  }
}
