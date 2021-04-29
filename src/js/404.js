import { introAnimation } from "./animation/introAnimation.js";
import { createIntroElements } from "./visuals/intro.js";
function getIntroHeaderReady() {
  createIntroElements();
  introAnimation();
}

getIntroHeaderReady();
