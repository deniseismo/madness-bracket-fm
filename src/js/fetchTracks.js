import { showErrorMessage } from "./errors/errorMessageHandlers.js";
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
    const name = options.getInputValue();
    const limit = options.getBracketMaxSize();
    const queryString = constructQueryString({
      name: name,
      limit: limit,
    });
    const response = await fetch(
      `http://192.168.1.62:5000/${bracketType}?` + queryString,
      {
        method: "POST",
        headers: new Headers({
          "Content-Type": "application/json",
        }),
        signal: signal,
      }
    );
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

export function constructQueryString(params) {
  const searchParams = new URLSearchParams();
  for (const prop in params) {
    if (params[prop]) {
      searchParams.append(prop, params[prop]);
    }
  }
  return searchParams;
}

export function pushHistory(params) {
  console.log("pushing history");
  const { state, title, url } = params;
  history.pushState(state, title, url);
}
