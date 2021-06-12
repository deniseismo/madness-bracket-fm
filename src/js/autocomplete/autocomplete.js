import autoComplete from "@tarekraafat/autocomplete.js";
import { checkScreenHeight } from "../misc/utilities.js";
import { fetchArtists } from "./fetchArtists.js";

// initialize autocomplete
export function setupAutocomplete(options) {
  // turn off autocomplete for smaller screens
  if (checkScreenHeight(700)) {
    return;
  }
  const autoCompleteJS = new autoComplete({
    placeHolder: "Search for Artist",
    data: {
      src: async () => {
        // Fetch Data from external Source
        const userInput = document.querySelector("#autoComplete").value;
        const source = await fetchArtists(userInput);
        const artistsFound = source["suggestions"];
        // Returns Fetched data
        return artistsFound;
      },
      cache: false,
      filter: (list) => {
        const value = document.querySelector("#autoComplete").value.slice(0, 3);
        // Sort results by starting character
        const sortedList = list.sort((a, b) => {
          if (!a.match.startsWith(value)) return -1;
          if (a.match.startsWith(value)) return 1;
          return 0;
        });
        console.log(sortedList);
        // Return sorted list
        return sortedList;
      },
    },
    // 3 or 1 result item in a result list for different screen sizes
    resultsList: {
      maxResults: checkScreenHeight(800) ? 1 : 3,
    },
    resultItem: {
      highlight: true,
    },
    diacritics: "loose",
    threshold: 3,
  });
  options.setAutocomplete(autoCompleteJS);
}

export function initAutocomplete(options) {
  options.getAutocomplete().init();
}

export function unInitAutocomplete(options) {
  options.getAutocomplete().unInit();
}

// additional autocomplete handlers
export function handleAutocomplete() {
  // submit on enter
  const autocompleteElement = document.querySelector("#autoComplete");
  autocompleteElement.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      document.querySelector(".form__group").requestSubmit();
    }
  });
  // fill input's value with the selected value
  autocompleteElement.addEventListener("navigate", function (event) {
    const selectedArtist = event.detail.selection.value;
    document.querySelector("#autoComplete").value = selectedArtist;
  });
  autocompleteElement.addEventListener("selection", function (event) {
    const inputField = document.querySelector("#autoComplete");
    inputField.blur();
    // Prepare User's Selected Value
    const selection = event.detail.selection.value;
    // Render selected choice to selection div
    // Replace Input value with the selected value
    inputField.value = selection;
    // Console log autoComplete data feedback
    inputField.focus();
    event.detail.event.preventDefault();
    document.querySelector(".form__group").requestSubmit();
  });
}
