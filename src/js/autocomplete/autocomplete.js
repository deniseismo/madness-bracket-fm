import autoComplete from "@tarekraafat/autocomplete.js";
import { checkScreenHeight } from "../misc/utilities.js";
import { fetchArtists } from "./fetchArtists.js";

// initialize autocomplete
export function setupAutocomplete(options) {
  // turn off autocomplete for smaller screens
  if (checkScreenHeight(700)) {
    return;
  }
  const autoCompleteJS = createAutocomplete("#autoComplete");
  const autoCompleteJS2 = createAutocomplete("#autoComplete2");
  options.setAutocomplete(autoCompleteJS);
  options.setSecondaryAutocomplete(autoCompleteJS2);
}

function createAutocomplete(inputFieldSelector) {
  const autoCompleteJS = new autoComplete({
    wrapper: false,
    selector: inputFieldSelector,
    placeHolder: "Search for Artist",
    data: {
      src: async () => {
        // Fetch Data from external Source
        const userInput = document.querySelector(inputFieldSelector).value;
        const source = await fetchArtists(userInput);
        const artistsFound = source["suggestions"];
        // Returns Fetched data
        return artistsFound;
      },
      trigger: (query) => {
        return query.replace(/ /g, "").length > 2;
      },
      cache: false,
      filter: (list) => {
        const value = document
          .querySelector(inputFieldSelector)
          .value.slice(0, 3);
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
  return autoCompleteJS;
}

export function initAutocomplete(options) {
  options.getAutocomplete()?.init();
}

export function unInitAutocomplete(options) {
  options.getAutocomplete()?.unInit();
}

// additional autocomplete handlers
export function handleAutocomplete(autoCompleteSelector) {
  // submit on enter
  const autocompleteElement = document.querySelector(autoCompleteSelector);
  autocompleteElement.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      submitForm();
    }
  });
  // fill input's value with the selected value
  autocompleteElement.addEventListener("navigate", function (event) {
    const selectedArtist = event.detail.selection.value;
    autocompleteElement.value = selectedArtist;
  });
  autocompleteElement.addEventListener("selection", function (event) {
    autocompleteElement.blur();
    // Prepare User's Selected Value
    const selection = event.detail.selection.value;
    // Render selected choice to selection div
    // Replace Input value with the selected value
    autocompleteElement.value = selection;
    // Console log autoComplete data feedback
    autocompleteElement.focus();
    event.detail.event.preventDefault();
    submitForm();
  });
}

function submitForm() {
  document.querySelector(".form__group").requestSubmit();
}
