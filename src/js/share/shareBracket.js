import { getCorrectURL } from "../misc/utilities.js";
import { shareModalInit } from "./shareModal.js";
// Save current bracket structure with all the info about tracks,
// cells, their position in the bracket and their status (i.e. active/advanceable/etc).
// Used to send current bracket to backend for storing & sharing
export function shareBracket(bracketInfo, options) {
  const bracketDataForSharing = prepareBracketDataForSharing(
    bracketInfo,
    options
  );
  sendBracketData(bracketDataForSharing).then((data) => {
    try {
      if (data) {
        console.log(data);
        const { bracketShareLink } = data;
        const correctShareURL = getCorrectURL(bracketShareLink);
        const description = options.getDescription();
        shareModalInit(correctShareURL, description);
      } else {
        console.log(data);
      }
    } catch (e) {
      console.log(e);
    }
  });
}

// prepares/parses all the needed bracket data for sending it to the backend
function prepareBracketDataForSharing(bracketInfo, options) {
  const bracket = {
    bracketType: options.getCurrentBracketType(),
    value1: options.getInputValue(),
    value2: options.getSecondaryInputValue(),
    description: options.getDescription(),
    extra: options.getExtra(),
    tracks: options.getCurrentTracks(),
    structure: bracketInfo,
  };
  // omit these properties when stringify
  function replacer(key, value) {
    if (
      // remove unnecessary and/or cyclic properties/objects
      key === "nextCell" ||
      key === "cellIndex" ||
      key === "element" ||
      key === "opponent" ||
      // remove raw info about song/text color/album colors
      key === "albumColors" ||
      key === "textColor" ||
      key === "song" ||
      key === "tooltip" ||
      key === "options" ||
      key === "defaultCellColor" ||
      key === "previousCells"
    ) {
      return undefined;
    } else {
      return value;
    }
  }
  const bracketDataForSharing = JSON.stringify(bracket, replacer);
  console.log(bracketDataForSharing);
  return bracketDataForSharing;
}

// send bracket data to backend → get share link
const sendBracketData = async function (bracketDataForSharing) {
  try {
    const response = await fetch("/share", {
      method: "POST",
      headers: new Headers({
        "Content-Type": "application/json",
      }),
      body: bracketDataForSharing,
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
    console.log("data is", data["bracketShareLink"]);
    return data;
  } catch (error) {
    // Handle the error
    console.log(`error is ${error}`);
    return Promise.reject();
  }
};
