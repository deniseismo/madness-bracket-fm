import { animateLetters } from "./animation/choiceBoxAnimation.js";
import { showElement } from "./utilities.js";

// handles picking bracket type: ARTIST or CHARTS
export function handleSquareButtons(options) {
  const squareButtons = document.querySelectorAll(".square-button");
  squareButtons.forEach((button) => {
    button.addEventListener("click", function () {
      console.log("clicked");
      // button 'activation'
      squareButtons.forEach((button) => button.classList.remove("active"));
      button.classList.add("active");
      // put bracket type into a 'state storage'
      const bracketType = button.dataset.bracketType;
      options.setCurrentBracketType(bracketType);
      // trigger animation
      animateLetters(button);
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
}

// show or hide input field depending on bracket type
function showHideInputField(bracketType) {
  const inputContainer = document.querySelector(".input-container");
  if (bracketType === "artist") {
    // shows input field for an 'artist bracket type'
    inputContainer.style.display = "flex";
    // focus
    const inputField = document.querySelector(".form__field");
    inputField.focus();
  } else {
    inputContainer.style.display = "none";
  }
}
