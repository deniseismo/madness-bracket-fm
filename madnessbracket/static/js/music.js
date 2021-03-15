import { removeAllChildNodes } from "./utilities.js";
import { getIcon } from "./playButton.js";

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
        const playIcon = getIcon("play");
        button.appendChild(playIcon);
        button.dataset.status = "standby";
        button.classList.remove("play-icon_playing");
        button.classList.add("play-icon_standby");
      }
    });
    removeAllChildNodes(this);
    const pauseIcon = getIcon("pause");
    this.appendChild(pauseIcon);
    this.dataset.status = "playing";
    this.classList.remove("play-icon_standby");
    this.classList.add("play-icon_playing");
    playMusic(previewURL, this);
  } else {
    removeAllChildNodes(this);
    const playIcon = getIcon("play");
    this.appendChild(playIcon);
    this.classList.remove("play-icon_playing");
    this.classList.add("play-icon_standby");
    this.dataset.status = "standby";
    stopMusic();
  }
}
