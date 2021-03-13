// Durstenfeld shuffle © https://www.wikiwand.com/en/Fisher%E2%80%93Yates_shuffle
export function shuffleArray(array) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
}

export function createElement(type, classes) {
  const element = document.createElement(type);
  for (const aClass of classes) {
    element.classList.add(aClass);
  }
  return element;
}

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

export function removeAllChildNodes(parent) {
  while (parent.firstChild) {
    parent.removeChild(parent.firstChild);
  }
}
