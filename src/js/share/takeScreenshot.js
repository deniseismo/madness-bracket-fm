import html2canvas from "html2canvas";

export function takeScreenshot() {
  html2canvas(document.querySelector(".wrapper")).then((canvas) => {
    canvas.toBlob(function (blob) {
      // Generate file download
      window.saveAs(blob, "madnessbracket.png");
    });
  });
}
