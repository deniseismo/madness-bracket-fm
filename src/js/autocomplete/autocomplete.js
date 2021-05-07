import autoComplete from "@tarekraafat/autocomplete.js";
import { checkScreenHeight } from "../misc/utilities.js";
import { fetchArtists } from "./fetchArtists.js";

// initialize autocomplete
export function autocompleteInit() {
  // turn off autocomplete for smaller screens
  if (checkScreenHeight(700)) {
    return;
  }
  const autoCompleteJS = new autoComplete({
    placeHolder: "Search for Food...",
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
      results: (list) => {
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
      highlight: {
        render: true,
      },
    },
    trigger: {
      event: ["input", "focus"],
    },
    threshold: 3,
    onSelection: (feedback) => {
      const inputField = document.querySelector("#autoComplete");
      inputField.blur();
      // Prepare User's Selected Value
      const selection = feedback.selection.value;
      // Render selected choice to selection div
      // Replace Input value with the selected value
      inputField.value = selection;
      // Console log autoComplete data feedback
      inputField.focus();
      feedback.event.preventDefault();
      document.querySelector(".form__group").requestSubmit();
    },
  });
}

// additional autocomplete handlers
export function handleAutocomplete() {
  // submit on enter
  document
    .querySelector("#autoComplete")
    .addEventListener("keydown", (event) => {
      if (event.key === "Enter") {
        document.querySelector(".form__group").requestSubmit();
      }
    });
  // fill input's value with the selected value
  document
    .querySelector("#autoComplete")
    .addEventListener("navigate", function (event) {
      const selectedArtist = event.detail.selection.value;
      document.querySelector("#autoComplete").value = selectedArtist;
    });
}
