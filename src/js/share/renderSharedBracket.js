import { BracketData } from "../bracket/bracketData.js";
import { createBracketStructure } from "../bracket/bracketStructure.js";
import { introAnimation } from "../animation/introAnimation.js";
import { createIntroElements } from "../visuals/intro.js";
import { OptionStorage } from "../options/optionStorage.js";
import { reconstructBracket } from "./reconstructBracket.js";
import { addModal } from "./shareModal.js";

export let bracket = new BracketData();

export let options = new OptionStorage();

// check if the shared bracket info is OK
function checkShareBracketInfo() {
  return typeof sharedBracketData !== "undefined";
}

function getIntroHeaderReady() {
  createIntroElements();
  introAnimation();
}

getIntroHeaderReady();

function getOptionsReady() {
  options.setInputValue(sharedBracketData["description"]);
  options.setCurrentTracks(sharedBracketData["tracks"]);
  options.setDescription(sharedBracketData["description"]);
  options.setCurrentBracketType(sharedBracketData["bracket_type"]);
}
getOptionsReady();

console.log("options:", options);
createBracketStructure(bracket, options);
console.log(sharedBracketData["structure"]);
console.log(sharedBracketData["tracks"]);

reconstructBracket(
  bracket,
  sharedBracketData["structure"],
  sharedBracketData["tracks"]
);
addModal();
