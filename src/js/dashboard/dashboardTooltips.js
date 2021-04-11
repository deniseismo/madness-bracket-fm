import tippy from "tippy.js";

export function activateDashboardTooltips() {
  tippy(".button-reset", {
    arrow: true,
    placement: "bottom",
    content: "reset",
  });
  tippy(".button-shuffle", {
    arrow: true,
    placement: "bottom",
    content: "shuffle",
  });
  tippy(".button-retry", {
    arrow: true,
    placement: "bottom",
    content: "new tracks",
  });
  tippy(".button-share", {
    arrow: true,
    placement: "bottom",
    content: "share",
  });
}
