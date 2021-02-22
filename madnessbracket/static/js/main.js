import { BracketData, resetBracket } from "./bracketData.js";
import { createBracketStructure } from "./bracketStructure.js"; 
export let bracket = new BracketData();


const getSpotifyTracks = function () {
  fetch("http://192.168.1.62:5000/fetch_spotify_tracks", {
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
      createBracketStructure(data);
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
  getSpotifyTracks();
});

const resetButton = document.querySelector(".reset-button");
resetButton.addEventListener("click", () => {
  // resets the bracket
  resetBracket();
});
