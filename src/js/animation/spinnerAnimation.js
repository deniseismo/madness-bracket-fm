import anime from "animejs/lib/anime.es.js";

export function animateSpinner() {
  let tl = anime.timeline({
    duration: 300, // Can be inherited
    easing: "easeOutExpo", // Can be inherited
    direction: "alternate", // Is not inherited
    loop: true,
  });

  tl.add({
    targets: ".spinner .horizontal-line",
    width: ["0", "150"],
  })
    .add({
      targets: ".spinner .vertical-line",
      height: ["0%", "100%"],
    })
    .add({
      targets: ".spinner .median-line",
      width: ["0", "100"],
    })
    .add({
      targets: ".spinner",
      rotate: 180,
    });
}
export function killSpinnerAnimation() {
  const spinner = document.querySelector(".spinner");
  const spinnerParts = spinner.querySelectorAll(":scope > div");
  anime.remove(spinner, spinnerParts);
}
