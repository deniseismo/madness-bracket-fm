import SwiperCore, { Pagination } from "swiper/core";
SwiperCore.use([Pagination]);

import { createElement } from "../misc/utilities";
import { hideAll } from "tippy.js";
// transforms tournament bracket into a mobile-friendly slider (swiper.js)
export function transformBracketIntoSlider() {
  const mainContainer = document.querySelector(".main");
  const bracket = document.querySelector(".tournament-bracket");
  if (bracket) {
    const swiperContainer = createElement("div", ["swiper-container"]);
    const swiperWrapper = createElement("div", ["swiper-wrapper"]);

    swiperContainer.appendChild(swiperWrapper);
    const paginator = createElement("div", ["swiper-pagination"]);
    bracket.appendChild(swiperContainer);
    mainContainer.appendChild(paginator);

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

export function sliderInit(numberOfRounds) {
  const slider = new SwiperCore(".swiper-container", {
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
    console.log(slider.activeIndex);
    hideAll();
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

function getCurrentSwiper() {
  const swiper = document.querySelector(".swiper-container")?.swiper;
  console.log(swiper);
  return swiper;
}

export function returnToSlideZero() {
  const swiper = getCurrentSwiper();
  if (swiper) {
    console.log("getting you back to slide 0");
    swiper.slideTo(0, 150, true);
  }
}
