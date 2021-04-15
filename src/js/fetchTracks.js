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
    const response = await fetch(`http://192.168.1.62:5000/${bracketType}`, {
      method: "POST",
      headers: new Headers({
        "Content-Type": "application/json",
      }),
      signal: signal,
      body: JSON.stringify({
        type: options.getCurrentBracketType(),
        value: options.getInputValue(),
        limit: options.getBracketMaxSize(),
      }),
    });
    // if response is not ok (status ain't no 200)
    if (!response.ok) {
      // do something
      return response.json().then((failData) => {
        console.log(failData.message);
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
