import { showErrorMessage } from "./errors/errorMessageHandlers.js";
import { getCorrectURL } from "./misc/utilities.js";
import { getQueryStringFromUserInput } from "./options/inputHandlers.js";

// fetch tracks from the server
let controller = null;
export const fetchTracks = async function (options) {
  // abort any ongoing fetching
  if (controller) {
    controller.abort();
  }
  controller = new AbortController();
  const signal = controller.signal;
  try {
    const bracketType = options.getCurrentBracketType();
    const queryString = getQueryStringFromUserInput(options);
    const fetchURL = getCorrectURL(`${bracketType}?` + queryString);
    const response = await fetch(fetchURL, {
      method: "POST",
      headers: new Headers({
        "Content-Type": "application/json",
      }),
      signal: signal,
    });
    // if response is not ok (status ain't no 200)
    if (!response.ok) {
      // do something
      return response.json().then((failData) => {
        console.log(failData.message);
        showErrorMessage(failData.message);
        // throw new Error(failData.message);
      });
    }
    const data = await response.json();
    console.log("data is", data);
    return data;
  } catch (error) {
    // Handle the error
    console.log(`error is ${error}`);
    return Promise.reject();
  }
};

export function pushHistory(params) {
  console.log("pushing history");
  const { state, title, url } = params;
  console.log(state, title, url);
  history.pushState(state, title, url);
  window.addEventListener("popstate", (event) => {
    if (event.state === null) {
      // initial page
      window.location.reload();
    }
  });
}
