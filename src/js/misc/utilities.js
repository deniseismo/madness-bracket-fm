// shuffle array
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

// pick a random element from a given array
export function pickRandomElement(array) {
  const randomIndex = Math.floor(Math.random() * array.length);
  return array[randomIndex];
}

// show element
export function showElement(element) {
  // element.style.display = 'flex';
  element.style.visibility = "visible";
}

// hide element
export function hideElement(element) {
  element.style.display = "none";
}

// removes all child nodes from a given parent
export function removeAllChildNodes(parent) {
  while (parent.firstChild) {
    parent.removeChild(parent.firstChild);
  }
}
// check if any of the array's elements is truthy
export function doesArrayContainSomethingTruthy(array) {
  const exist = (element) => element;
  return array.some(exist);
}

// check if input's not empty
export function isInputValid(value) {
  return value.length > 0;
}

// shuffle tracks
export function shuffleTracks(tracks, options) {
  const isArtistBattle = options.getSecret() === "artists_battle";
  /* shuffle tracks differently if it's "artist battle".
  we need to keep 'artist vs artist' logic in all of the match-ups after shuffling
  */
  if (isArtistBattle) {
    const tracksLength = tracks.length / 2;
    let firstArtist = [];
    let secondArtist = [];
    // separate two artists tracks into different arrays
    tracks.forEach((track, index) => {
      if (index % 2 == 0) {
        firstArtist.push(track);
      } else {
        secondArtist.push(track);
      }
    });
    // shuffle each artist's tracks array separately
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
  // shuffle normally
  return shuffleArray(tracks);
}

// get current screen size
export function getScreenSize() {
  const mediaQueryFull = window.matchMedia("(min-width: 1200px)");
  const mediaQuery640 = window.matchMedia("(min-width: 641px)");
  const mediaQuery500 = window.matchMedia("(min-width: 500px)");
  const mediaQuery400 = window.matchMedia("(min-width: 400px)");
  if (mediaQueryFull.matches) {
    return "full";
  }
  if (mediaQuery640.matches) {
    return "640";
  }
  if (mediaQuery500.matches) {
    return "500";
  }
  if (mediaQuery400.matches) {
    return "400";
  }
  return "small";
}

// check if screen height is too small
export function checkScreenHeight() {
  const mediaQueryFull = window.matchMedia("(max-height: 1000px)");
  return mediaQueryFull.matches;
}

export function getCorrectURL(someEndpoint) {
  const correctURL = new URL(someEndpoint, window.location.origin).href;
  return correctURL;
}
