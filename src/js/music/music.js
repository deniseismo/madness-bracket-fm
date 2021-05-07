import { PlayButton } from "./playButton.js";

export let music = new Audio();

// play music handler
export function playMusic(url, button) {
  music.pause();
  music = new Audio(url);
  music.volume = 0.2;
  music.play();
  // change play icon to pause when finished playing
  music.onended = function () {
    PlayButton.changePlayButtonIcon(button, "play");
  };
}

// stop music
export function stopMusic() {
  music.pause();
}
