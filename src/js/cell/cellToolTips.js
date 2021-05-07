import tippy from "tippy.js";

// add tooltips to the corresponding cell: used to hint artist's name
export function addTooltipToCell(cell, content, side) {
  // left-sided cells get the right-sided tooltips, and vice-versa
  const placement = side === "left" ? "right" : "left";
  cell.setTooltip(
    tippy(cell.element, {
      arrow: true,
      placement: placement,
      content: content,
    })
  );
}
