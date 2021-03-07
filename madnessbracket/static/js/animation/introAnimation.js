import anime from "../third-party/anime.es.js";

export function introAnimation() {
  // Create a timeline with default parameters
  var tl = anime.timeline({
    easing: "easeInElastic(2, .9)", /* "easeInElastic(1, .6)", */
    duration: 250,
  });

  tl.add({
    targets: ".horizontal-line",
    width: ["0", "150"],
    // borderRight: ['0px solid white', '5px solid white'],
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
      easing: 'spring(1, 80, 10, 0)'
    });
}
