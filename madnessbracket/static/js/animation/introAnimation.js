import anime from "../third-party/anime.es.js";

// animate intro/header lines and the title
export function introAnimation() {
  let tl = anime.timeline({
    easing: "easeInElastic(2, .9)",
    duration: 250,
  });

  tl.add({
    targets: ".horizontal-line",
    width: ["0", "150"],
  })
    .add({
      targets: ".vertical-line",
      height: ["0%", "100%"],
    })
    .add({
      targets: ".intro-line",
      width: ["0", "100"],
    })
    .add({
      targets: ".intro-title",
      opacity: ["0%", "100%"],
      easing: "spring(1, 80, 10, 0)",
    });
}
