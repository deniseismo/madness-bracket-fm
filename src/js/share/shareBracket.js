import { createElement } from "../utilities.js";
import MicroModal from "micromodal";
//import MicroModal from "../third-party/micromodal.es.js";
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
        triggerShareModal(data["share_bracket_id"]);
        // addBracketLink(data["share_bracket_id"]);
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
    description: options.getDescription(),
    tracks: options.getCurrentTracks(),
    structure: bracketInfo,
  };
  // omit these properties when stringify
  function replacer(key, value) {
    if (
      // remove unnecessary and/or circular properties
      key === "nextCell" ||
      key === "cellIndex" ||
      key === "element" ||
      key === "opponent" ||
      // remove raw info about song/text color/album colors
      key === "albumColors" ||
      key === "textColor" ||
      key === "song"
    ) {
      return undefined;
    } else {
      return value;
    }
  }
  console.log(JSON.stringify(bracket, replacer));
  const bracketDataForSharing = JSON.stringify(bracket, replacer);
  return bracketDataForSharing;
}

// send bracket data to backend → get share link
const sendBracketData = async function (bracketDataForSharing) {
  try {
    const response = await fetch("http://192.168.1.62:5000/share", {
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
    console.log("data is", data["share_bracket_id"]);
    return data;
  } catch (error) {
    // Handle the error
    console.log(`error is ${error}`);
    return Promise.reject();
  }
};

// show share modal with the share link ready
function triggerShareModal(shareLink) {
  const shareLinkElement = document.querySelector(".share-link");
  shareLinkElement.value = shareLink;
  MicroModal.show("modal-1");
}
