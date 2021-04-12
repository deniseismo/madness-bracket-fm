import { BracketData } from "./bracket/bracketData.js";
import { createBracketStructure } from "./bracket/bracketStructure.js";
import { introAnimation } from "./animation/introAnimation.js";
import { createIntroElements } from "./visuals/intro.js";
import { addModal } from "./share/shareModal.js";
import { OptionStorage } from "./options/optionStorage.js";
import {
  handleSquareButtons,
  handleMaxBracketSizeOption,
} from "./options/optionHandlers.js";
import { fetchTracks } from "./fetchTracks.js";
export let bracket = new BracketData();

export let options = new OptionStorage();

document.querySelector(".form__group").onsubmit = function () {
  const inputValue = document.querySelector(".form__field").value.trim();
  options.setInputValue(inputValue);
  fetchTracks(options).then((data) => {
    try {
      if (data) {
        options.setCurrentTracks(data["tracks"]);
        options.setDescription(data["description"]);
        createBracketStructure(bracket, options);
        addModal();
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
