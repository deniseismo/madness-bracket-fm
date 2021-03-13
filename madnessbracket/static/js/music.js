export var music = new Audio();
export function playMusic(url) {
  music.pause();
  music = new Audio(url);
  music.volume = 0.2;
  music.play();
}
