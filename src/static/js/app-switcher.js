/* App switcher grid, shared by main-web, catalog-web, and admin-web - see the
 * suite-app-switcher-nav OpenSpec change in sweetrpg/platform. Mirrors avatar-menu.js's
 * open/close/focus behavior so the two triggers behave identically.
 */
(function () {
  function closePanel(panel, trigger) {
    panel.hidden = true;
    trigger.setAttribute('aria-expanded', 'false');
  }

  function openPanel(panel, trigger) {
    panel.hidden = false;
    trigger.setAttribute('aria-expanded', 'true');
  }

  function initSwitcher(switcher) {
    const trigger = switcher.querySelector('.app-switcher-trigger');
    const panel = switcher.querySelector('.app-switcher-panel');
    if (!trigger || !panel) {
      return;
    }

    trigger.setAttribute('aria-haspopup', 'true');
    trigger.setAttribute('aria-expanded', 'false');
    closePanel(panel, trigger);

    trigger.addEventListener('click', function (event) {
      event.stopPropagation();
      if (panel.hidden) {
        openPanel(panel, trigger);
      } else {
        closePanel(panel, trigger);
      }
    });

    panel.addEventListener('click', function (event) {
      const item = event.target.closest('.app-switcher-item');
      if (item) {
        closePanel(panel, trigger);
      }
    });

    document.addEventListener('click', function (event) {
      if (!panel.hidden && !switcher.contains(event.target)) {
        closePanel(panel, trigger);
      }
    });

    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && !panel.hidden) {
        closePanel(panel, trigger);
        trigger.focus();
      }
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.app-switcher').forEach(initSwitcher);
  });
})();
