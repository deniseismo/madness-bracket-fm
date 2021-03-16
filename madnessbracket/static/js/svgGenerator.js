export function getSVGIcon(svgData) {
  const svgIcon = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  svgIcon.classList.add("play-icon");
  svgIcon.setAttribute("viewBox", "0 0 512 512");
  const aPath = document.createElementNS("http://www.w3.org/2000/svg", "path");
  const pathProperties = svgData.path;
  for (const prop in pathProperties) {
    aPath.setAttributeNS(null, prop, pathProperties[prop]);
  }
  svgIcon.appendChild(aPath);
  return svgIcon;
}
