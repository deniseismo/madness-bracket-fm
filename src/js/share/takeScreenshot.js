import html2canvas from "html2canvas";
import MicroModal from "micromodal";

// take screenshot & render it onto the page
export function takeScreenshot() {
  MicroModal.close("modal-1");
  html2canvas(document.querySelector(".wrapper")).then((canvas) => {
    canvas.classList.add("screenshot");
    document.body.addEventListener("click", closeScreenshot);
    document.body.appendChild(canvas);
  });
}
// close/remove screenshot
function closeScreenshot() {
  const screenshot = document.querySelector(".screenshot");
  if (screenshot) {
    screenshot.remove();
  }
  document.body.removeEventListener("click", closeScreenshot);
}
