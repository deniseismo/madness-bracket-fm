import { Cell } from "../cell/cell.js";
import { traverseAllCells } from "./bracketData.js";
import { removeAllChildNodes, createElement } from "../misc/utilities.js";
import { getSVGIcon } from "../misc/svgGenerator.js";
import { displayBracketDescription } from "../visuals/description.js";
import { getDashboard } from "../dashboard/dashboardHandlers.js";
import { addTooltipToCell } from "../cell/cellToolTips.js";
import { trophySVGData } from "../visuals/winnerFX.js";
import { activateDashboardTooltips } from "../dashboard/dashboardTooltips.js";
import { fixSVGDimensions } from "../misc/svgGenerator.js";
import { bracketAnimation } from "../animation/bracketAnimation.js";

// create madness bracket
export function createBracketStructure(bracket, options) {
  const mainContainer = document.querySelector(".main");
  const tracksData = options.getCurrentTracks();
  const description = options.getDescription();
  removeAllChildNodes(mainContainer);
  displayBracketDescription(description);
  const tracksLength = tracksData.length;
  bracket.setStructure(tracksLength);
  const tracks = {
    left: tracksData.slice(0, tracksLength / 2),
    right: tracksData.slice(tracksLength / 2),
  };
  // calculate the number of rounds (sans final round)
  const numberOfRounds = Math.log2(tracksLength / 2) * 2;
  // set a variable for an amount of tracks per round
  let tracksPerRound = tracksLength / 2;
  // create and append the main bracket div to 'container' container
  const tournamentBracket = document.createElement("div");
  tournamentBracket.classList.add("tournament-bracket");
  mainContainer.appendChild(tournamentBracket);

  for (let i = 0; i < numberOfRounds; i++) {
    const round = document.createElement("div");
    round.classList.add("round");
    let roundIndex = i;
    let side = "left";
    if (i < numberOfRounds / 2) {
      roundIndex = i;
      side = "left";
    } else {
      roundIndex = numberOfRounds - i - 1;
      side = "right";
    }
    // add an appropriate class to the round specifying its index as well
    const roundClassName = `${side}-${roundIndex}`;
    round.classList.add(roundClassName, `round-${side}`);

    // add a cell to the 'round' div 'tracksPerRound' times
    for (let j = 0; j < tracksPerRound; j++) {
      const cellClassName = `${side}-${roundIndex}-${j}`;
      const cellClassNameTwo = `cell-${side}`;
      const cell = createElement("div", [
        "cell",
        cellClassName,
        cellClassNameTwo,
      ]);
      const songTitleElement = createElement("p", ["song-title"]);
      cell.appendChild(songTitleElement);
      const cellObject = new Cell(roundIndex, j, cell);
      cell.addEventListener("click", cellObject.advance.bind(cellObject));

      // distributes all the songs across the first round cells on both sides of the bracket
      if (roundIndex === 0) {
        cell.classList.add("cell-first");
        const previewURL = tracks[side][j]["spotify_preview_url"];
        if (previewURL) {
          cellObject.setPreviewURL(previewURL);
          cellObject.addPlayButton();
        }
        const trackTitle = tracks[side][j]["track_title"];
        const artistName = tracks[side][j]["artist_name"];
        const albumColors = tracks[side][j]["album_colors"];
        const textColor = tracks[side][j]["text_color"];
        cellObject.setCurrentSong(trackTitle);
        cellObject.setArtistName(artistName);
        cellObject.setElementText();
        cellObject.makeAdvanceable();
        cellObject.activate();

        cellObject.setTextColor(textColor);
        cellObject.setAlbumColors(albumColors);
        cellObject.applyColors();
        if (options.getCurrentBracketType() != "artist") {
          addTooltipToCell(cellObject, artistName, side);
        }
        if (side === "left") {
          cellObject.setTrackID(j);
        } else {
          cellObject.setTrackID(j + tracksLength / 2);
        }
      } else {
        cell.classList.add("cell-not-first");
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
      const finalRound = createFinalRound(bracket, options);
      tournamentBracket.appendChild(finalRound);
    }
  }
  activateDashboardTooltips();
  traverseAllCells(bracket);
  bracketAnimation(numberOfRounds);
}

// create final round (two finalist and the winner)
function createFinalRound(bracket, options) {
  const finalRound = createElement("div", ["round", "final-round"]);
  const winnerContainer = createElement("div", ["winner-container"]);
  const winnerCell = createElement("div", [
    "cell",
    "winner-cell",
    "cell_empty",
    "final-cell",
  ]);
  const songWinnerTitleElement = createElement("p", ["song-title"]);
  winnerCell.appendChild(songWinnerTitleElement);
  const winnerCellObject = new Cell(-2, 0, winnerCell);
  winnerCell.addEventListener(
    "click",
    winnerCellObject.advance.bind(winnerCellObject)
  );
  bracket.final["winner"] = winnerCellObject;
  winnerContainer.appendChild(winnerCell);
  const trophyIcon = getSVGIcon(trophySVGData["trophy"]);
  trophyIcon.classList.add("trophy-icon");
  fixSVGDimensions(trophyIcon, "32px");
  winnerContainer.appendChild(trophyIcon);

  finalRound.appendChild(winnerContainer);

  const finalists = createElement("div", ["finalists"]);
  const leftCell = createElement("div", [
    "cell",
    "left-final-cell",
    "final-cell",
    "cell_empty",
    "cell-left",
    "cell-not-first",
  ]);
  const songLeftTitleElement = createElement("p", ["song-title"]);
  leftCell.appendChild(songLeftTitleElement);
  const leftCellObject = new Cell(-1, 0, leftCell);
  leftCell.addEventListener(
    "click",
    leftCellObject.advance.bind(leftCellObject)
  );
  bracket.final["left"] = leftCellObject;
  const rightCell = createElement("div", [
    "cell",
    "right-final-cell",
    "final-cell",
    "cell_empty",
    "cell-right",
    "cell-not-first",
  ]);
  const songRightTitleElement = createElement("p", ["song-title"]);
  rightCell.appendChild(songRightTitleElement);
  const rightCellObject = new Cell(-1, 1, rightCell);
  rightCell.addEventListener(
    "click",
    rightCellObject.advance.bind(rightCellObject)
  );
  bracket.final["right"] = rightCellObject;
  finalists.appendChild(leftCell);
  finalists.appendChild(rightCell);

  finalRound.appendChild(finalists);

  const dashboardContainer = getDashboard(bracket, options);
  finalRound.appendChild(dashboardContainer);
  return finalRound;
}
