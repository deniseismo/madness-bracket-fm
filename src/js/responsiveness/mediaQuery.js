import {
  transformBracketIntoSlider,
  removeSlider,
  sliderInit,
} from "./slider.js";

export function handleResponsiveness() {
  const mediaQuery = window.matchMedia("(max-width: 910px)");
  function handleSmallerDevices(e) {
    // Check if the media query is true
    if (e.matches) {
      // Then log the following message to the console
      console.log("Media Query Matched!");
      transformBracketIntoSlider();
      sliderInit();
    } else {
      removeSlider();
    }
  } // Register event listener
  mediaQuery.addEventListener("change", handleSmallerDevices);
  handleSmallerDevices(mediaQuery);
}
