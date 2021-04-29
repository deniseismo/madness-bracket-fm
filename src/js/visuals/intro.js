import { createElement } from "../misc/utilities.js";

// create intro/header
export function createIntroElements() {
  const introContainer = createIntroLines();
  const introTitle = createElement("div", ["intro-title"]);
  const titleLink = createElement("a", ["title-link"]);
  titleLink.textContent = "madness bracket";
  titleLink.href = "/home";
  introTitle.appendChild(titleLink);
  introContainer.appendChild(introTitle);

  const headerContainer = document.querySelector("header");
  headerContainer.appendChild(introContainer);
}

// create intro/header bracket lines -=
export function createIntroLines(reverse = false) {
  const introContainer = createElement("div", ["intro-container"]);

  const horizontalLines = createElement("div", ["column-space-between"]);
  const horizontalLine1 = createElement("div", ["horizontal-line"]);
  const horizontalLine2 = createElement("div", ["horizontal-line"]);
  horizontalLines.append(horizontalLine1, horizontalLine2);

  const verticalLines = createElement("div", ["column-space-between"]);
  const verticalLine1 = createElement("div", ["vertical-line"]);
  const verticalLine2 = createElement("div", ["vertical-line"]);
  verticalLines.append(verticalLine1, verticalLine2);

  const introLine = createElement("div", ["intro-line"]);
  if (!reverse) {
    introContainer.append(horizontalLines, verticalLines, introLine);
  } else {
    introContainer.append(introLine, verticalLines, horizontalLines);
  }
  return introContainer;
}
