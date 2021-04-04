export const fetchTracks = async function (options) {
  try {
    const response = await fetch("http://192.168.1.62:5000/bracket", {
      method: "POST",
      headers: new Headers({
        "Content-Type": "application/json",
      }),
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
