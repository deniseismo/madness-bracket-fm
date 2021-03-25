import { BracketData } from "./bracketData.js";
import { createBracketStructure } from "./bracketStructure.js";
import { introAnimation } from "./animation/introAnimation.js";
import { createIntroElements } from "./intro.js";
import { optionStorage } from "./optionStorage.js";
import {
  handleSquareButtons,
  handleMaxBracketSizeOption,
} from "./optionHandlers.js";
import { fetchTracks } from "./fetchTracks.js";
export let bracket = new BracketData();

export let options = new optionStorage();

console.log(document.querySelector(".form__group"));
document.querySelector(".form__group").onsubmit = function () {
  console.log("submitting!");
  const inputValue = document.querySelector(".form__field").value.trim();
  options.setInputValue(inputValue);
  fetchTracks(options).then((data) => {
    try {
      if (data) {
        options.setCurrentTracks(data);
        createBracketStructure(bracket, options);
        console.log(bracket);
      } else {
        console.log(data);
      }
    } catch (e) {
      console.log(e);
    }
  });
  return false;
};

createIntroElements();
introAnimation();
handleSquareButtons(options);
handleMaxBracketSizeOption(options);
