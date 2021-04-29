import { BracketData } from "./bracket/bracketData.js";
import { introAnimation } from "./animation/introAnimation.js";
import { createBracketStructure } from "./bracket/bracketStructure.js";
import { createIntroElements } from "./visuals/intro.js";
import { OptionStorage } from "./options/optionStorage.js";
import { addModal } from "./share/shareModal.js";
import {
  fetchTracks,
  pushHistory,
  constructQueryString,
} from "./fetchTracks.js";
import { showSpinner, hideSpinner } from "./visuals/spinner.js";
import { handleResponsiveness } from "./responsiveness/mediaQuery.js";
export let bracket = new BracketData();

export let options = new OptionStorage();

// renders intro/header
function getIntroHeaderReady() {
  createIntroElements();
  introAnimation();
}

getIntroHeaderReady();
addModal();
function getOptionsReady() {
  options.setInputValue(userRequest["name"]);
  options.setBracketMaxSize(userRequest["limit"]);
  options.setCurrentBracketType(userRequest["bracket_type"]);
}
getOptionsReady();
loadBracketOnDemand();

function loadBracketOnDemand() {
  showSpinner();
  fetchTracks(options).then((data) => {
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
