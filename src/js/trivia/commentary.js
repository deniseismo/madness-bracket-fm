import { getCorrectURL } from "../misc/utilities";
import tippy from "tippy.js";

export function triggerCommentary(artistName, songTitle) {
  console.log("commentary triggered");
  fetchCommentary(artistName, songTitle).then((commentaryData) => {
    const { commentary } = commentaryData;
    if (commentary) {
      activateCommentaryTooltip(commentary);
    }
  });
}

async function fetchCommentary(artistName, songTitle) {
  // fetches madness commentary
  const fetchURL = getCorrectURL("get_commentary");

  const response = await fetch(fetchURL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      artist_name: artistName,
      song_title: songTitle,
    }),
  });
  if (!response.ok) {
    return null;
  }
  const commentaryData = await response.json();
  console.log(commentaryData);
  return commentaryData;
}

function activateCommentaryTooltip(commentary) {
  const commentaryTooltip = tippy(".winner-cell", {
    arrow: true,
    placement: "top",
    animation: "scale-extreme",
    theme: "madness",
    content: commentary,
    duration: [300, 500],
    showOnCreate: true,
    onHidden(commentaryTooltip) {
      console.log(commentaryTooltip);
      commentaryTooltip.hide();
      commentaryTooltip.destroy();
    },
  });
}
