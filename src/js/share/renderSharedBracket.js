import { BracketData } from "../bracket/bracketData.js";
import { createBracketStructure } from "../bracket/bracketStructure.js";
import { introAnimation } from "../animation/introAnimation.js";
import { createIntroElements } from "../visuals/intro.js";
import { OptionStorage } from "../options/optionStorage.js";
import { reconstructBracket } from "./reconstructBracket.js";
import { addModal } from "./shareModal.js";
import { handleResponsiveness } from "../responsiveness/mediaQuery.js";
export let bracket = new BracketData();

export let options = new OptionStorage();

// check if the shared bracket info is OK
function checkShareBracketInfo() {
  return typeof sharedBracketData !== "undefined";
}

// renders intro/header
function getIntroHeaderReady() {
  createIntroElements();
  introAnimation();
}

getIntroHeaderReady();

// ready up all the options
function getOptionsReady() {
  options.setInputValue(sharedBracketData["value1"]);
  options.setSecondaryInputValue(sharedBracketData["value2"]);
  options.setCurrentTracks(sharedBracketData["tracks"]);
  options.setDescription(sharedBracketData["description"]);
  options.setExtra(sharedBracketData["extra"]);
  options.setCurrentBracketType(sharedBracketData["bracket_type"]);
}
getOptionsReady();

// create bracket structure
createBracketStructure(bracket, options);
handleResponsiveness();
// reconstruct bracket from the given data
reconstructBracket(
  bracket,
  sharedBracketData["structure"],
  sharedBracketData["tracks"]
);
addModal();
