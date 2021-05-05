//import anime from "../third-party/anime.es.js";
import anime from "animejs/lib/anime.es.js";
import { pickRandomElement } from "../misc/utilities.js";
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
    "KANYE",
    "ARTIST",
    "M83",
    "PARAMORE",
  ],
  // words for CHARTS 'square choice box'
  charts: [
    "CHARTS",
    "TOP",
    "BEST",
    "PITCHFORK",
    "NME",
    "RS500",
    "CLASSICS",
    "CHARTS",
    "CHARTS",
    "CHARTS",
    "CHARTS",
  ],
  // words for SECRET 'square choice box'
  secret: [
    "SECRET",
    "WILD CARD",
    "???",
    "WAIT, WHAT?",
    "WHO KNOWS?",
    "SECRET",
    "SECRET",
    "SECRET",
    "SECRET",
    "SECRET",
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
  const letterSpanElements = letters.map((char) => {
    if (char === " ") {
      return `<span class="letter">&nbsp;</span>`;
    }
    return `<span class="letter">${char}</span>`;
  });
  // put span elements inside paragraph element
  randomParagraphElement.innerHTML = letterSpanElements.join("");
  // return random paragraph
  return randomParagraphElement;
}

// animates letters inside square boxes (artist or charts)
export function animateLetters(squareChoiceBox) {
  // pick random paragraph element
  const randomElement = getRandomElement(squareChoiceBox);
  // select all letter-span elements inside paragraph
  const spanLetters = randomElement.querySelectorAll(":scope > span");
  const animation = anime
    .timeline({ loop: false })
    .add({
      targets: spanLetters,
      rotateX: [360, 0],
      opacity: [0.5, 1],
      duration: 300,
      delay: (el, i) => 10 * i,
      easing: "cubicBezier(.06,.74,.7,.08)",
    })
    .add({
      targets: randomElement,
      scale: [2, 1],
    });
  animation.complete = function () {
    // restart animation with a newly random
    animateLetters(squareChoiceBox);
  };
}

export function deanimateLetters(squareChoiceBox) {
  const squareButtons = document.querySelectorAll(".square-button");
  squareButtons.forEach((button) => {
    if (button !== squareChoiceBox) {
      const paragraphs = button.querySelectorAll(":scope > p");
      //console.log("paragraphs:", paragraphs);
      paragraphs.forEach((paragraph) => {
        const spanLetters = paragraph.querySelectorAll(":scope > span");
        if (spanLetters) {
          const spanLettersAnimation = anime({
            targets: spanLetters,
            rotateX: [0],
            opacity: [1],
            duration: 50,
            delay: (el, i) => 10 * i,
            easing: "cubicBezier(.07,1.2,.31,1.16)",
          });
        }
        const paragraphAnimation = anime({
          targets: paragraph,
          scale: [1],
        });
      });
    }
  });
  setTimeout(() => {
    anime.remove(["span", "p"]);
  }, 100);
}
