import { getSVGIcon } from "../misc/svgGenerator";
import { createElement } from "../misc/utilities";
import { appIconsSVGData } from "../misc/appIcons.js";
import tippy from "tippy.js";

export function activateMaxSizeTooltip() {
  tippy(".max-size-tooltip", {
    arrow: true,
    placement: "right",
    allowHTML: true,
    content: "bracket size: i.e. <i>maximum</i> number of tracks",
  });
}

export function addMaxSizeTooltip() {
  const maxSizeOptionsContainer = document.querySelector(
    ".bracket_max_size_container"
  );
  const maxSizeTooltip = createElement("div", ["max-size-tooltip"]);
  const maxSizeTooltipIcon = getSVGIcon(appIconsSVGData["help"]);
  maxSizeTooltipIcon.classList.add("max-size-tooltip-icon");
  maxSizeTooltip.appendChild(maxSizeTooltipIcon);
  maxSizeOptionsContainer.appendChild(maxSizeTooltip);
  activateMaxSizeTooltip();
}
