import { createElement } from "../misc/utilities.js";

export function showErrorMessage(message) {
  const container = document.querySelector(".container");
  const error = createErrorMessage(message);
  container.appendChild(error);
}

export function hideErrorMessage() {
  const error = document.querySelector(".error-wrapper");
  if (error) {
    error.remove();
  }
}

function createErrorMessage(message) {
  const errorWrapper = createElement("div", ["error-wrapper"]);
  const errorMessage = createElement("p", ["error-message"]);
  errorMessage.textContent = message;
  errorWrapper.appendChild(errorMessage);
  errorWrapper.addEventListener("click", hideErrorMessage);
  return errorWrapper;
}
