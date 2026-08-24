/* TrustScan QR encoder — byte mode, versions 1–40, ECC L/M/Q/H.
 *
 * Runs entirely in the browser. Nothing you type is uploaded, which is the
 * whole point of putting a generator on this site rather than linking to one.
 *
 * Algorithm follows Project Nayuki's QR Code generator (MIT licence),
 * reimplemented compactly for this page.
 */
(function (global) {
  'use strict';

  var ECC = { L: 0, M: 1, Q: 2, H: 3 };
  // Format-info bit patterns are ordered L,M,Q,H by spec value, not by index.
  var ECC_FORMAT_BITS = [1, 0, 3, 2];

  var ECC_CODEWORDS_PER_BLOCK = [
    [7, 10, 15, 20, 26, 18, 20, 24, 30, 18, 20, 24, 26, 30, 22, 24, 28, 30, 28,
      28, 28, 28, 30, 30, 26, 28, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30,
      30, 30, 30],
    [10, 16, 26, 18, 24, 16, 18, 22, 22, 26, 30, 22, 22, 24, 24, 28, 28, 26,
      26, 26, 26, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28,
      28, 28, 28, 28],
    [13, 22, 18, 26, 18, 24, 18, 22, 20, 24, 28, 26, 24, 20, 30, 24, 28, 28,
      26, 30, 28, 30, 30, 30, 30, 28, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30,
      30, 30, 30, 30],
    [17, 28, 22, 16, 22, 28, 26, 26, 24, 28, 24, 28, 22, 24, 24, 30, 28, 28,
      26, 28, 30, 24, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30,
      30, 30, 30, 30]
  ];

  var NUM_BLOCKS = [
    [1, 1, 1, 1, 1, 2, 2, 2, 2, 4, 4, 4, 4, 4, 6, 6, 6, 6, 7, 8, 8, 9, 9, 10,
      12, 12, 12, 13, 14, 15, 16, 17, 18, 19, 19, 20, 21, 22, 24, 25],
    [1, 1, 1, 2, 2, 4, 4, 4, 5, 5, 5, 8, 9, 9, 10, 10, 11, 13, 14, 16, 17, 17,
      18, 20, 21, 23, 25, 26, 28, 29, 31, 33, 35, 37, 38, 40, 43, 45, 47, 49],
    [1, 1, 2, 2, 4, 4, 6, 6, 8, 8, 8, 10, 12, 16, 12, 17, 16, 18, 21, 20, 23,
      23, 25, 27, 29, 34, 34, 35, 38, 40, 43, 45, 48, 51, 53, 56, 59, 62, 65,
      68],
    [1, 1, 2, 4, 4, 4, 5, 6, 8, 8, 11, 11, 16, 16, 18, 16, 19, 21, 25, 25, 25,
      34, 30, 32, 35, 37, 40, 42, 45, 48, 51, 54, 57, 60, 63, 66, 70, 74, 77,
      81]
  ];

  function rawDataModules(ver) {
    var result = (16 * ver + 128) * ver + 64;
    if (ver >= 2) {
      var numAlign = Math.floor(ver / 7) + 2;
      result -= (25 * numAlign - 10) * numAlign - 55;
      if (ver >= 7) result -= 36;
    }
    return result;
  }

  function dataCodewords(ver, ecl) {
    return Math.floor(rawDataModules(ver) / 8) -
      ECC_CODEWORDS_PER_BLOCK[ecl][ver - 1] * NUM_BLOCKS[ecl][ver - 1];
  }

  function alignmentPositions(ver) {
    if (ver === 1) return [];
    var numAlign = Math.floor(ver / 7) + 2;
    var step = (ver === 32) ? 26
      : Math.ceil((ver * 4 + 4) / (numAlign * 2 - 2)) * 2;
    var result = [6];
    for (var pos = ver * 4 + 10; result.length < numAlign; pos -= step) {
      result.splice(1, 0, pos);
    }
    return result;
  }

  // --- Galois field arithmetic ---------------------------------------------

  function gfMultiply(x, y) {
    var z = 0;
    for (var i = 7; i >= 0; i--) {
      z = ((z << 1) ^ ((z >>> 7) * 0x11D)) & 0xFF;
      z ^= ((y >>> i) & 1) * x;
      z &= 0xFF;
    }
    return z;
  }

  function rsDivisor(degree) {
    var result = new Uint8Array(degree);
    result[degree - 1] = 1;
    var root = 1;
    for (var i = 0; i < degree; i++) {
      for (var j = 0; j < result.length; j++) {
        result[j] = gfMultiply(result[j], root);
        if (j + 1 < result.length) result[j] ^= result[j + 1];
      }
      root = gfMultiply(root, 0x02);
    }
    return result;
  }

  function rsRemainder(data, divisor) {
    var result = new Uint8Array(divisor.length);
    for (var k = 0; k < data.length; k++) {
      var factor = data[k] ^ result[0];
      result.copyWithin(0, 1);
      result[result.length - 1] = 0;
      for (var i = 0; i < result.length; i++) {
        result[i] ^= gfMultiply(divisor[i], factor);
      }
    }
    return result;
  }

  // --- Encoding ------------------------------------------------------------

  function utf8Bytes(str) {
    var out = [];
    for (var i = 0; i < str.length; i++) {
      var c = str.codePointAt(i);
      if (c > 0xFFFF) i++;
      // An unpaired surrogate is not a character. Emitting it raw produces
      // CESU-8, which is invalid UTF-8, and decoders reject the entire
      // payload rather than the one bad character. Substitute U+FFFD, which
      // is what TextEncoder does.
      else if (c >= 0xD800 && c <= 0xDFFF) c = 0xFFFD;
      if (c < 0x80) out.push(c);
      else if (c < 0x800) {
        out.push(0xC0 | (c >> 6), 0x80 | (c & 0x3F));
      } else if (c < 0x10000) {
        out.push(0xE0 | (c >> 12), 0x80 | ((c >> 6) & 0x3F), 0x80 | (c & 0x3F));
      } else {
        out.push(0xF0 | (c >> 18), 0x80 | ((c >> 12) & 0x3F),
          0x80 | ((c >> 6) & 0x3F), 0x80 | (c & 0x3F));
      }
    }
    return out;
  }

  function BitBuffer() { this.bits = []; }
  BitBuffer.prototype.append = function (val, len) {
    for (var i = len - 1; i >= 0; i--) this.bits.push((val >>> i) & 1);
  };

  function charCountBits(ver) { return ver < 10 ? 8 : 16; }

  function buildCodewords(bytes, ver, ecl) {
    var bb = new BitBuffer();
    bb.append(0x4, 4);                          // byte mode
    bb.append(bytes.length, charCountBits(ver));
    for (var i = 0; i < bytes.length; i++) bb.append(bytes[i], 8);

    var capacityBits = dataCodewords(ver, ecl) * 8;
    bb.append(0, Math.min(4, capacityBits - bb.bits.length));
    bb.append(0, (8 - bb.bits.length % 8) % 8);
    for (var pad = 0xEC; bb.bits.length < capacityBits; pad ^= 0xEC ^ 0x11) {
      bb.append(pad, 8);
    }

    var data = new Uint8Array(bb.bits.length / 8);
    for (var j = 0; j < bb.bits.length; j++) {
      data[j >>> 3] |= bb.bits[j] << (7 - (j & 7));
    }
    return interleave(data, ver, ecl);
  }

  function interleave(data, ver, ecl) {
    var numBlocks = NUM_BLOCKS[ecl][ver - 1];
    var eccLen = ECC_CODEWORDS_PER_BLOCK[ecl][ver - 1];
    var rawCodewords = Math.floor(rawDataModules(ver) / 8);
    var numShort = numBlocks - rawCodewords % numBlocks;
    var shortLen = Math.floor(rawCodewords / numBlocks);

    var blocks = [];
    var divisor = rsDivisor(eccLen);
    for (var i = 0, k = 0; i < numBlocks; i++) {
      var len = shortLen - eccLen + (i < numShort ? 0 : 1);
      var dat = data.slice(k, k + len);
      k += len;
      var ecc = rsRemainder(dat, divisor);
      var block = Array.prototype.slice.call(dat);
      blocks.push({ data: block, ecc: Array.prototype.slice.call(ecc) });
    }

    var result = [];
    for (var c = 0; c < shortLen - eccLen + 1; c++) {
      for (var b = 0; b < blocks.length; b++) {
        if (c < blocks[b].data.length) result.push(blocks[b].data[c]);
      }
    }
    for (var e = 0; e < eccLen; e++) {
      for (var b2 = 0; b2 < blocks.length; b2++) result.push(blocks[b2].ecc[e]);
    }
    return result;
  }

  // --- Matrix --------------------------------------------------------------

  function makeMatrix(ver, ecl, codewords) {
    var size = ver * 4 + 17;
    var modules = [], reserved = [];
    for (var y = 0; y < size; y++) {
      modules.push(new Array(size).fill(false));
      reserved.push(new Array(size).fill(false));
    }

    function setFn(x, y, dark) {
      if (x < 0 || y < 0 || x >= size || y >= size) return;
      modules[y][x] = dark;
      reserved[y][x] = true;
    }

    function finder(cx, cy) {
      for (var dy = -4; dy <= 4; dy++) {
        for (var dx = -4; dx <= 4; dx++) {
          var d = Math.max(Math.abs(dx), Math.abs(dy));
          setFn(cx + dx, cy + dy, d !== 2 && d !== 4);
        }
      }
    }
    finder(3, 3); finder(size - 4, 3); finder(3, size - 4);

    for (var i = 8; i < size - 8; i++) {
      setFn(i, 6, i % 2 === 0);
      setFn(6, i, i % 2 === 0);
    }

    var align = alignmentPositions(ver);
    for (var a = 0; a < align.length; a++) {
      for (var b = 0; b < align.length; b++) {
        var skip = (a === 0 && b === 0) || (a === 0 && b === align.length - 1) ||
          (a === align.length - 1 && b === 0);
        if (skip) continue;
        for (var dy2 = -2; dy2 <= 2; dy2++) {
          for (var dx2 = -2; dx2 <= 2; dx2++) {
            setFn(align[b] + dx2, align[a] + dy2,
              Math.max(Math.abs(dx2), Math.abs(dy2)) !== 1);
          }
        }
      }
    }

    // Reserve format areas; the real bits are written after masking.
    for (var f = 0; f <= 8; f++) { setFn(f, 8, false); setFn(8, f, false); }
    for (var g = 0; g < 8; g++) {
      setFn(size - 1 - g, 8, false);
      setFn(8, size - 1 - g, false);
    }
    setFn(8, size - 8, true); // permanently dark module

    if (ver >= 7) {
      var rem = ver;
      for (var vi = 0; vi < 12; vi++) rem = (rem << 1) ^ ((rem >>> 11) * 0x1F25);
      var vbits = (ver << 12) | rem;
      for (var vk = 0; vk < 18; vk++) {
        var bit = ((vbits >>> vk) & 1) !== 0;
        var vx = size - 11 + vk % 3, vy = Math.floor(vk / 3);
        setFn(vx, vy, bit); setFn(vy, vx, bit);
      }
    }

    // Zigzag data placement, right to left, skipping the vertical timing line.
    var idx = 0;
    for (var right = size - 1; right >= 1; right -= 2) {
      if (right === 6) right = 5;
      for (var vert = 0; vert < size; vert++) {
        for (var jj = 0; jj < 2; jj++) {
          var xx = right - jj;
          var upward = ((right + 1) & 2) === 0;
          var yy = upward ? size - 1 - vert : vert;
          if (!reserved[yy][xx] && idx < codewords.length * 8) {
            modules[yy][xx] = ((codewords[idx >>> 3] >>> (7 - (idx & 7))) & 1) !== 0;
            idx++;
          }
        }
      }
    }

    // Try every mask, keep the least penalised — this is what makes a code
    // scan reliably rather than merely decode in software.
    var bestMask = 0, bestPenalty = Infinity, bestModules = null;
    for (var m = 0; m < 8; m++) {
      var trial = modules.map(function (row) { return row.slice(); });
      applyMask(trial, reserved, m, size);
      drawFormat(trial, ecl, m, size);
      var p = penalty(trial, size);
      if (p < bestPenalty) {
        bestPenalty = p; bestMask = m;
        bestModules = trial;
      }
    }
    return bestModules;
  }

  function maskFn(m, x, y) {
    switch (m) {
      case 0: return (x + y) % 2 === 0;
      case 1: return y % 2 === 0;
      case 2: return x % 3 === 0;
      case 3: return (x + y) % 3 === 0;
      case 4: return (Math.floor(x / 3) + Math.floor(y / 2)) % 2 === 0;
      case 5: return x * y % 2 + x * y % 3 === 0;
      case 6: return (x * y % 2 + x * y % 3) % 2 === 0;
      default: return ((x + y) % 2 + x * y % 3) % 2 === 0;
    }
  }

  function applyMask(mods, reserved, m, size) {
    for (var y = 0; y < size; y++) {
      for (var x = 0; x < size; x++) {
        if (!reserved[y][x] && maskFn(m, x, y)) mods[y][x] = !mods[y][x];
      }
    }
  }

  function drawFormat(mods, ecl, mask, size) {
    var data = (ECC_FORMAT_BITS[ecl] << 3) | mask;
    var rem = data;
    for (var i = 0; i < 10; i++) rem = (rem << 1) ^ ((rem >>> 9) * 0x537);
    var bits = ((data << 10) | rem) ^ 0x5412;

    function bit(n) { return ((bits >>> n) & 1) !== 0; }

    // mods is indexed [row][column], i.e. [y][x]. The spec lists these as
    // (x, y) pairs, and transcribing them in that order transposes every
    // one — which produces a structurally perfect code that no scanner can
    // read, because the format bits say the wrong mask and ECC level.
    for (var j = 0; j <= 5; j++) mods[j][8] = bit(j);
    mods[7][8] = bit(6);
    mods[8][8] = bit(7);
    mods[8][7] = bit(8);
    for (var k = 9; k < 15; k++) mods[8][14 - k] = bit(k);

    // Second copy, split between the other two finder patterns.
    for (var p = 0; p < 8; p++) mods[8][size - 1 - p] = bit(p);
    for (var q = 8; q < 15; q++) mods[size - 15 + q][8] = bit(q);
    mods[size - 8][8] = true;
  }

  function penalty(mods, size) {
    var result = 0, x, y, i;

    for (y = 0; y < size; y++) {
      var runColor = false, runLen = 0;
      for (x = 0; x < size; x++) {
        if (mods[y][x] === runColor) {
          runLen++;
          if (runLen === 5) result += 3;
          else if (runLen > 5) result++;
        } else { runColor = mods[y][x]; runLen = 1; }
      }
    }
    for (x = 0; x < size; x++) {
      var rc = false, rl = 0;
      for (y = 0; y < size; y++) {
        if (mods[y][x] === rc) {
          rl++;
          if (rl === 5) result += 3; else if (rl > 5) result++;
        } else { rc = mods[y][x]; rl = 1; }
      }
    }

    for (y = 0; y < size - 1; y++) {
      for (x = 0; x < size - 1; x++) {
        var c = mods[y][x];
        if (c === mods[y][x + 1] && c === mods[y + 1][x] &&
          c === mods[y + 1][x + 1]) result += 3;
      }
    }

    // Rule 3: a 1:1:3:1:1 run with four light modules on either side reads
    // like a finder pattern and misleads a camera about where the code is.
    var A = [true, false, true, true, true, false, true];
    function runsAt(get, n) {
      var hits = 0;
      for (var i = 0; i + 7 <= n; i++) {
        var ok = true;
        for (var j = 0; j < 7; j++) {
          if (get(i + j) !== A[j]) { ok = false; break; }
        }
        if (!ok) continue;
        var before = true, after = true;
        for (var k = 1; k <= 4; k++) {
          if (i - k >= 0 && get(i - k)) before = false;
          if (i + 6 + k < n && get(i + 6 + k)) after = false;
        }
        if (before || after) hits++;
      }
      return hits;
    }
    for (y = 0; y < size; y++) {
      result += 40 * runsAt(function (i) { return mods[y][i]; }, size);
    }
    for (x = 0; x < size; x++) {
      result += 40 * runsAt(function (i) { return mods[i][x]; }, size);
    }

    var dark = 0;
    for (y = 0; y < size; y++) {
      for (x = 0; x < size; x++) if (mods[y][x]) dark++;
    }
    var total = size * size;
    var k2 = Math.ceil(Math.abs(dark * 20 - total * 10) / total) - 1;
    result += k2 * 10;
    return result;
  }

  // --- Public API ----------------------------------------------------------

  /**
   * Encodes text into a QR matrix.
   * @returns {{size:number, modules:boolean[][], version:number}}
   * @throws if the text is too long for any version at this ECC level.
   */
  function encode(text, eccName) {
    var ecl = ECC[eccName] !== undefined ? ECC[eccName] : ECC.M;
    var bytes = utf8Bytes(String(text));
    var ver = 0;
    for (var v = 1; v <= 40; v++) {
      var cap = dataCodewords(v, ecl) * 8;
      var need = 4 + charCountBits(v) + bytes.length * 8;
      if (need <= cap) { ver = v; break; }
    }
    if (ver === 0) {
      throw new Error('Too much content for one QR code — shorten it, or ' +
        'lower the error correction level.');
    }
    var codewords = buildCodewords(bytes, ver, ecl);
    var modules = makeMatrix(ver, ecl, codewords);
    return { size: ver * 4 + 17, modules: modules, version: ver };
  }

  global.TrustScanQR = { encode: encode };
})(typeof window !== 'undefined' ? window : self);
