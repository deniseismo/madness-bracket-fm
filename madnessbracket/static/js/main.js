import { BracketData, resetBracket, shuffleBracket } from "./bracketData.js";
import { createBracketStructure } from "./bracketStructure.js";
import { introAnimation } from "./animation/introAnimation.js";
import { createIntroElements } from "./intro.js";
import { optionStore } from "./optionStore.js";
import {
  handleSquareButtons,
  handleMaxBracketSizeOption,
} from "./optionHandlers.js";
export let bracket = new BracketData();

export let tracksData;

export let options = new optionStore();

const getSpotifyTracks = async function (inputValue = null) {
  try {
    const currentOptions = processOptions();

    const response = await fetch("http://192.168.1.62:5000/bracket", {
      method: "POST",
      headers: new Headers({
        "Content-Type": "application/json",
      }),
      body: JSON.stringify({
        type: currentOptions["bracketType"],
        value: inputValue,
        limit: currentOptions["maxSize"],
      }),
    });
    // if response is not ok (status ain't no 200)
    if (!response.ok) {
      // do something
      return response.json().then((failData) => {
        console.log(failData.message);
        // throw new Error(failData.message);
      });
    }
    const data = await response.json();
    console.log("data is", data);
    return data;
  } catch (error) {
    // Handle the error
    console.log(`error is ${error}`);
    return Promise.reject();
  }
};

console.log(document.querySelector(".form__group"));
document.querySelector(".form__group").onsubmit = function () {
  console.log("submitting!");
  const inputValue = document.querySelector(".form__field").value.trim();
  getSpotifyTracks(inputValue).then((data) => {
    try {
      if (data) {
        tracksData = data;
        createBracketStructure(tracksData);
      } else {
        console.log(data);
      }
    } catch (e) {
      console.log(e);
    }
  });
  return false;
};

function processOptions() {
  const bracketType = options.getCurrentBracketType();
  const maxSize = options.getBracketMaxSize();
  return {
    bracketType: bracketType,
    maxSize: maxSize,
  };
}

createIntroElements();
introAnimation();
handleSquareButtons();
handleMaxBracketSizeOption();
