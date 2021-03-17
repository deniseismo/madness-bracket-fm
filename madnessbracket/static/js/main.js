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

export let options = new optionStore();

export const getSpotifyTracks = async function (inputValue = null) {
  try {
    const currentOptions = processOptions();

    const response = await fetch("http://192.168.1.62:5000/bracket", {
      method: "POST",
      headers: new Headers({
        "Content-Type": "application/json",
      }),
      body: JSON.stringify({
        type: currentOptions["bracketType"],
        value: currentOptions["inputValue"],
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
  options.setInputValue(inputValue);
  getSpotifyTracks().then((data) => {
    try {
      if (data) {
        options.setCurrentTracks(data);
        createBracketStructure(options.getCurrentTracks());
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
  const inputValue = options.getInputValue();
  return {
    bracketType: bracketType,
    maxSize: maxSize,
    inputValue: inputValue,
  };
}

createIntroElements();
introAnimation();
handleSquareButtons();
handleMaxBracketSizeOption();
