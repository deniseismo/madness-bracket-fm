import { createElement } from "../misc/utilities.js";
import {
  animateSpinner,
  killSpinnerAnimation,
} from "../animation/spinnerAnimation.js";

// handle showing spinner when bracket's loading
export function showSpinner() {
  const mainContainer = document.querySelector(".main");
  const spinner = createSpinner();
  mainContainer.appendChild(spinner);
  animateSpinner();
}

// hide/remove spinner
export function hideSpinner() {
  const spinner = document.querySelector(".spinner-wrapper");
  if (spinner) {
    killSpinnerAnimation();
    spinner.remove();
  }
}

// create spinner element
function createSpinner() {
  const spinnerWrapper = createElement("div", ["spinner-wrapper"]);
  const spinner = createElement("div", ["spinner"]);
  const upperHorizontalLine = createElement("div", ["horizontal-line", "line"]);
  const lowerHorizontalLine = createElement("div", ["horizontal-line", "line"]);
  const upperVerticalLine = createElement("div", ["vertical-line", "line"]);
  const lowerVerticalLine = createElement("div", ["vertical-line", "line"]);
  const horLinesContainer = createElement("div", ["column-space-between"]);
  const vertLinesContainer = createElement("div", ["column-space-between"]);
  horLinesContainer.append(upperHorizontalLine, lowerHorizontalLine);
  vertLinesContainer.append(upperVerticalLine, lowerVerticalLine);
  const medianLine = createElement("div", ["median-line", "line"]);
  spinner.append(horLinesContainer, vertLinesContainer, medianLine);
  spinnerWrapper.appendChild(spinner);
  return spinnerWrapper;
}
