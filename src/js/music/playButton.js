import { playMusic, stopMusic } from "./music.js";
import { removeAllChildNodes } from "../misc/utilities.js";
import { getSVGIcon } from "../misc/svgGenerator.js";
export const playButtonSVGData = {
  play: {
    path: [
      {
        d:
          "M112 111v290c0 17.44 17 28.52 31 20.16l247.9-148.37c12.12-7.25 12.12-26.33 0-33.58L143 90.84c-14-8.36-31 2.72-31 20.16z",
        fill: "none",
        stroke: "currentColor",
        "stroke-miterlimit": "10",
        "stroke-width": "32",
      },
    ],
  },
  pause: {
    path: [
      {
        d: "M176 96h16v320h-16zM320 96h16v320h-16z",
        fill: "none",
        stroke: "currentColor",
        "stroke-linecap": "round",
        "stroke-linejoin": "round",
        "stroke-width": "32",
      },
    ],
  },
};

export class PlayButton {
  constructor(playButtonElement, previewURL) {
    this.playButtonElement = playButtonElement;
    this.previewURL = previewURL;
  }
  playPause() {
    if (this.playButtonElement.dataset.status === "standby") {
      this.resetAllButtons();
      this.playButtonElement.dataset.status = "playing";
      PlayButton.changePlayButtonIcon(this.playButtonElement, "pause");
      this.playButtonElement.classList.remove("play-icon_standby");
      this.playButtonElement.classList.add("play-icon_playing");
      playMusic(this.previewURL, this.playButtonElement);
    } else {
      this.playButtonElement.dataset.status = "standby";
      PlayButton.changePlayButtonIcon(this.playButtonElement, "play");
      this.playButtonElement.classList.remove("play-icon_playing");
      this.playButtonElement.classList.add("play-icon_standby");
      stopMusic();
    }
  }
  resetAllButtons() {
    const allButtons = document.querySelectorAll(".play-button");
    allButtons.forEach((button) => {
      if (button.dataset.status !== "standby") {
        PlayButton.changePlayButtonIcon(button, "play");
        button.dataset.status = "standby";
        button.classList.remove("play-icon_playing");
        button.classList.add("play-icon_standby");
      }
    });
  }
  static changePlayButtonIcon(buttonToChange, iconType) {
    removeAllChildNodes(buttonToChange);
    const pauseIcon = getSVGIcon(playButtonSVGData[iconType]);
    pauseIcon.classList.add("play-icon");
    buttonToChange.appendChild(pauseIcon);
  }
}
