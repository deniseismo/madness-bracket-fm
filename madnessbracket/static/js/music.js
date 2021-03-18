import { PlayButton } from "./playButton.js";

export var music = new Audio();
export function playMusic(url, button) {
  music.pause();
  music = new Audio(url);
  music.volume = 0.2;
  music.play();
  music.onended = function () {
    PlayButton.changePlayButtonIcon(button, "play");
  };
}

export function stopMusic() {
  music.pause();
}
