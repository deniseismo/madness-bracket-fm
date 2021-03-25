import { getSVGIcon } from "./svgGenerator.js";
import { dashboardButtonsSVGData } from "./dashboardButtons.js";
import { createElement } from "./utilities.js";
import { resetBracket, shuffleBracket } from "./bracketData.js";
import { shareBracket } from "./share/shareBracket.js";
import { fetchTracks } from "./fetchTracks.js";

export function getDashboard(bracket, options) {
  const dashboardContainer = createElement("div", ["dashboard-container"]);

  const resetButton = createElement("button", [
    "button-dashboard",
    "button-reset",
  ]);
  const resetIcon = getSVGIcon(dashboardButtonsSVGData["reset"]);
  resetIcon.classList.add("dashboard-icon");
  resetButton.appendChild(resetIcon);
  resetButton.addEventListener("click", () => {
    resetBracket(bracket);
  });

  const shuffleButton = createElement("button", [
    "button-dashboard",
    "button-shuffle",
  ]);
  const shuffleIcon = getSVGIcon(dashboardButtonsSVGData["shuffle"]);
  shuffleIcon.classList.add("dashboard-icon");
  shuffleButton.appendChild(shuffleIcon);
  shuffleButton.addEventListener("click", () => {
    shuffleBracket(bracket, options);
  });

  const retryButton = createElement("button", [
    "button-dashboard",
    "button-retry",
  ]);
  const retryIcon = getSVGIcon(dashboardButtonsSVGData["retry"]);
  retryIcon.classList.add("dashboard-icon");
  retryButton.appendChild(retryIcon);
  retryButton.addEventListener("click", () => {
    fetchTracks(options).then((data) => {
      try {
        if (data) {
          options.setCurrentTracks(data["tracks"]);
          options.setDescription(data["description"]);
          shuffleBracket(bracket, options);
        } else {
          console.log(data);
        }
      } catch (e) {
        console.log(e);
      }
    });
  });

  const shareButton = createElement("button", [
    "button-dashboard",
    "button-share",
  ]);
  const shareIcon = getSVGIcon(dashboardButtonsSVGData["share"]);
  shareIcon.classList.add("dashboard-icon");
  shareButton.appendChild(shareIcon);
  shareButton.addEventListener("click", () => {
    console.log(bracket);
    console.log(options.getCurrentTracks());
    shareBracket(bracket, options);
  });

  dashboardContainer.append(
    resetButton,
    shuffleButton,
    retryButton,
    shareButton
  );
  return dashboardContainer;
}
