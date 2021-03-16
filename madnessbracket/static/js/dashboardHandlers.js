import { getSVGIcon } from "./svgGenerator.js";
import { dashboardButtonsSVGData } from "./dashboardButtons.js";
import { createElement } from "./utilities.js";
import { resetBracket, shuffleBracket } from "./bracketData.js";
import { bracket, tracksData } from "./main.js";

export function getDashboard() {
  const dashboardContainer = createElement("div", ["dashboard-container"]);

  const resetButton = createElement("button", [
    "button-dashboard",
    "button-reset",
  ]);
  const resetIcon = getSVGIcon(dashboardButtonsSVGData["reset"]);
  resetButton.appendChild(resetIcon);
  resetButton.addEventListener("click", () => {
    resetBracket(bracket);
  });

  const shuffleButton = createElement("button", [
    "button-dashboard",
    "button-shuffle",
  ]);
  const shuffleIcon = getSVGIcon(dashboardButtonsSVGData["shuffle"]);
  shuffleButton.appendChild(shuffleIcon);
  shuffleButton.addEventListener("click", () => {
    shuffleBracket(bracket, tracksData);
  });

  const shareButton = createElement("button", [
    "button-dashboard",
    "button-share",
  ]);
  const shareIcon = getSVGIcon(dashboardButtonsSVGData["share"]);
  shareButton.appendChild(shareIcon);

  dashboardContainer.append(resetButton, shuffleButton, shareButton);
  return dashboardContainer;
}
