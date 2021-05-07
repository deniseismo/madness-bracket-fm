import { getCorrectURL } from "../misc/utilities";
import tippy from "tippy.js";

export function triggerCommentary(artistName, songTitle, options) {
  const bracketType = options.getCurrentBracketType();
  const description = options.getDescription();
  console.log("commentary triggered");
  fetchCommentary(artistName, songTitle, bracketType, description).then(
    (commentaryData) => {
      const { commentary } = commentaryData;
      if (commentary) {
        activateCommentaryTooltip(commentary);
      }
    }
  );
}

// get a secret commentary/taunt/easter egg
async function fetchCommentary(
  artistName,
  songTitle,
  bracketType,
  description
) {
  const fetchURL = getCorrectURL("get_commentary");

  const response = await fetch(fetchURL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      artist_name: artistName,
      song_title: songTitle,
      bracket_type: bracketType,
      description: description,
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
