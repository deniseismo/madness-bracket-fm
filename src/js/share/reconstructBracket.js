export function reconstructBracket(
  currentBracketData,
  sharedBracketData,
  tracksArray
) {
  function updateCellData(cellToUpdate, cellData) {
    const trackID = cellData["trackID"];
    cellToUpdate.removeClassEmpty();
    cellToUpdate.setTrackID(trackID);
    cellToUpdate.setCurrentSong(tracksArray[trackID]["track_title"]);
    cellToUpdate.setArtistName(tracksArray[trackID]["artist_name"]);
    cellToUpdate.setPreviewURL(tracksArray[trackID]["spotify_preview_url"]);
    cellToUpdate.setAlbumColors(tracksArray[trackID]["album_colors"]);
    cellToUpdate.setTextColor(tracksArray[trackID]["text_color"]);
    cellToUpdate.applyColors();
    cellToUpdate.setElementText();
    if (cellData["active"]) {
      cellToUpdate.activate();
    } else {
      cellToUpdate.deactivate();
    }
    if (cellData["advanceable"]) {
      cellToUpdate.makeAdvanceable();
    } else {
      cellToUpdate.makeUnadvanceable();
    }
    if (cellData["loser"]) {
      cellToUpdate.lose();
    }
  }

  for (const finalist in sharedBracketData["final"]) {
    const cellData = sharedBracketData["final"][finalist];
    const trackID = cellData["trackID"];
    if (trackID || trackID === 0) {
      updateCellData(currentBracketData["final"][finalist], cellData);
    }
  }
  ["left", "right"].forEach((side) => {
    for (const roundIndex in sharedBracketData[side]) {
      for (const cellIndex in sharedBracketData[side][roundIndex]) {
        const cellData = sharedBracketData[side][roundIndex][cellIndex];
        const trackID = cellData["trackID"];
        if (trackID || trackID === 0) {
          updateCellData(
            currentBracketData[side][roundIndex][cellIndex],
            cellData
          );
        }
      }
    }
  });
}
