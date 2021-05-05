import {
  animateLetters,
  deanimateLetters,
} from "../animation/choiceBoxAnimation.js";
import { isInputValid, showElement } from "../misc/utilities.js";
import { addMaxSizeTooltip } from "./maxSizeTooltip.js";

// handles picking bracket type: ARTIST or CHARTS
export function handleSquareButtons(options) {
  const squareButtons = document.querySelectorAll(".square-button");
  squareButtons.forEach((button) => {
    button.addEventListener("click", function (e) {
      // button 'activation'
      if (this.classList.contains("active")) {
        return;
      }
      squareButtons.forEach((button) => button.classList.remove("active"));
      button.classList.add("active");
      // put bracket type into a 'state storage'
      const bracketType = button.dataset.bracketType;
      options.setCurrentBracketType(bracketType);
      // trigger animation
      deanimateLetters(button);
      setTimeout(() => {
        animateLetters(button);
      }, 400);

      const optionsContainer = document.querySelector(".options");
      showElement(optionsContainer);
      // show or hide input field depending on bracket type
      showHideInputField(bracketType);
    });
  });
}
// handles picking bracket max size: 4, 8, 16, or 32 tracks (max)
export function handleMaxBracketSizeOption(options) {
  const maxBracketSizeButtons = document.querySelectorAll(
    ".bracket_max_size_option"
  );
  maxBracketSizeButtons.forEach((button) => {
    button.addEventListener("click", function () {
      maxBracketSizeButtons.forEach((button) =>
        button.classList.remove("bracket_max_size_option_active")
      );
      button.classList.add("bracket_max_size_option_active");
      // put bracket max size into a 'state storage'
      const maxSize = button.dataset.maxSize;
      options.setBracketMaxSize(maxSize);
    });
  });
  addMaxSizeTooltip();
}

// show or hide input field depending on bracket type
function showHideInputField(bracketType) {
  const inputContainer = document.querySelector(".input-container");
  const submitButton = document.querySelector(".generate-button");
  if (bracketType === "artist") {
    // shows input field for an 'artist bracket type'
    inputContainer.style.display = "flex";
    // focus
    const inputField = document.querySelector(".form__field");
    inputField.focus();
    // disable submit button if input's empty
    submitButton.disabled = !isInputValid(inputField.value);
    inputField.addEventListener("input", () => {
      // dynamically disable submit button if input's empty
      submitButton.disabled = !isInputValid(inputField.value);
    });
  } else {
    inputContainer.style.display = "none";
    submitButton.disabled = false;
  }
}
