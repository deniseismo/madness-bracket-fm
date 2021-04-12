// generates svg given data
export function getSVGIcon(svgData) {
  const svgIcon = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  svgIcon.setAttribute("viewBox", "0 0 512 512");
  const paths = svgData.path;
  console.log("paths", paths);
  for (const pathProperties of paths) {
    console.log(pathProperties);
    const aPath = document.createElementNS(
      "http://www.w3.org/2000/svg",
      "path"
    );
    for (const prop in pathProperties) {
      aPath.setAttributeNS(null, prop, pathProperties[prop]);
    }
    svgIcon.appendChild(aPath);
  }
  if (svgData.hasOwnProperty("figures")) {
    for (const figureProperties of svgData["figures"]) {
      const aFigure = document.createElementNS(
        "http://www.w3.org/2000/svg",
        figureProperties["type"]
      );
      for (const prop in figureProperties) {
        if (prop !== "type") {
          aFigure.setAttributeNS(null, prop, figureProperties[prop]);
        }
      }
      svgIcon.appendChild(aFigure);
    }
  }
  return svgIcon;
}

// add width & height attributes to fix an html2canvas screenshot bug w/ svgs
export function fixSVGDimensions(svg, size) {
  svg.setAttribute("width", size);
  svg.setAttribute("height", size);
}
