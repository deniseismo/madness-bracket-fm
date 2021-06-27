import { BracketData } from "./bracket/bracketData.js";
import { introAnimation } from "./animation/introAnimation.js";
import { createBracketStructure } from "./bracket/bracketStructure.js";
import { createIntroElements } from "./visuals/intro.js";
import { OptionStorage } from "./options/optionStorage.js";
import { addModal } from "./share/shareModal.js";
import { fetchTracks, pushHistory } from "./fetchTracks.js";
import { showSpinner, hideSpinner } from "./visuals/spinner.js";
import { handleResponsiveness } from "./responsiveness/mediaQuery.js";
import { getQueryStringFromUserInput } from "./options/inputHandlers.js";
import { removeFlashMessages } from "./messages/messages.js";
export let bracket = new BracketData();

export let options = new OptionStorage();

// renders intro/header
function getIntroHeaderReady() {
  createIntroElements();
  introAnimation();
}
function getOptionsReady() {
  options.setInputValue(userRequest["value1"]);
  options.setSecondaryInputValue(userRequest["value2"]);
  options.setBracketMaxSize(userRequest["limit"]);
  options.setCurrentBracketType(userRequest["bracket_type"]);
}
function loadBracketOnDemand() {
  showSpinner();
  fetchTracks(options).then((data) => {
    hideSpinner();
    try {
      if (data) {
        const bracketType = options.getCurrentBracketType();
        const name = options.getInputValue();
        const limit = options.getBracketMaxSize();
        const queryString = getQueryStringFromUserInput(options);
        options.setCurrentTracks(data["tracks"]);
        options.setDescription(data["description"]);
        options.setInputValue(data["value1"]);
        options.setSecondaryInputValue(data["value2"]);
        options.setExtra(data["extra"]);
        createBracketStructure(bracket, options);
        handleResponsiveness();
        addModal();
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
  });
}

getIntroHeaderReady();
addModal();
getOptionsReady();
loadBracketOnDemand();
removeFlashMessages();
