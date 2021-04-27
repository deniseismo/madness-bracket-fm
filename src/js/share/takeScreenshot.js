import MicroModal from "micromodal";
import { hideAll } from "tippy.js";

// take screenshot & render it onto the page
export async function takeScreenshot() {
  MicroModal.close("modal-1");
  const html2canvas = await import("html2canvas");
  html2canvas.default(document.querySelector(".wrapper")).then((canvas) => {
    canvas.classList.add("screenshot");
    document.body.addEventListener("click", closeScreenshot);
    document.body.appendChild(canvas);
  });
  hideAll();
}
// close/remove screenshot
function closeScreenshot() {
  const screenshot = document.querySelector(".screenshot");
  if (screenshot) {
    screenshot.remove();
  }
  document.body.removeEventListener("click", closeScreenshot);
}
