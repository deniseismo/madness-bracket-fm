import anime from "animejs/lib/anime.es.js";
import { getScreenSize } from "../misc/utilities.js";

// get intro lines sizes (max width size) depending on screen size
function getResponsiveIntroLineSizes() {
  const screenSize = getScreenSize();
  console.log(screenSize);
  if (screenSize === "full") {
    return ["8rem", "7rem"];
  }
  if (screenSize === "640") {
    return ["6rem", "5rem"];
  }
  if (screenSize === "500") {
    return ["5rem", "4rem"];
  }
  if (screenSize === "400") {
    return ["4rem", "3rem"];
  }
  if (screenSize === "small") {
    return ["3.5rem", "2.5rem"];
  }
}

// animate intro/header lines and the title
export function introAnimation() {
  const [
    horizontalLineMaxSize,
    introLineMaxSize,
  ] = getResponsiveIntroLineSizes();
  console.log(horizontalLineMaxSize, introLineMaxSize);
  let tl = anime.timeline({
    easing: "easeInElastic(2, .9)",
    duration: 250,
  });

  tl.add({
    targets: ".horizontal-line",
    width: ["0rem", horizontalLineMaxSize],
  })
    .add({
      targets: ".vertical-line",
      height: ["0%", "100%"],
    })
    .add({
      targets: ".intro-line",
      width: ["0rem", introLineMaxSize],
    })
    .add({
      targets: ".intro-title",
      opacity: ["0%", "100%"],
      easing: "spring(1, 80, 10, 0)",
    });
}
