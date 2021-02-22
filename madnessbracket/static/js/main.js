import {Bracket} from './bracket.js';
import {Cell} from './cell.js';


let bracket = new Bracket();


function createBracketStructure(tracksData) {
  const tracksLength = tracksData['tracks'].length;
  bracket.setStructure(tracksLength);
  const tracks = {
    "left": tracksData['tracks'].slice(0, tracksLength / 2),
    "right": tracksData['tracks'].slice(tracksLength / 2)
  }
  // const leftTracks = tracksData['tracks'].slice(0, tracksLength / 2);
  // const rightTracks = tracksData['tracks'].slice(tracksLength / 2);
  // calculate the number of rounds (sans final round)
  const numberOfRounds = Math.log2(tracksLength / 2) * 2;
  // set a variable for an amount of tracks per round
  let tracksPerRound = tracksLength / 2;
  const mainContainer = document.querySelector('.container');
  // create and append the main bracket div to 'container' container
  const tournamentBracket = document.createElement('div');
  tournamentBracket.classList.add('tournament-bracket');
  mainContainer.appendChild(tournamentBracket);

  for (let i = 0; i < numberOfRounds; i++) {
    const round = document.createElement('div');
    round.classList.add('round');
    if (i < numberOfRounds / 2) {
      var roundIndex = i;
      var side = 'left';
    }
    else {
      var roundIndex = numberOfRounds - i - 1;
      var side = 'right';
    }
    // add an appropriate class to the round specifying its index as well
    const roundClassName = `${side}-${roundIndex}`;
    round.classList.add(roundClassName);

    // add a cell to the 'round' div 'tracksPerRound' times
    for (let j = 0; j < tracksPerRound; j++) {
      const cell = document.createElement('div');
      const cellClassName = side + '-' + roundIndex + '-' + j;
      const cellObject = new Cell(roundIndex, j, cell);
      cell.addEventListener('click', cellObject.advance.bind(cellObject));
      cell.classList.add('cell', cellClassName);
      
      if (roundIndex === 0) {
        const trackTitle = tracks[side][j]['track_title'];
        cellObject.setCurrentSong(trackTitle);
        cellObject.setElementText();
        cellObject.makeAdvanceable();
        cellObject.activate();
      }
      bracket[side][roundIndex][j] = cellObject;
      round.appendChild(cell);
    }

    // check if it's left or right side
    if (i < numberOfRounds / 2 - 1) {
      // half the number of tracks per round
      tracksPerRound /= 2;
    }
    else if (i > numberOfRounds / 2 - 1) {
      // mutiply number of tracks per round by 2
      tracksPerRound *= 2;
    }

    tournamentBracket.appendChild(round);
    if (i === numberOfRounds / 2 - 1) {
      const finalRound = document.createElement('div');
      finalRound.classList.add('round', 'final-round');

      const winnerContainer = document.createElement('div');
      winnerContainer.classList.add('winner-container');
      const winnerCell = document.createElement('div');
      winnerCell.classList.add('cell', 'winner-cell');
      const winnerCellObject = new Cell(i + 2, 0, winnerCell);
      winnerCell.addEventListener('click', winnerCellObject.advance.bind(winnerCellObject));
      bracket.final['winner'] = winnerCellObject;
      winnerContainer.appendChild(winnerCell);

      finalRound.appendChild(winnerContainer);

      const finalists = document.createElement('div');
      finalists.classList.add('finalists');
      const leftCell = document.createElement('div');
      leftCell.classList.add('cell', 'left-final-cell', 'final-cell');
      const leftCellObject = new Cell(i + 1, 0, leftCell);
      leftCell.addEventListener('click', leftCellObject.advance.bind(leftCellObject));
      bracket.final['left'] = leftCellObject;
      const rightCell = document.createElement('div');
      rightCell.classList.add('cell', 'right-final-cell', 'final-cell');
      const rightCellObject = new Cell(i + 1, 1, rightCell);
      rightCell.addEventListener('click', rightCellObject.advance.bind(rightCellObject));
      bracket.final['right'] = rightCellObject;
      finalists.appendChild(leftCell);
      finalists.appendChild(rightCell);

      finalRound.appendChild(finalists);


      tournamentBracket.appendChild(finalRound);
    }
  }

  traverseAllCells();
  console.log(bracket)

};


function traverseAllCells() {
  const numberOfRounds = Object.keys(bracket.left).length;
  console.log('numberofRounds' + numberOfRounds)
  // traversing through the rounds
  for (let i = 0; i < numberOfRounds; i++) {
    const numberOfCells = Object.keys(bracket.left[i]).length;
    // traversing through cells processing 2 at a time, step = 2 as well
    for (let j = 0; j < numberOfCells; j += 2) {
      // in a pair of cells set each other as opponents
      ['left', 'right'].forEach(side => {
        bracket[side][i][j].setOpponent(bracket[side][i][j + 1]);
        bracket[side][i][j + 1].setOpponent(bracket[side][i][j]);
      })
      // check if there's a next round 
      if (bracket.left.hasOwnProperty(i + 1)) {
        // set the appropriate's next round's cell to be the 'nextCell' (where they should advance to)
        const nextCellIndex = Math.floor(j / 2);
        ['left', 'right'].forEach(side => {
          bracket[side][i][j].setNextCell(bracket[side][i + 1][nextCellIndex]);
          bracket[side][i][j + 1].setNextCell(bracket[side][i + 1][nextCellIndex]);
        })
      }
      // no next round meaning it's finale time
      else {
        ['left', 'right'].forEach(side => {
          bracket[side][i][j].setNextCell(bracket.final[side]);
          bracket[side][i][j + 1].setNextCell(bracket.final[side]);
        })
      }
    }
    ['left', 'right'].forEach(side => {
      bracket.final[side].setNextCell(bracket.final['winner']);
    })
    bracket.final['left'].setOpponent(bracket.final['right']);
    bracket.final['right'].setOpponent(bracket.final['left']);
  }
  console.log('traversing')
};



const getSpotifyTracks = function() {
  
  fetch('http://192.168.1.62:5000/fetch_spotify_tracks', {
    method: 'POST',
    headers: new Headers({
      'Content-Type': 'application/json'
    })
  })
  .then(response => {
    // if response is not ok (status ain't no 200)
      if (!response.ok) {
        // do something
      }
    return response.json();
    })
  .then(data => {
    console.log(data)
    createBracketStructure(data);
  })
  .catch((error) => {
    // Handle the error
    console.log(`error is ${error}`);
  });
};


// event listener for a submit form and an 'ok' submit button
const getTracksButton = document.querySelector('.get-tracks-button');
getTracksButton.addEventListener('click', () => {
  // checks if the game is not on
    getSpotifyTracks();
});