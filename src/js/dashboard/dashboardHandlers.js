import { fixSVGDimensions, getSVGIcon } from "../misc/svgGenerator.js";
import { dashboardButtonsSVGData } from "./dashboardButtons.js";
import { createElement } from "../misc/utilities.js";
import {
  resetBracket,
  retryBracket,
  shuffleBracket,
} from "../bracket/bracketData.js";
import { shareBracket } from "../share/shareBracket.js";
import { fetchTracks } from "../fetchTracks.js";
import { updateDescription } from "../visuals/description.js";
import { returnToSlideZero } from "../responsiveness/slider.js";

// create a dashboard (reset, shuffle, retry, share buttons)
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
    resetBracket(bracket, options);
    returnToSlideZero();
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
    returnToSlideZero();
  });

  const retryButton = createElement("button", [
    "button-dashboard",
    "button-retry",
  ]);
  const retryIcon = getSVGIcon(dashboardButtonsSVGData["retry"]);
  retryIcon.classList.add("dashboard-icon");
  retryButton.appendChild(retryIcon);
  retryButton.addEventListener("click", () => {
    retryButton.classList.add("button-retry_animated");
    retryButton.disabled = true;
    fetchTracks(options).then((data) => {
      retryButton.classList.remove("button-retry_animated");
      retryButton.disabled = false;
      try {
        if (data) {
          options.setComplete(false);
          options.setCurrentTracks(data["tracks"]);
          options.setDescription(data["description"]);
          options.setExtra(data["extra"]);
          updateDescription(options.getDescription());
          retryBracket(bracket, options);
          returnToSlideZero();
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
    shareBracket(bracket, options);
  });

  [resetIcon, shuffleIcon, retryIcon, shareIcon].forEach((icon) => {
    fixSVGDimensions(icon, "25px");
  });

  dashboardContainer.append(
    resetButton,
    shuffleButton,
    retryButton,
    shareButton
  );
  return dashboardContainer;
}
