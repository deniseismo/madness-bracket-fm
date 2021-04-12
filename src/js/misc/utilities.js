// Durstenfeld shuffle © https://www.wikiwand.com/en/Fisher%E2%80%93Yates_shuffle
export function shuffleArray(array) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
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
