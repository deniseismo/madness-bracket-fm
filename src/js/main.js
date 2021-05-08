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
import {
  fetchTracks,
  pushHistory,
  constructQueryString,
} from "./fetchTracks.js";
import { showSpinner, hideSpinner } from "./visuals/spinner.js";
import { handleResponsiveness } from "./responsiveness/mediaQuery.js";
import {
  autocompleteInit,
  handleAutocomplete,
} from "./autocomplete/autocomplete.js";

export let bracket = new BracketData();

export let options = new OptionStorage();

document.querySelector(".form__group").addEventListener("submit", handleSubmit);

function handleSubmit(e) {
  const inputValue = document.querySelector(".form__field").value.trim();
  options.setInputValue(inputValue);
  showSpinner();
  fetchTracks(options)
    .then((data) => {
      hideSpinner();
      try {
        if (data) {
          const bracketType = options.getCurrentBracketType();
          const name = options.getInputValue();
          const limit = options.getBracketMaxSize();
          const queryString = constructQueryString({
            name: name,
            limit: limit,
          });
          options.setCurrentTracks(data["tracks"]);
          options.setDescription(data["description"]);
          options.setSecret(data["secret"]);
          createBracketStructure(bracket, options);
          addModal();
          handleResponsiveness();
          pushHistory({
            state: {
              bracketType: bracketType,
              name: name,
              limit: limit,
            },
            title: null,
            url: `${bracketType}?` + queryString,
          });
        } else {
          console.log(data);
        }
      } catch (e) {
        console.log(e);
      }
    })
    .catch((e) => {
      console.log(e);
    });
  return false;
}

autocompleteInit();
handleAutocomplete();

createIntroElements();
introAnimation();
handleSquareButtons(options);
handleMaxBracketSizeOption(options);
