/* Navigation and the homepage link checker. */
(function () {
  'use strict';

  var toggle = document.querySelector('.nav-toggle');
  var nav = document.querySelector('.nav');
  if (toggle && nav) {
    nav.id = nav.id || 'site-nav';
    toggle.setAttribute('aria-controls', nav.id);

    function setNav(open) {
      nav.setAttribute('data-open', open ? 'true' : 'false');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    }
    toggle.addEventListener('click', function (e) {
      e.stopPropagation();
      setNav(nav.getAttribute('data-open') !== 'true');
    });
    // The panel covers the page, so Escape and a tap outside are the two
    // exits people reach for. Neither worked.
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.getAttribute('data-open') === 'true') {
        setNav(false);
        toggle.focus();
      }
    });
    document.addEventListener('click', function (e) {
      if (nav.getAttribute('data-open') === 'true' && !nav.contains(e.target)) {
        setNav(false);
      }
    });
  }

  var input = document.getElementById('check-url');
  var out = document.getElementById('check-out');
  if (!input || !out || !window.TrustScanSafety) return;

  var LABEL = {
    safe: 'Looks safe',
    caution: 'Open with caution',
    danger: 'Dangerous link'
  };

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;   // textContent, never innerHTML
    return n;
  }

  function run() {
    // Built as DOM nodes rather than an HTML string. Part of every finding is
    // derived from the URL the visitor typed — the TLD, for one — and this is
    // a page about link safety. Escaping by hand is a bug waiting to happen;
    // textContent cannot be escaped wrongly.
    out.textContent = '';
    var value = input.value.trim();

    if (!value) {
      out.setAttribute('data-level', '');
      out.appendChild(el('p', 'none',
        'Paste a link to check it. Nothing you type here leaves your browser.'));
      return;
    }

    var r = window.TrustScanSafety.check(value);
    out.setAttribute('data-level', r.level);
    out.appendChild(el('div', 'verdict-head', LABEL[r.level]));
    // aria-live reads the box in DOM order, so the verdict word lands first.

    if (!r.reasons.length) {
      out.appendChild(el('p', 'none', 'No risks found across the 21 checks.'));
      return;
    }
    var ul = document.createElement('ul');
    r.reasons.forEach(function (reason) {
      ul.appendChild(el('li', null, reason));
    });
    out.appendChild(ul);
  }

  var timer;
  input.addEventListener('input', function () {
    clearTimeout(timer);
    timer = setTimeout(run, 180);
  });

  Array.prototype.forEach.call(
    document.querySelectorAll('[data-sample]'), function (b) {
      b.addEventListener('click', function () {
        input.value = b.getAttribute('data-sample');
        run();
        input.focus();
      });
    });

  run();
})();
