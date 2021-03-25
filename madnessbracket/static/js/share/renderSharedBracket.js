import { BracketData } from "../bracketData.js";
import { createBracketStructure } from "../bracketStructure.js";
import { introAnimation } from "../animation/introAnimation.js";
import { createIntroElements } from "../intro.js";
import { OptionStorage } from "../optionStorage.js";
import { reconstructBracket } from "./reconstructBracket.js";

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
