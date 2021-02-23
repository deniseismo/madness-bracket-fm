import { shuffleArray } from "./utilities.js";
export class BracketData {
  constructor() {
    this.left = {};
    this.right = {};
    this.final = {};
  }
  setStructure(tracksLength) {
    const numberOfRounds = Math.log2(tracksLength / 2) * 2;
    let tracksPerRound = tracksLength / 2;
    for (let i = 0; i < numberOfRounds / 2; i++) {
      this.left[i] = {};
      this.right[i] = {};
      for (let j = 0; j < tracksPerRound; j++) {
        this.left[i][j] = null;
        this.right[i][j] = null;
      }
      tracksPerRound /= 2;
    }
    this.final["left"] = null;
    this.final["right"] = null;
    this.final["winner"] = null;
  }
}

export function traverseAllCells(bracket) {
  const numberOfRounds = Object.keys(bracket.left).length;
  console.log("numberofRounds" + numberOfRounds);
  // traversing through the rounds
  for (let i = 0; i < numberOfRounds; i++) {
    const numberOfCells = Object.keys(bracket.left[i]).length;
    // traversing through cells processing 2 at a time, step = 2 as well
    for (let j = 0; j < numberOfCells; j += 2) {
      // in a pair of cells set each other as opponents
      ["left", "right"].forEach((side) => {
        bracket[side][i][j].setOpponent(bracket[side][i][j + 1]);
        bracket[side][i][j + 1].setOpponent(bracket[side][i][j]);
      });
      // check if there's a next round
      if (bracket.left.hasOwnProperty(i + 1)) {
        // set the appropriate's next round's cell to be the 'nextCell' (where they should advance to)
        const nextCellIndex = Math.floor(j / 2);
        ["left", "right"].forEach((side) => {
          bracket[side][i][j].setNextCell(bracket[side][i + 1][nextCellIndex]);
          bracket[side][i][j + 1].setNextCell(
            bracket[side][i + 1][nextCellIndex]
          );
        });
      }
      // no next round meaning it's finale time
      else {
        ["left", "right"].forEach((side) => {
          bracket[side][i][j].setNextCell(bracket.final[side]);
          bracket[side][i][j + 1].setNextCell(bracket.final[side]);
        });
      }
    }
    ["left", "right"].forEach((side) => {
      bracket.final[side].setNextCell(bracket.final["winner"]);
    });
    bracket.final["left"].setOpponent(bracket.final["right"]);
    bracket.final["right"].setOpponent(bracket.final["left"]);
  }
  console.log("traversing");
}

export function resetBracket(bracket) {
  // supplementary function to reset a single cell's properties
  function resetCell(cell) {
    cell.setCurrentSong("");
    cell.setElementText();
    cell.makeUnadvanceable();
    cell.deactivate();
  }
  // reset the final round
  ["left", "right", "winner"].forEach((side) =>
    resetCell(bracket.final[side])
  );
  const numberOfRounds = Object.keys(bracket.left).length;
  for (let i = 0; i < numberOfRounds; i++) {
    const numberOfCells = Object.keys(bracket.left[i]).length;
    for (let j = 0; j < numberOfCells; j++) {
      // revert the first round back to normal
      if (i === 0) {
        ["left", "right"].forEach((side) => {
          bracket[side][i][j].makeAdvanceable();
          bracket[side][i][j].activate();
        });
      // reset the rest of the rounds
      } else {
        ["left", "right"].forEach((side) => resetCell(bracket[side][i][j]));
      }
    }
  }
}

// resets & then shuffles songs in the bracket
export function shuffleBracket(bracket, tracksData) {
  // reset first
  resetBracket(bracket);
  // take out the array of all the tracks dicts
  let tracks = tracksData['tracks'];
  shuffleArray(tracks);
  tracks = {
    left: tracks.slice(0, tracks.length / 2),
    right: tracks.slice(tracks.length / 2),
  };
  console.log('shuffled array now is ', tracks);
  // the length of each side's first round
  const numberOfCells = Object.keys(bracket.left[0]).length;
  for (let i = 0; i < numberOfCells; i++) {
    ['left', 'right'].forEach(side => {
      const trackTitle = tracks[side][i]['track_title'];
      bracket[side][0][i].setCurrentSong(trackTitle);
      bracket[side][0][i].setElementText();
    })
  }
}