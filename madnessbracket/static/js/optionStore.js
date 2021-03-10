export class optionStore {
  constructor() {
    this.currentBracketType = null;
    this.trackLimit = 16;
    this.inputValue = null;
  }
  setCurrentBracketType(bracketType) {
    this.currentBracketType = bracketType;
  }
  getCurrentBracketType() {
    return this.currentBracketType;
  }
  setBracketMaxSize(trackLimit) {
    this.trackLimit = trackLimit;
  }
  getBracketMaxSize() {
    return this.trackLimit;
  }
  setInputValue(inputValue) {
    this.inputValue = inputValue;
  }
  getInputValue() {
    return this.inputValue;
  }
}
