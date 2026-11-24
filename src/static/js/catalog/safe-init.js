/**
 * Fail-soft wrapper for hosted behavior scripts (PADR-0045).
 *
 * Runs `init(root)` for each element matching `selector`. A throwing init is logged and
 * contained so other scripts on the page keep working; the element is marked
 * `data-script-state="failed"` so CSS can keep its controls inert or hidden. A successful
 * init sets `data-script-state="ready"`. Elements stay `pending` until a script initializes
 * them, so a script that never loads leaves its controls in the `pending` state.
 */
export function safeInit(selector, init, doc = document, log = console) {
  for (const root of doc.querySelectorAll(selector)) {
    try {
      init(root);
      root.dataset.scriptState = 'ready';
    } catch (err) {
      root.dataset.scriptState = 'failed';
      log.error(`script init failed for ${selector}`, err);
    }
  }
}
