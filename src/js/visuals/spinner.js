import { createElement } from "../misc/utilities.js";
import {
  animateSpinner,
  killSpinnerAnimation,
} from "../animation/spinnerAnimation.js";

export function showSpinner() {
  const container = document.querySelector(".container");
  const spinner = createSpinner();
  container.appendChild(spinner);
  animateSpinner();
}

export function hideSpinner() {
  const spinner = document.querySelector(".spinner-wrapper");
  if (spinner) {
    killSpinnerAnimation();
    spinner.remove();
  }
}

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
