import Swiper from "swiper/bundle";
import { createElement } from "../misc/utilities";
// transforms tournament bracket into a mobile-friendly slider (swiper.js)
export function transformBracketIntoSlider() {
  const container = document.querySelector(".container");
  const bracket = document.querySelector(".tournament-bracket");
  if (bracket) {
    const swiperContainer = createElement("div", ["swiper-container"]);
    const swiperWrapper = createElement("div", ["swiper-wrapper"]);

    swiperContainer.appendChild(swiperWrapper);
    const paginator = createElement("div", ["swiper-pagination"]);
    bracket.appendChild(swiperContainer);
    console.log(container);
    container.appendChild(paginator);

    const rounds = document.querySelectorAll(".round");
    rounds.forEach((round) => {
      const slide = createElement("div", ["swiper-slide"]);
      swiperWrapper.appendChild(slide);
      slide.appendChild(round);
    });
  }
}

export function removeSlider() {
  const bracket = document.querySelector(".tournament-bracket");
  if (bracket) {
    const rounds = document.querySelectorAll(".round");
    rounds.forEach((round) => {
      bracket.appendChild(round);
    });
    const swiperContainer = document.querySelector(".swiper-container");
    if (swiperContainer) {
      swiperContainer.remove();
    }
    const paginator = document.querySelector(".swiper-pagination");
    if (paginator) {
      paginator.remove();
    }
  }
}

export function sliderInit() {
  const slider = new Swiper(".swiper-container", {
    // parameters
    direction: "horizontal",
    loop: false,
    centeredSlides: false,
    slidesPerView: "auto",

    pagination: {
      el: ".swiper-pagination",
      clickable: true,
    },
  });
  slider.on("slideChange", function () {
    const rounds = document.querySelectorAll(".round");
    const numberOfRounds = rounds.length;
    console.log(slider.activeIndex);
    const activeIndex = slider.activeIndex;
    console.log(Math.floor(numberOfRounds / 2));
    if (activeIndex === Math.floor(numberOfRounds / 2)) {
      console.log("MIDDLE!");
      slider.params.slidesPerView = 1;
    } else {
      slider.params.slidesPerView = 2;
    }
  });
}
