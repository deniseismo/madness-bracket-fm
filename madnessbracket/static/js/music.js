import { removeAllChildNodes } from "./utilities.js";
import { getSVGIcon } from "./svgGenerator.js";
import { playButtonSVGData } from "./playButton.js";

export var music = new Audio();
export function playMusic(url, button) {
  music.pause();
  music = new Audio(url);
  music.volume = 0.2;
  music.play();
  music.onended = function () {
    alert("audio playback has ended");
  };
}

export function stopMusic() {
  music.pause();
}

export function handlePlayButton(previewURL) {
  console.log(this);
  if (this.dataset.status === "standby") {
    const allButtons = document.querySelectorAll(".play-button");
    allButtons.forEach((button) => {
      if (button.dataset.status !== "standby") {
        removeAllChildNodes(button);
        const playIcon = getSVGIcon(playButtonSVGData["play"]);
        playIcon.classList.add("play-icon");
        button.appendChild(playIcon);
        button.dataset.status = "standby";
        button.classList.remove("play-icon_playing");
        button.classList.add("play-icon_standby");
      }
    });
    removeAllChildNodes(this);
    const pauseIcon = getSVGIcon(playButtonSVGData["pause"]);
    pauseIcon.classList.add("play-icon");
    this.appendChild(pauseIcon);
    this.dataset.status = "playing";
    this.classList.remove("play-icon_standby");
    this.classList.add("play-icon_playing");
    playMusic(previewURL, this);
  } else {
    removeAllChildNodes(this);
    const playIcon = getSVGIcon(playButtonSVGData["play"]);
    playIcon.classList.add("play-icon");
    this.appendChild(playIcon);
    this.classList.remove("play-icon_playing");
    this.classList.add("play-icon_standby");
    this.dataset.status = "standby";
    stopMusic();
  }
}
