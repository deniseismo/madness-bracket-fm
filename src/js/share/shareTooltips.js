import tippy from "tippy.js";

export function activateShareTooltips() {
  const twitterButton = document.querySelector(".button-twitter");
  const redditButton = document.querySelector(".button-reddit");
  const vkButton = document.querySelector(".button-vk");
  const facebookButton = document.querySelector(".button-facebook");
  const telegramButton = document.querySelector(".button-telegram");
  const screenshotButton = document.querySelector(".button-screenshot");
  const copyButton = document.querySelector(".button-copy");
  const buttons = [
    twitterButton,
    redditButton,
    vkButton,
    facebookButton,
    telegramButton,
    screenshotButton,
    copyButton,
  ];
  const titles = [
    "twitter",
    "reddit",
    "vk",
    "facebook",
    "telegram",
    "take screenshot",
    "copy link",
  ];
  const titledButtons = buttons.map(function (element, index) {
    return [element, titles[index]];
  });
  console.log(buttons);
  titledButtons.forEach((group) => {
    tippy(group[0], {
      arrow: true,
      placement: "bottom",
      content: group[1],
    });
  });
}
