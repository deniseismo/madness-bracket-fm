// Durstenfeld shuffle © https://www.wikiwand.com/en/Fisher%E2%80%93Yates_shuffle
export function shuffleArray(array) {
  let shuffledArray = [...array];
  for (let i = shuffledArray.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [shuffledArray[i], shuffledArray[j]] = [shuffledArray[j], shuffledArray[i]];
  }
  return shuffledArray;
}

// creates element of a given type, adds given classes
export function createElement(type, classes = null) {
  const element = document.createElement(type);
  if (classes) {
    for (const aClass of classes) {
      element.classList.add(aClass);
    }
  }
  return element;
}

// picks a random element from a given array
export function pickRandomElement(array) {
  const randomIndex = Math.floor(Math.random() * array.length);
  return array[randomIndex];
}

export function showElement(element) {
  // element.style.display = 'flex';
  element.style.visibility = "visible";
}

export function hideElement(element) {
  element.style.display = "none";
}

// removes all child nodes from a given parent
export function removeAllChildNodes(parent) {
  while (parent.firstChild) {
    parent.removeChild(parent.firstChild);
  }
}

export function doesArrayContainSomethingTruthy(array) {
  const exist = (element) => element;
  return array.some(exist);
}

export function isInputValid(value) {
  return value.length > 0;
}

export function shuffleTracks(tracks, options) {
  console.log(options.getSecret());
  const isArtistBattle = options.getSecret() === "artists_battle";
  if (isArtistBattle) {
    const tracksLength = tracks.length / 2;
    let firstArtist = [];
    let secondArtist = [];
    tracks.forEach((track, index) => {
      if (index % 2 == 0) {
        firstArtist.push(track);
      } else {
        secondArtist.push(track);
      }
    });
    firstArtist = shuffleArray(firstArtist);
    secondArtist = shuffleArray(secondArtist);
    let battleTracks = [];
    for (let i = 0; i < tracksLength; i++) {
      battleTracks.push(firstArtist[i]);
      battleTracks.push(secondArtist[i]);
    }
    console.log("battle tracks:", battleTracks);
    return battleTracks;
  }
  return shuffleArray(tracks);
}
