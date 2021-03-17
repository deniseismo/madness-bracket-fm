import { getSVGIcon } from "./svgGenerator.js";
import { dashboardButtonsSVGData } from "./dashboardButtons.js";
import { createElement } from "./utilities.js";
import { resetBracket, shuffleBracket } from "./bracketData.js";
import { bracket, getSpotifyTracks, options } from "./main.js";

export function getDashboard() {
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
    const tracksData = options.getCurrentTracks();
    shuffleBracket(bracket, tracksData);
  });

  const retryButton = createElement("button", [
    "button-dashboard",
    "button-retry",
  ]);
  const retryIcon = getSVGIcon(dashboardButtonsSVGData["retry"]);
  retryIcon.classList.add("dashboard-icon");
  retryButton.appendChild(retryIcon);
  retryButton.addEventListener("click", () => {
    getSpotifyTracks().then((data) => {
      try {
        if (data) {
          options.setCurrentTracks(data);
          shuffleBracket(bracket, options.getCurrentTracks());
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

  dashboardContainer.append(
    resetButton,
    shuffleButton,
    retryButton,
    shareButton
  );
  return dashboardContainer;
}
