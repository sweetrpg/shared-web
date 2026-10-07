/* Shared "Report a problem / request a feature" widget - see feedback-widget.css and this
 * repo's README for the embed contract. Plain DOM APIs, no build step, matching
 * avatar-menu.js/app-switcher.js's style so any *-web frontend (Flask, Rust+Askama, ...) can
 * embed it with just a <script> tag - the widget builds and mounts its own markup rather than
 * requiring the host to render a matching template, since hosts don't all share one templating
 * language.
 *
 * Config is read from this script tag's own data attributes (via document.currentScript, so it
 * must stay a plain synchronous <script src="...">, not loaded as a module or injected
 * dynamically after the fact):
 *   data-api-url           (required) full URL of admin-api's POST /feedback endpoint
 *   data-trigger-selector  (optional) CSS selector for host-provided trigger element(s); when
 *                          absent, the widget injects its own floating trigger button
 *   data-trigger-label     (optional) label for the auto-injected trigger button
 *   data-source            (optional) value sent as the submission's "source" field; defaults
 *                          to the page's location
 */
(function () {
  var scriptEl = document.currentScript;
  if (!scriptEl) {
    return;
  }

  var config = {
    apiUrl: scriptEl.getAttribute('data-api-url'),
    triggerSelector: scriptEl.getAttribute('data-trigger-selector'),
    triggerLabel: scriptEl.getAttribute('data-trigger-label') || 'Report a problem / request a feature',
    source: scriptEl.getAttribute('data-source') || (window.location.hostname + window.location.pathname),
  };

  if (!config.apiUrl) {
    return;
  }

  var TITLE_MAX = 200;
  var BODY_MAX = 5000;

  var dialogState = null;

  function buildDialog() {
    var backdrop = document.createElement('div');
    backdrop.className = 'feedback-backdrop';
    backdrop.hidden = true;

    var dialog = document.createElement('div');
    dialog.className = 'feedback-dialog';
    dialog.setAttribute('role', 'dialog');
    dialog.setAttribute('aria-modal', 'true');
    dialog.setAttribute('aria-labelledby', 'feedback-widget-heading');

    var heading = document.createElement('h2');
    heading.id = 'feedback-widget-heading';
    heading.textContent = 'Report a problem or request a feature';

    var form = document.createElement('form');
    form.setAttribute('novalidate', 'novalidate');

    var typeField = fieldWrapper('feedback-widget-type', 'Type', selectEl());
    var titleField = fieldWrapper('feedback-widget-title', 'Title', textInputEl());
    var bodyField = fieldWrapper('feedback-widget-body', 'Description', textareaEl());
    var emailField = fieldWrapper('feedback-widget-email', 'Your email (optional)', emailInputEl());

    var honeypot = document.createElement('input');
    honeypot.className = 'feedback-honeypot';
    honeypot.type = 'text';
    honeypot.name = 'website';
    honeypot.tabIndex = -1;
    honeypot.setAttribute('aria-hidden', 'true');
    honeypot.setAttribute('autocomplete', 'off');

    var status = document.createElement('div');
    status.className = 'feedback-status';
    status.setAttribute('role', 'status');
    status.setAttribute('aria-live', 'polite');

    var actions = document.createElement('div');
    actions.className = 'feedback-actions';

    var cancelBtn = document.createElement('button');
    cancelBtn.type = 'button';
    cancelBtn.className = 'btn btn-secondary';
    cancelBtn.textContent = 'Cancel';

    var submitBtn = document.createElement('button');
    submitBtn.type = 'submit';
    submitBtn.className = 'btn btn-primary';
    submitBtn.textContent = 'Submit';

    actions.appendChild(cancelBtn);
    actions.appendChild(submitBtn);

    form.appendChild(typeField.wrapper);
    form.appendChild(titleField.wrapper);
    form.appendChild(bodyField.wrapper);
    form.appendChild(emailField.wrapper);
    form.appendChild(honeypot);
    form.appendChild(status);
    form.appendChild(actions);

    dialog.appendChild(heading);
    dialog.appendChild(form);
    backdrop.appendChild(dialog);
    document.body.appendChild(backdrop);

    return {
      backdrop: backdrop,
      dialog: dialog,
      form: form,
      typeInput: typeField.control,
      titleInput: titleField.control,
      bodyInput: bodyField.control,
      emailInput: emailField.control,
      honeypot: honeypot,
      status: status,
      submitBtn: submitBtn,
      cancelBtn: cancelBtn,
      openedAt: null,
      lastFocused: null,
    };
  }

  function fieldWrapper(id, labelText, control) {
    var wrapper = document.createElement('div');
    wrapper.className = 'feedback-field';

    var label = document.createElement('label');
    label.setAttribute('for', id);
    label.textContent = labelText;

    control.id = id;
    wrapper.appendChild(label);
    wrapper.appendChild(control);

    return { wrapper: wrapper, control: control };
  }

  function selectEl() {
    var select = document.createElement('select');
    select.className = 'input';
    select.name = 'type';

    var bugOpt = document.createElement('option');
    bugOpt.value = 'bug';
    bugOpt.textContent = 'Bug';

    var featureOpt = document.createElement('option');
    featureOpt.value = 'feature';
    featureOpt.textContent = 'Feature request';

    select.appendChild(bugOpt);
    select.appendChild(featureOpt);
    return select;
  }

  function textInputEl() {
    var input = document.createElement('input');
    input.className = 'input';
    input.type = 'text';
    input.name = 'title';
    input.required = true;
    input.maxLength = TITLE_MAX;
    return input;
  }

  function textareaEl() {
    var textarea = document.createElement('textarea');
    textarea.className = 'input';
    textarea.name = 'body';
    textarea.required = true;
    textarea.maxLength = BODY_MAX;
    textarea.rows = 5;
    return textarea;
  }

  function emailInputEl() {
    var input = document.createElement('input');
    input.className = 'input';
    input.type = 'email';
    input.name = 'reporter_email';
    return input;
  }

  function setStatus(state, message) {
    dialogState.status.textContent = message || '';
    dialogState.status.classList.remove('banner', 'banner-error', 'banner-success');
    if (state === 'error') {
      dialogState.status.classList.add('banner', 'banner-error');
      dialogState.status.setAttribute('role', 'alert');
    } else if (state === 'success') {
      dialogState.status.classList.add('banner', 'banner-success');
      dialogState.status.setAttribute('role', 'status');
    } else {
      dialogState.status.setAttribute('role', 'status');
    }
  }

  function resetForm() {
    dialogState.typeInput.value = 'bug';
    dialogState.titleInput.value = '';
    dialogState.bodyInput.value = '';
    dialogState.emailInput.value = '';
    dialogState.honeypot.value = '';
    setStatus(null, '');
  }

  function openDialog() {
    if (!dialogState) {
      dialogState = buildDialog();
      wireDialog();
    }

    dialogState.lastFocused = document.activeElement;
    dialogState.openedAt = Date.now();
    dialogState.backdrop.hidden = false;
    dialogState.typeInput.focus();
  }

  function closeDialog() {
    if (!dialogState) {
      return;
    }
    dialogState.backdrop.hidden = true;
    if (dialogState.lastFocused && typeof dialogState.lastFocused.focus === 'function') {
      dialogState.lastFocused.focus();
    }
  }

  function trapFocus(event) {
    var focusable = dialogState.dialog.querySelectorAll(
      'input, select, textarea, button, [href]'
    );
    if (!focusable.length) {
      return;
    }
    var first = focusable[0];
    var last = focusable[focusable.length - 1];

    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  }

  function wireDialog() {
    dialogState.cancelBtn.addEventListener('click', closeDialog);

    dialogState.backdrop.addEventListener('click', function (event) {
      if (event.target === dialogState.backdrop) {
        closeDialog();
      }
    });

    dialogState.backdrop.addEventListener('keydown', function (event) {
      if (event.key === 'Escape') {
        closeDialog();
        return;
      }
      if (event.key === 'Tab') {
        trapFocus(event);
      }
    });

    dialogState.form.addEventListener('submit', function (event) {
      event.preventDefault();
      submitForm();
    });
  }

  function submitForm() {
    var title = dialogState.titleInput.value.trim();
    var body = dialogState.bodyInput.value.trim();

    if (!title || !body) {
      setStatus('error', 'Title and description are both required.');
      return;
    }

    var payload = {
      type: dialogState.typeInput.value,
      title: title,
      body: body,
      source: config.source,
      website: dialogState.honeypot.value,
      started_at: new Date(dialogState.openedAt).toISOString(),
    };

    var email = dialogState.emailInput.value.trim();
    if (email) {
      payload.reporter_email = email;
    }

    dialogState.submitBtn.disabled = true;
    setStatus(null, '');

    fetch(config.apiUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    })
      .then(function (response) {
        dialogState.submitBtn.disabled = false;
        if (response.ok) {
          dialogState.titleInput.value = '';
          dialogState.bodyInput.value = '';
          dialogState.emailInput.value = '';
          dialogState.honeypot.value = '';
          setStatus('success', "Thanks - we've logged this.");
          return;
        }
        if (response.status === 429) {
          setStatus('error', "You've submitted a few of these recently - please try again in a bit.");
          return;
        }
        setStatus('error', "That didn't go through. Please try again shortly.");
      })
      .catch(function () {
        dialogState.submitBtn.disabled = false;
        setStatus('error', "That didn't go through. Please check your connection and try again.");
      });
  }

  function attachTriggers() {
    if (config.triggerSelector) {
      var hostTriggers = document.querySelectorAll(config.triggerSelector);
      hostTriggers.forEach(function (el) {
        el.addEventListener('click', openDialog);
      });
      return;
    }

    var trigger = document.createElement('button');
    trigger.type = 'button';
    trigger.className = 'btn btn-primary feedback-trigger';
    trigger.textContent = config.triggerLabel;
    trigger.addEventListener('click', openDialog);
    document.body.appendChild(trigger);
  }

  document.addEventListener('DOMContentLoaded', attachTriggers);

  // Exposed for hosts that want to trigger the dialog programmatically (e.g. from a menu item
  // that isn't known at load time) instead of relying on data-trigger-selector.
  window.SweetRPGFeedbackWidget = { open: openDialog, close: closeDialog, resetForm: resetForm };
})();
