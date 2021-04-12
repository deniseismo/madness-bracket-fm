import anime from "animejs/lib/anime.es.js";
import { doesArrayContainSomethingTruthy } from "../misc/utilities.js";

// animate bracket: the way rounds & cells appear on the screen
export function bracketAnimation(numberOfRounds) {
  const tl = anime.timeline({
    easing: "easeOutBounce",
    duration: 250,
  });
  // select rounds on both side consecutively
  const rounds = [];
  for (let i = 0; i < numberOfRounds; i++) {
    const round = [
      document.querySelector(`.left-${i}`),
      document.querySelector(`.right-${i}`),
    ];
    rounds.push(round);
  }
  const finalRound = [document.querySelector(".final-round")];
  rounds.push(finalRound);
  // animate each round on both sides consecutively (starting from round 1)
  rounds.forEach((round) => {
    // check if array contains truthy values in case the round does not exist
    if (doesArrayContainSomethingTruthy(round)) {
      tl.add({
        targets: round,
        opacity: [0, 1],
      });
    }
  });
}
