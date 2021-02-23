import { BracketData, resetBracket, shuffleBracket} from "./bracketData.js";
import { createBracketStructure } from "./bracketStructure.js"; 
export let bracket = new BracketData();
export let tracksData;

const getSpotifyTracks = function () {
  return fetch("http://192.168.1.62:5000/fetch_spotify_tracks", {
    method: "POST",
    headers: new Headers({
      "Content-Type": "application/json",
    }),
  })
    .then((response) => {
      // if response is not ok (status ain't no 200)
      if (!response.ok) {
        // do something
      }
      return response.json();
    })
    .then((data) => {
      console.log(data);
      return data;
    })
    .catch((error) => {
      // Handle the error
      console.log(`error is ${error}`);
    });
};

// event listener for a submit form and an 'ok' submit button
const getTracksButton = document.querySelector(".get-tracks-button");
getTracksButton.addEventListener("click", () => {
  // checks if the game is not on
  getSpotifyTracks().then(data => {
    tracksData = data;
    createBracketStructure(tracksData);
  });
});

const resetButton = document.querySelector(".reset-button");
resetButton.addEventListener("click", () => {
  // resets the bracket
  resetBracket(bracket);
});

const shuffleButton = document.querySelector(".shuffle-button");
shuffleButton.addEventListener("click", () => {
  // resets the bracket
  shuffleBracket(bracket, tracksData);
});
