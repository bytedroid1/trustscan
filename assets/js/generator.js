/* QR generator UI.
 *
 * One page per QR type; the page declares which one via <body data-qr-type>.
 * Field definitions and payload builders come from types.js, which build.py
 * generates from the same spec that writes the pages — so a new type is one
 * dict entry, never two files that can drift apart.
 *
 * Everything runs in this tab. Nothing typed here is uploaded.
 */
(function () {
  'use strict';

  var typeId = document.body.getAttribute('data-qr-type');
  var spec = window.QR_TYPES && window.QR_TYPES[typeId];
  var elFields = document.getElementById('gen-fields');
  var elCanvas = document.getElementById('gen-canvas');
  if (!spec || !elFields || !elCanvas) return;

  var elMeta = document.getElementById('gen-meta');
  var elError = document.getElementById('gen-error');

  var state = {
    values: {}, ecc: 'M', shape: 'rounded', eye: 'rounded',
    fg: '#10111A', eyeColor: '#0B5CFF', bg: '#FFFFFF',
    logo: null, matrix: null
  };

  // --- fields --------------------------------------------------------------

  spec.fields.forEach(function (f) {
    var wrap = document.createElement('div');
    wrap.className = 'field';
    var id = 'f-' + f.name;

    var lab = document.createElement('label');
    lab.setAttribute('for', id);
    lab.textContent = f.label;
    wrap.appendChild(lab);

    var input;
    if (f.el === 'textarea') {
      input = document.createElement('textarea');
    } else if (f.el === 'select') {
      input = document.createElement('select');
      f.options.forEach(function (o) {
        var opt = document.createElement('option');
        opt.value = o[0];
        opt.textContent = o[1];
        input.appendChild(opt);
      });
      state.values[f.name] = f.options[0][0];
    } else {
      input = document.createElement('input');
      input.type = f.type || 'text';
    }
    input.id = id;
    if (f.placeholder) input.placeholder = f.placeholder;
    input.addEventListener('input', function () {
      state.values[f.name] = input.value; render();
    });
    input.addEventListener('change', function () {
      state.values[f.name] = input.value; render();
    });
    wrap.appendChild(input);
    elFields.appendChild(wrap);
  });

  // --- drawing -------------------------------------------------------------

  function isEye(x, y, size) {
    return (x < 7 && y < 7) || (x >= size - 7 && y < 7) || (x < 7 && y >= size - 7);
  }

  function roundRect(ctx, x, y, w, h, r) {
    r = Math.min(r, w / 2, h / 2);
    ctx.beginPath();
    ctx.moveTo(x + r, y);
    ctx.arcTo(x + w, y, x + w, y + h, r);
    ctx.arcTo(x + w, y + h, x, y + h, r);
    ctx.arcTo(x, y + h, x, y, r);
    ctx.arcTo(x, y, x + w, y, r);
    ctx.closePath();
    ctx.fill();
  }

  function drawModule(ctx, px, py, s, shape) {
    var pad = s * 0.06;
    var x = px + pad, y = py + pad, d = s - pad * 2;
    if (shape === 'dots') {
      ctx.beginPath();
      ctx.arc(x + d / 2, y + d / 2, d / 2, 0, Math.PI * 2);
      ctx.fill();
    } else if (shape === 'diamond') {
      ctx.beginPath();
      ctx.moveTo(x + d / 2, y);
      ctx.lineTo(x + d, y + d / 2);
      ctx.lineTo(x + d / 2, y + d);
      ctx.lineTo(x, y + d / 2);
      ctx.closePath();
      ctx.fill();
    } else if (shape === 'rounded') {
      roundRect(ctx, x, y, d, d, d * 0.34);
    } else {
      ctx.fillRect(px, py, s, s);
    }
  }

  /** The three finder patterns, drawn as one shape rather than 49 modules.
   *
   * The middle ring is painted in the background colour rather than punched
   * out with destination-out — that composite mode erases the background fill
   * as well, which looks fine on a white page and exports a PNG with
   * transparent holes in all three corners.
   */
  function drawEye(ctx, cx, cy, s, style) {
    var outer = s * 7, ring = s;
    var r = style === 'circle' ? outer / 2
      : style === 'rounded' ? outer * 0.26
        : style === 'leaf' ? outer * 0.44 : 0;

    // Outer.
    ctx.fillStyle = state.eyeColor;
    if (style === 'leaf') leafPath(ctx, cx, cy, outer, r); else
      roundRect(ctx, cx, cy, outer, outer, r);

    // Ring, in the background colour.
    ctx.fillStyle = state.bg;
    var i1 = outer - ring * 2, r1 = Math.max(0, r - ring);
    if (style === 'leaf') leafPath(ctx, cx + ring, cy + ring, i1, r1); else
      roundRect(ctx, cx + ring, cy + ring, i1, i1, r1);

    // Pupil.
    ctx.fillStyle = state.eyeColor;
    var i2 = outer - ring * 4;
    var r2 = style === 'circle' ? i2 / 2
      : style === 'leaf' ? i2 * 0.38 : Math.max(0, r - ring * 2);
    roundRect(ctx, cx + ring * 2, cy + ring * 2, i2, i2, r2);
  }

  /** A square with two opposite corners rounded — the "leaf" eye shape. */
  function leafPath(ctx, x, y, s, r) {
    ctx.beginPath();
    ctx.moveTo(x + r, y);
    ctx.lineTo(x + s, y);
    ctx.lineTo(x + s, y + s - r);
    ctx.quadraticCurveTo(x + s, y + s, x + s - r, y + s);
    ctx.lineTo(x, y + s);
    ctx.lineTo(x, y + r);
    ctx.quadraticCurveTo(x, y, x + r, y);
    ctx.closePath();
    ctx.fill();
  }

  function paint(canvas, result, scale) {
    var quiet = 4;
    var dim = (result.size + quiet * 2) * scale;
    canvas.width = dim;
    canvas.height = dim;
    var ctx = canvas.getContext('2d');

    ctx.fillStyle = state.bg;
    ctx.fillRect(0, 0, dim, dim);

    ctx.fillStyle = state.fg;
    for (var y = 0; y < result.size; y++) {
      for (var x = 0; x < result.size; x++) {
        if (!result.modules[y][x] || isEye(x, y, result.size)) continue;
        drawModule(ctx, (x + quiet) * scale, (y + quiet) * scale, scale, state.shape);
      }
    }

    ctx.fillStyle = state.eyeColor;
    var far = (result.size - 7 + quiet) * scale;
    var near = quiet * scale;
    drawEye(ctx, near, near, scale, state.eye);
    drawEye(ctx, far, near, scale, state.eye);
    drawEye(ctx, near, far, scale, state.eye);

    if (state.logo) {
      // A fifth of the width, on a background-coloured pad so the logo never
      // sits directly on modules. Error correction covers the loss.
      var box = dim * 0.21;
      var pad = box * 0.14;
      var lx = (dim - box) / 2;
      ctx.fillStyle = state.bg;
      roundRect(ctx, lx - pad, lx - pad, box + pad * 2, box + pad * 2, box * 0.22);
      ctx.drawImage(state.logo, lx, lx, box, box);
    }
  }

  /** Colours only ever come from <input type="color">, which normalises to
   *  #rrggbb — but an unescaped value interpolated into SVG attributes is one
   *  refactor away from a script-bearing download, and an SVG opened from
   *  disk executes script. Validate at the boundary. */
  function hex(c, fallback) {
    return /^#[0-9a-fA-F]{6}$/.test(c) ? c : fallback;
  }

  function svg(result) {
    var quiet = 4, n = result.size + quiet * 2;
    var out = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ' + n + ' ' + n +
      '" width="1024" height="1024" shape-rendering="geometricPrecision">' +
      '<rect width="' + n + '" height="' + n + '" fill="' + hex(state.bg, '#FFFFFF') + '"/>';

    var body = '';
    for (var y = 0; y < result.size; y++) {
      for (var x = 0; x < result.size; x++) {
        if (!result.modules[y][x] || isEye(x, y, result.size)) continue;
        var px = x + quiet, py = y + quiet;
        if (state.shape === 'dots') {
          body += '<circle cx="' + (px + .5) + '" cy="' + (py + .5) + '" r="0.44"/>';
        } else if (state.shape === 'diamond') {
          // Inset by 0.06 on each side, as the canvas does. Spanning the full
          // cell made SVG diamonds visibly fatter than PNG ones.
          var d0 = px + .06, d1 = py + .06, dw = .88;
          body += '<path d="M' + (d0 + dw / 2) + ' ' + d1 + 'L' + (d0 + dw) + ' ' +
            (d1 + dw / 2) + 'L' + (d0 + dw / 2) + ' ' + (d1 + dw) + 'L' + d0 + ' ' +
            (d1 + dw / 2) + 'z"/>';
        } else if (state.shape === 'rounded') {
          // 0.88 * 0.34, matching drawModule's radius rather than a round 0.3.
          body += '<rect x="' + (px + .06) + '" y="' + (py + .06) +
            '" width="0.88" height="0.88" rx="0.2992"/>';
        } else {
          body += '<rect x="' + px + '" y="' + py + '" width="1" height="1"/>';
        }
      }
    }
    out += '<g fill="' + hex(state.fg, '#10111A') + '">' + body + '</g>';

    var r = state.eye === 'circle' ? 3.5
      : state.eye === 'rounded' ? 7 * 0.26
        : state.eye === 'leaf' ? 7 * 0.44 : 0;
    var leaf = state.eye === 'leaf';
    var shape = leaf ? leafPathSvg : rectPath;
    var eyes = '';
    [[quiet, quiet], [result.size - 7 + quiet, quiet], [quiet, result.size - 7 + quiet]]
      .forEach(function (p) {
        eyes += '<path fill-rule="evenodd" d="' +
          shape(p[0], p[1], 7, r) +
          shape(p[0] + 1, p[1] + 1, 5, Math.max(0, r - 1)) + '"/>' +
          '<rect x="' + (p[0] + 2) + '" y="' + (p[1] + 2) + '" width="3" height="3" rx="' +
          (state.eye === 'circle' ? 1.5 : leaf ? 3 * 0.38 : Math.max(0, r - 2)) + '"/>';
      });
    out += '<g fill="' + hex(state.eyeColor, '#0B5CFF') + '">' + eyes + '</g>';

    if (state.logo) {
      // Embedded as a data URI so the .svg stays a single self-contained file.
      var box = n * 0.21, pad = box * 0.14, lx = (n - box) / 2;
      var tmp = document.createElement('canvas');
      tmp.width = tmp.height = 512;
      tmp.getContext('2d').drawImage(state.logo, 0, 0, 512, 512);
      out += '<rect x="' + (lx - pad) + '" y="' + (lx - pad) + '" width="' +
        (box + pad * 2) + '" height="' + (box + pad * 2) + '" rx="' + (box * 0.22) +
        '" fill="' + hex(state.bg, '#FFFFFF') + '"/>' +
        '<image x="' + lx + '" y="' + lx + '" width="' + box + '" height="' + box +
        '" href="' + tmp.toDataURL('image/png') + '"/>';
    }
    return out + '</svg>';
  }

  /** SVG twin of leafPath: two opposite corners rounded, two square. */
  function leafPathSvg(x, y, s, r) {
    if (!r) return rectPath(x, y, s, 0);
    return 'M' + (x + r) + ' ' + y + 'H' + (x + s) + 'V' + (y + s - r) +
      'Q' + (x + s) + ' ' + (y + s) + ' ' + (x + s - r) + ' ' + (y + s) +
      'H' + x + 'V' + (y + r) + 'Q' + x + ' ' + y + ' ' + (x + r) + ' ' + y + 'z';
  }

  function rectPath(x, y, s, r) {
    if (!r) return 'M' + x + ' ' + y + 'h' + s + 'v' + s + 'h-' + s + 'z';
    return 'M' + (x + r) + ' ' + y + 'h' + (s - 2 * r) + 'a' + r + ' ' + r + ' 0 0 1 ' +
      r + ' ' + r + 'v' + (s - 2 * r) + 'a' + r + ' ' + r + ' 0 0 1 -' + r + ' ' + r +
      'h-' + (s - 2 * r) + 'a' + r + ' ' + r + ' 0 0 1 -' + r + ' -' + r +
      'v-' + (s - 2 * r) + 'a' + r + ' ' + r + ' 0 0 1 ' + r + ' -' + r + 'z';
  }


  // --- bulk mode -----------------------------------------------------------
  //
  // The bulk page promised "each line becomes its own QR code" while the
  // builder returned only the first line, so it was byte-identical to every
  // other single-code page. This renders one code per line, each separately
  // downloadable.

  var BULK_LIMIT = 200;
  var bulkOut = document.getElementById('bulk-out');

  function renderBulk() {
    var raw = String(state.values.text || '');
    var lines = raw.split('\n').map(function (l) { return l.trim(); })
      .filter(function (l) { return l.length; });

    bulkOut.textContent = '';
    var count = document.getElementById('bulk-count');
    if (!lines.length) {
      count.textContent = 'Paste one link or line of text per line above.';
      return;
    }

    var over = lines.length > BULK_LIMIT;
    if (over) lines = lines.slice(0, BULK_LIMIT);
    count.textContent = lines.length + ' code' + (lines.length === 1 ? '' : 's') +
      (over ? ' — only the first ' + BULK_LIMIT + ' are shown' : '');

    lines.forEach(function (line, i) {
      var cell = document.createElement('div');
      cell.className = 'bulk-cell';
      var cv = document.createElement('canvas');
      var result;
      try {
        result = window.TrustScanQR.encode(line, state.ecc);
      } catch (e) {
        cell.appendChild(el('p', 'gen-error', 'Line ' + (i + 1) + ': ' + e.message));
        bulkOut.appendChild(cell);
        return;
      }
      paint(cv, result, 6);
      cell.appendChild(cv);

      var label = el('p', 'bulk-label', line.length > 42 ? line.slice(0, 42) + '…' : line);
      label.title = line;
      cell.appendChild(label);

      var btn = el('button', 'btn btn-ghost', 'Download');
      btn.type = 'button';
      btn.addEventListener('click', function () {
        var big = document.createElement('canvas');
        paint(big, result, 28);
        big.toBlob(function (b) { save(fileName(line, i) + '.png', b); }, 'image/png');
      });
      cell.appendChild(btn);
      bulkOut.appendChild(cell);
    });
  }

  function fileName(line, i) {
    var base = line.replace(/^https?:\/\//, '')
      .replace(/[^a-zA-Z0-9]+/g, '-').replace(/^-+|-+$/g, '').toLowerCase();
    if (!base) base = 'code';
    if (base.length > 40) base = base.slice(0, 40).replace(/-+$/, '');
    return String(i + 1).padStart(3, '0') + '-' + base;
  }

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }

  // --- render loop ---------------------------------------------------------

  function render() {
    if (bulkOut) return renderBulk();
    var text = '';
    try { text = spec.build(state.values) || ''; } catch (e) { text = ''; }
    elError.textContent = '';

    if (!text) {
      state.matrix = null;
      elCanvas.getContext('2d').clearRect(0, 0, elCanvas.width, elCanvas.height);
      elMeta.textContent = 'Fill in a field to see your code';
      return;
    }
    var result;
    try {
      result = window.TrustScanQR.encode(text, state.ecc);
    } catch (e) {
      state.matrix = null;
      // Clear it. Leaving the previous code visible next to an error message
      // invites saving a QR for content the user has already replaced.
      elCanvas.getContext('2d').clearRect(0, 0, elCanvas.width, elCanvas.height);
      elError.textContent = e.message;
      elMeta.textContent = '';
      return;
    }
    state.matrix = result;
    paint(elCanvas, result, 10);
    elMeta.textContent = 'Version ' + result.version + ' · ' + result.size + '×' +
      result.size + ' modules · ECC ' + state.ecc + ' · ' + text.length + ' characters';
  }

  // --- controls ------------------------------------------------------------

  function bind(id, key, event) {
    var el = document.getElementById(id);
    if (!el) return;
    el.addEventListener(event || 'change', function () {
      state[key] = el.value; render();
    });
  }
  bind('gen-ecc', 'ecc');
  bind('gen-shape', 'shape');
  bind('gen-eye', 'eye');
  bind('gen-fg', 'fg', 'input');
  bind('gen-eyecolor', 'eyeColor', 'input');
  bind('gen-bg', 'bg', 'input');

  var presets = document.getElementById('gen-presets');
  if (presets) {
    presets.querySelectorAll('button').forEach(function (b) {
      var c = b.getAttribute('data-preset').split(',');
      b.style.background = 'linear-gradient(90deg,' + c[0] + ' 50%,' + c[1] + ' 50%)';
      b.style.borderColor = c[2];
      // title= alone is a last-resort accessible name and never surfaces on
      // touch. Give the swatch a real label and a pressed state.
      b.setAttribute('aria-label', (b.getAttribute('title') || 'Colour preset') +
        ' colour preset');
      b.setAttribute('aria-pressed', 'false');
      b.addEventListener('click', function () {
        state.fg = c[0]; state.eyeColor = c[1]; state.bg = c[2];
        var f = document.getElementById('gen-fg');
        var e = document.getElementById('gen-eyecolor');
        var g = document.getElementById('gen-bg');
        if (f) f.value = c[0];
        if (e) e.value = c[1];
        if (g) g.value = c[2];
        Array.prototype.forEach.call(presets.querySelectorAll('button'),
          function (x) { x.setAttribute('aria-pressed', 'false'); });
        b.setAttribute('aria-pressed', 'true');
        render();
      });
    });
  }

  var logoInput = document.getElementById('gen-logo');
  if (logoInput) {
    logoInput.addEventListener('change', function () {
      var file = logoInput.files && logoInput.files[0];
      if (!file) { state.logo = null; render(); return; }
      var img = new Image();
      var objUrl = URL.createObjectURL(file);
      img.onload = function () {
        state.logo = img;
        URL.revokeObjectURL(objUrl);   // was never revoked
        if (logoClear) logoClear.disabled = false;
        render();
      };
      img.src = objUrl;
    });
  }
  var logoClear = document.getElementById('gen-logo-clear');
  if (logoClear) {
    logoClear.disabled = true;
    logoClear.addEventListener('click', function () {
      state.logo = null;
      if (logoInput) logoInput.value = '';
      logoClear.disabled = true;
      render();
    });
  }

  // --- downloads -----------------------------------------------------------

  /** A filename that says which code it is — ten files all called
   *  trustscan-qr.png are indistinguishable once downloaded. */
  function downloadName() {
    var first = '';
    for (var k in state.values) {
      if (state.values[k]) { first = String(state.values[k]); break; }
    }
    var slug = first.replace(/^https?:\/\//, '')
      .replace(/[^a-zA-Z0-9]+/g, '-').replace(/^-+|-+$/g, '').toLowerCase().slice(0, 40);
    return typeId + (slug ? '-' + slug.replace(/-+$/, '') : '') + '-qr';
  }

  function save(name, blob) {
    var a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = name;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    setTimeout(function () { URL.revokeObjectURL(a.href); }, 1000);
  }

  var png = document.getElementById('dl-png');
  if (png) png.addEventListener('click', function () {
    if (!state.matrix) return;
    var big = document.createElement('canvas');
    paint(big, state.matrix, 28);           // ~1000–1600 px, print-safe
    big.toBlob(function (b) { save(downloadName() + '.png', b); }, 'image/png');
  });

  var dlsvg = document.getElementById('dl-svg');
  if (dlsvg) dlsvg.addEventListener('click', function () {
    if (!state.matrix) return;
    save(downloadName() + '.svg',
      new Blob([svg(state.matrix)], { type: 'image/svg+xml' }));
  });

  render();
})();
