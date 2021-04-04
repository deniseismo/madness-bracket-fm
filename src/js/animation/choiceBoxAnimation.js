//import anime from "../third-party/anime.es.js";
import anime from "animejs/lib/anime.es.js";
import { pickRandomElement } from "../utilities.js";
// random words used for text animation
const FLASHING_WORDS = {
  // words for ARTIST 'square choice box'
  artist: [
    "ADELE",
    "PRINCE",
    "QUEEN",
    "BOWIE",
    "U2",
    "RTJ",
    "WILCO",
    "MUSE",
    "ARTIST",
    "ARTIST",
    "ARTIST",
    "ARTIST",
  ],
  // words for CHARTS 'square choice box'
  charts: [
    "CHARTS",
    "TOP",
    "BEST",
    "PITCHFORK",
    "NME",
    "RS500",
    "CHARTS",
    "CHARTS",
    "CHARTS",
    "CHARTS",
  ],
};

// pick random paragraph (the word/words to animate afterwards) from the 'square box of choice'
function getRandomElement(squareChoiceBox) {
  // get all paragraphs from the box
  const allParagraphs = squareChoiceBox.querySelectorAll(":scope > p");
  // get a random paragraph
  const randomParagraphElement = pickRandomElement(allParagraphs);
  // figure out what this square box type is: artist or charts
  const choiceBoxType = squareChoiceBox.dataset.bracketType;
  // pick random text (artist/charts) to change to
  const randomWord = pickRandomElement(FLASHING_WORDS[choiceBoxType]);
  // change text content to a random word
  randomParagraphElement.textContent = randomWord;
  // split text into letters
  const letters = randomParagraphElement.textContent.split("");
  // wrap each letter in a span with the class='letter'
  const letterSpanElements = letters.map(
    (char) => `<span class="letter">${char}</span>`
  );
  // put span elements inside paragraph element
  randomParagraphElement.innerHTML = letterSpanElements.join("");
  // return random paragraph
  return randomParagraphElement;
}

// animates letters inside square boxes (artist or charts)
export function animateLetters(squareChoiceBox) {
  // stop/remove animation from paragraphs and span-letters
  anime.remove(["span", "p"]);
  // pick random paragraph element
  const randomElement = getRandomElement(squareChoiceBox);
  // select all letter-span elements inside paragraph
  const spanLetters = randomElement.querySelectorAll(":scope > span");
  const animation = anime
    .timeline({ loop: false })
    .add({
      targets: spanLetters,
      translateY: ["1.1em", 0],
      translateZ: 0,
      rotateY: [360, 0],
      duration: 750,
      delay: (el, i) => 50 * i,
      easing: "easeInQuint",
    })
    .add({
      targets: randomElement,
      scale: [2, 1],
    });
  animation.complete = function () {
    // restart animation with a newly random
    //randomElement.textContent = randomArtistName;
    animateLetters(squareChoiceBox);
  };
}
