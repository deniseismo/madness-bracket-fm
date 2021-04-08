import tippy from "tippy.js";

export function addTooltipToCell(cell, content, side) {
  const placement = side === "left" ? "right" : "left";
  cell.setTooltip(
    tippy(cell.element, {
      arrow: true,
      placement: placement,
      content: content,
    })
  );
}
