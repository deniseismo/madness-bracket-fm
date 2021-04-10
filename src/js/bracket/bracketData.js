import { shuffleArray } from "../misc/utilities.js";
import { stopMusic } from "../music/music.js";
import { addTooltipToCell } from "../cell/cellToolTips.js";
/*
Creates a special data structure to hold all the info about cells.
BracketData consists of left side of the bracket, right one, and the finale. 
*/
export class BracketData {
  constructor() {
    // each side (and the finale) is a dict of dicts
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
// resets current bracket to the initial state (basically resets all cells except for the first round)
export function resetBracket(bracket) {
  // reset the final round
  ["left", "right", "winner"].forEach((side) =>
    bracket.final[side].resetCell()
  );
  const numberOfRounds = Object.keys(bracket.left).length;
  for (let i = 0; i < numberOfRounds; i++) {
    const numberOfCells = Object.keys(bracket.left[i]).length;
    for (let j = 0; j < numberOfCells; j++) {
      // revert the first round back to normal
      if (i === 0) {
        ["left", "right"].forEach((side) => {
          // make cells from the first round advanceable and active again
          bracket[side][i][j].makeAdvanceable();
          bracket[side][i][j].activate();
        });
        // reset the rest of the rounds
      } else {
        // reset the cell if it's not the first round
        ["left", "right"].forEach((side) => bracket[side][i][j].resetCell());
        console.log(i);
      }
    }
  }
  // reset trophy icon back to normal
  const trophyIcon = document.querySelector(".trophy-icon");
  trophyIcon.classList.remove("trophy-icon_active");
}

// resets & then shuffles songs in the bracket
export function shuffleBracket(bracket, options) {
  // stop music if there's any playing
  stopMusic();
  // reset bracket first
  resetBracket(bracket);
  // take current bracket tracks data
  let tracks = options.getCurrentTracks();
  // shuffle tracks
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
      const albumColors = tracks[side][i]["album_colors"];
      const textColor = tracks[side][i]["text_color"];
      const previewURL = tracks[side][i]["spotify_preview_url"];
      // set preview url and the play button if a song has a preview url
      if (previewURL) {
        bracket[side][0][i].setPreviewURL(previewURL);
        bracket[side][0][i].addPlayButton();
      } else {
        // remove play button otherwise
        bracket[side][0][i].removePlayButton();
      }
      console.log(artistName);
      // set all the track data
      bracket[side][0][i].setCurrentSong(trackTitle);
      bracket[side][0][i].setArtistName(artistName);
      bracket[side][0][i].setTextColor(textColor);
      bracket[side][0][i].setAlbumColors(albumColors);
      bracket[side][0][i].setElementText();
      bracket[side][0][i].applyColors();
      if (options.getCurrentBracketType() != "artist") {
        addTooltipToCell(bracket[side][0][i], artistName, side);
      }
    });
  }
}
