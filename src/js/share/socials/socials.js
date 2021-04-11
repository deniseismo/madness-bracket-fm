export function socialShareInit(url, title) {
  const twitterButton = document.querySelector(".button-twitter");
  const redditButton = document.querySelector(".button-reddit");
  const vkButton = document.querySelector(".button-vk");
  const facebookButton = document.querySelector(".button-facebook");
  const telegramButton = document.querySelector(".button-telegram");

  const shareUrl = encodeURI(url);
  const shareTitle = encodeURI(`Here's my madnessbracket for ${title}`);

  twitterButton.setAttribute(
    "href",
    `https://twitter.com/share?url=${shareUrl}&text=${shareTitle}&hashtags=madnessbracket`
  );
  redditButton.setAttribute(
    "href",
    `https://reddit.com/submit?url=${shareUrl}&title=${shareTitle}`
  );
  vkButton.setAttribute(
    "href",
    `https://vk.com/share.php?url=${shareUrl}&title=${shareTitle}`
  );
  facebookButton.setAttribute(
    "href",
    `https://www.facebook.com/sharer.php?u=${shareUrl}`
  );
  telegramButton.setAttribute(
    "href",
    `https://t.me/share/url?url=${shareUrl}&text=${shareTitle}`
  );
  [
    twitterButton,
    redditButton,
    vkButton,
    facebookButton,
    telegramButton,
  ].forEach((button) => {
    button.setAttribute("target", "_blank");
    button.setAttribute("rel", "noopener");
  });
}
