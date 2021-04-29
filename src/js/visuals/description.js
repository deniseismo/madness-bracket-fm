import { createElement } from "../misc/utilities.js";

// show bracket description/title: artist's name/classics/charts/secret, etc.
export function displayBracketDescription(description) {
  const mainContainer = document.querySelector(".main");
  const descriptionContainer = createElement("div", ["description-container"]);
  const descriptionText = createElement("h1", ["description-text"]);
  descriptionText.textContent = description.toUpperCase();
  const hr = createElement("hr", ["description-line"]);
  descriptionContainer.append(descriptionText, hr);
  mainContainer.appendChild(descriptionContainer);
}

/* update bracket's description with the new one (in case it somehow changed, 
 e.g. if one click retry button in SECRET mode) 
*/
export function updateDescription(description) {
  const descriptionText = document.querySelector(".description-text");
  descriptionText.textContent = description.toUpperCase();
}
