import { Cell } from "./cell.js";
import { bracket } from "./main.js";
import { traverseAllCells } from "./bracketData.js";
import { removeAllChildNodes } from "./utilities.js";

export function createBracketStructure(tracksData) {
  const container = document.querySelector(".container");
  removeAllChildNodes(container);
  const tracksLength = tracksData["tracks"].length;
  bracket.setStructure(tracksLength);
  const tracks = {
    left: tracksData["tracks"].slice(0, tracksLength / 2),
    right: tracksData["tracks"].slice(tracksLength / 2),
  };
  // calculate the number of rounds (sans final round)
  const numberOfRounds = Math.log2(tracksLength / 2) * 2;
  // set a variable for an amount of tracks per round
  let tracksPerRound = tracksLength / 2;
  const mainContainer = document.querySelector(".container");
  // create and append the main bracket div to 'container' container
  const tournamentBracket = document.createElement("div");
  tournamentBracket.classList.add("tournament-bracket");
  mainContainer.appendChild(tournamentBracket);

  for (let i = 0; i < numberOfRounds; i++) {
    const round = document.createElement("div");
    round.classList.add("round");
    if (i < numberOfRounds / 2) {
      var roundIndex = i;
      var side = "left";
    } else {
      var roundIndex = numberOfRounds - i - 1;
      var side = "right";
    }
    // add an appropriate class to the round specifying its index as well
    const roundClassName = `${side}-${roundIndex}`;
    round.classList.add(roundClassName);

    // add a cell to the 'round' div 'tracksPerRound' times
    for (let j = 0; j < tracksPerRound; j++) {
      const cell = document.createElement("div");
      const cellClassName = `${side}-${roundIndex}-${j}`;
      const cellObject = new Cell(roundIndex, j, cell);
      cell.addEventListener("click", cellObject.advance.bind(cellObject));
      cell.classList.add("cell", cellClassName);

      // distributes all the song across the first round cells on both sides of the bracket
      if (roundIndex === 0) {
        const trackTitle = tracks[side][j]["track_title"];
        const artistName = tracks[side][j]["artist_name"];
        const albumColors = tracks[side][j]["album_colors"];
        console.log(trackTitle, artistName);
        cellObject.setCurrentSong(trackTitle);
        cellObject.setArtistName(artistName);
        cellObject.setElementText();
        cellObject.makeAdvanceable();
        cellObject.activate();

        cellObject.setAlbumColors(albumColors);
        cellObject.applyColors();
      } else {
        cell.classList.add("cell_empty");
      }
      // fill the bracketData object will all the cell objects
      bracket[side][roundIndex][j] = cellObject;
      round.appendChild(cell);
    }

    // check if it's left or right side
    if (i < numberOfRounds / 2 - 1) {
      // half the number of tracks per round
      tracksPerRound /= 2;
    } else if (i > numberOfRounds / 2 - 1) {
      // multiply number of tracks per round by 2
      tracksPerRound *= 2;
    }
    tournamentBracket.appendChild(round);

    if (i === numberOfRounds / 2 - 1) {
      const finalRound = createFinalRound();
      tournamentBracket.appendChild(finalRound);
    }
  }
  traverseAllCells(bracket);
}

function createFinalRound() {
  const finalRound = document.createElement("div");
  finalRound.classList.add("round", "final-round");

  const winnerContainer = document.createElement("div");
  winnerContainer.classList.add("winner-container");
  const winnerCell = document.createElement("div");
  winnerCell.classList.add("cell", "winner-cell", "cell_empty");
  const winnerCellObject = new Cell(-2, 0, winnerCell);
  winnerCell.addEventListener(
    "click",
    winnerCellObject.advance.bind(winnerCellObject)
  );
  bracket.final["winner"] = winnerCellObject;
  winnerContainer.appendChild(winnerCell);

  finalRound.appendChild(winnerContainer);

  const finalists = document.createElement("div");
  finalists.classList.add("finalists");
  const leftCell = document.createElement("div");
  leftCell.classList.add("cell", "left-final-cell", "final-cell", "cell_empty");
  const leftCellObject = new Cell(-1, 0, leftCell);
  leftCell.addEventListener(
    "click",
    leftCellObject.advance.bind(leftCellObject)
  );
  bracket.final["left"] = leftCellObject;
  const rightCell = document.createElement("div");
  rightCell.classList.add(
    "cell",
    "right-final-cell",
    "final-cell",
    "cell_empty"
  );
  const rightCellObject = new Cell(-1, 1, rightCell);
  rightCell.addEventListener(
    "click",
    rightCellObject.advance.bind(rightCellObject)
  );
  bracket.final["right"] = rightCellObject;
  finalists.appendChild(leftCell);
  finalists.appendChild(rightCell);

  finalRound.appendChild(finalists);
  return finalRound;
}
