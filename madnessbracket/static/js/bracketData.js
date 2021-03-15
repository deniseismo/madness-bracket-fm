import { shuffleArray } from "./utilities.js";

//creates a special data structure to hold all the info about cells
export class BracketData {
  constructor() {
    // it has two sides (left and right) and the final round
    this.left = {};
    this.right = {};
    this.final = {};
  }
  setStructure(tracksLength) {
    // given the number of tracks total we can figure out the number of rounds in a bracket
    const numberOfRounds = Math.log2(tracksLength / 2) * 2;
    // starting with (number of tracks / 2) as the bracket has 2 sides
    let tracksPerRound = tracksLength / 2;
    for (let i = 0; i < numberOfRounds / 2; i++) {
      // we create a sort of dict for each round at [i] loc
      this.left[i] = {};
      this.right[i] = {};
      // each round has tracksPerRound 'seats' for cells at [j] loc
      for (let j = 0; j < tracksPerRound; j++) {
        this.left[i][j] = null;
        this.right[i][j] = null;
      }
      // each round we divide the number of tracks per round by 2 → bracket progresses to the finals
      tracksPerRound /= 2;
    }
    // init final round cell 'seats'
    this.final["left"] = null;
    this.final["right"] = null;
    this.final["winner"] = null;
  }
}

/*
make data structure meaningful: each cell has an opponent (a cell in a matchup)
and the next cell where it can progress to. (makes every cell a part of a corresponding singly-linked list)
*/
export function traverseAllCells(bracket) {
  const numberOfRounds = Object.keys(bracket.left).length;
  console.log("numberOfRounds" + numberOfRounds);
  // traversing through the rounds
  for (let i = 0; i < numberOfRounds; i++) {
    const numberOfCells = Object.keys(bracket.left[i]).length;
    // traversing through cells processing 2 at a time, step = 2 as well
    for (let j = 0; j < numberOfCells; j += 2) {
      // configure matchup: set each cell in a pair of nearby cells to be an opponent to each other
      ["left", "right"].forEach((side) => {
        bracket[side][i][j].setOpponent(bracket[side][i][j + 1]);
        bracket[side][i][j + 1].setOpponent(bracket[side][i][j]);
      });
      // check if there's a next round
      if (bracket.left.hasOwnProperty(i + 1)) {
        // set the appropriate cell from the next round to be this cell's 'nextCell'
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
          // next cells for these cells will be final two cells
          bracket[side][i][j].setNextCell(bracket.final[side]);
          bracket[side][i][j + 1].setNextCell(bracket.final[side]);
        });
      }
    }
    ["left", "right"].forEach((side) => {
      // final pair of cells has the ultimate 'nextCell' — the winner cell
      bracket.final[side].setNextCell(bracket.final["winner"]);
    });
    // configure matchup for two finalists
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
  ["left", "right", "winner"].forEach((side) => resetCell(bracket.final[side]));
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
  let tracks = tracksData["tracks"];
  shuffleArray(tracks);
  tracks = {
    left: tracks.slice(0, tracks.length / 2),
    right: tracks.slice(tracks.length / 2),
  };
  console.log("shuffled array now is ", tracks);
  // the length of each side's first round
  const numberOfCells = Object.keys(bracket.left[0]).length;
  for (let i = 0; i < numberOfCells; i++) {
    ["left", "right"].forEach((side) => {
      const trackTitle = tracks[side][i]["track_title"];
      const artistName = tracks[side][i]["artist_name"];
      console.log(artistName);
      bracket[side][0][i].setCurrentSong(trackTitle);
      bracket[side][0][i].setArtistName(artistName);
      bracket[side][0][i].setElementText();
    });
  }
}
