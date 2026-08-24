/* TrustScan link checks, ported from the app's lib/services/url_safety.dart.
 *
 * Runs in your browser. The URL you type is never sent anywhere — same
 * guarantee the app makes, and the reason this demo can exist at all.
 */
(function (global) {
  'use strict';

  var SHORTENERS = ['bit.ly', 'tinyurl.com', 't.co', 'goo.gl', 'is.gd',
    'cutt.ly', 'rb.gy', 'ow.ly', 'buff.ly', 'shorturl.at', 't.ly', 's.id',
    'rebrand.ly', 'tiny.cc',
    '1url.at', 'lnk.ink', 'tiny.one', 'shorte.st', 'adf.ly', 'bc.vc', 'gg.gg',
    'v.gd', 'u.to', 'clck.ru', 'vk.cc', 'surl.li', 'shrtco.de', 'cutt.us',
    'qr.ae', 'lnkd.in', 'bl.ink', 'short.io', 'qrco.de', 'linktr.ee'];

  // Hosting anyone can publish to in minutes, without paying or identifying
  // themselves. The largest blind spot in a checker that only reads the shape
  // of a hostname: a phishing page on `something.pages.dev` imitates nothing,
  // has a valid certificate, sits on a reputable network, and passes every
  // other check here. Being on one is not itself wrong — so alone it is a
  // caution, and a danger only when the page also asks for a password.
  var FREE_HOSTS = [
    'web.app', 'firebaseapp.com', 'firebasestorage.googleapis.com',
    'appspot.com', 'sites.google.com',
    'pages.dev', 'workers.dev', 'r2.dev', 'trycloudflare.com',
    'vercel.app', 'netlify.app', 'onrender.com', 'herokuapp.com',
    'azurewebsites.net', 'glitch.me', 'repl.co', 'replit.app', 'surge.sh',
    'fly.dev', 'railway.app', 'koyeb.app', 'ondigitalocean.app',
    'weebly.com', 'wixsite.com', '000webhostapp.com', 'blogspot.com',
    'square.site', 'godaddysites.com', 'my-free.website', 'webflow.io',
    'telegra.ph', 'notion.site', 'framer.website', 'carrd.co',
    'ipfs.io', 'dweb.link', 'cf-ipfs.com', 'cloudflare-ipfs.com',
    'gateway.pinata.cloud', 'ipfs.fleek.co', 'nftstorage.link'
  ,
    'github.io', 'gitlab.io', 'bitbucket.io', 'gitbook.io', 'readthedocs.io',
    'ngrok.io', 'ngrok-free.app', 'zrok.io', 'loca.lt', 'serveo.net',
    'pythonanywhere.com', 'neocities.org', 'eu.cc', 'is-a.dev', 'js.org'];

  // Endings a global brand plausibly uses — not every valid TLD, just the
  // unremarkable ones. The point is `roblox.ly`: treating any brand-as-
  // registrable-label as official read that as safe, which is backwards.
  var ORDINARY_SUFFIXES = [
    'com','net','org','co','io','app','dev','me','tv','ai','cloud',
    'inc','shop','store','group','global','online','site','tech',
    'uk','de','fr','es','it','nl','be','ch','at','se','no','dk',
    'fi','pl','pt','ie','gr','cz','hu','ro','ru','ua','tr',
    'us','ca','mx','br','ar','cl','pe','co.uk','com.au','com.br',
    'jp','cn','kr','in','id','my','sg','ph','th','vn','hk','tw',
    'au','nz','za','ng','ke','eg','ae','sa','il','pk','bd','lk',
    'eu','asia'
  ];

  // Real brand domains on endings the list above calls unusual. Measured, not
  // guessed — each was a false alarm in the top-4,000 corpus.
  var BRAND_OWN_DOMAINS = [
    'discord.gg','discord.media','discordapp.com','discordapp.net',
    'apple.news','apple.co','amzn.to','a.co','fb.me','fb.com','fb.watch',
    'aka.ms','msn.com','goo.gl','g.co','youtu.be','spoti.fi','t.me','wa.me'
  ];

  var RISKY_TLDS = ['tk', 'ml', 'ga', 'cf', 'gq', 'zip', 'mov', 'top',
    'click', 'link', 'work',
    'lat', 'cfd', 'sbs', 'bond', 'icu', 'rest', 'quest', 'cyou', 'cam',
    'monster', 'beauty', 'hair', 'skin', 'makeup', 'autos', 'boats', 'lol',
    'bar', 'kim', 'country', 'gdn', 'download', 'racing', 'review', 'stream'];

  var BRANDS = ['paypal', 'apple', 'icloud', 'google', 'microsoft', 'office365',
    'netflix', 'amazon', 'facebook', 'instagram', 'whatsapp', 'binance',
    'coinbase', 'metamask', 'fedex', 'hmrc', 'bankid',
    // Added after measuring against live phishing feeds: every one of these
    // was impersonated in the corpus and passed as "no risks found".
    'roblox', 'steam', 'discord', 'spotify', 'linkedin', 'tiktok', 'snapchat',
    'dhl', 'usps', 'dpd', 'evri', 'royalmail', 'correos',
    'revolut', 'monzo', 'starling', 'nubank', 'paytm', 'phonepe',
    'santander', 'barclays', 'lloyds', 'natwest', 'halifax', 'hsbc',
    'kraken', 'ledger', 'trezor', 'trustwallet', 'phantom', 'opensea',
    'aliexpress', 'alibaba', 'shopee', 'lazada', 'mercadolibre'];

  var SUFFIX_HEADS = ['co', 'com', 'net', 'org', 'gov', 'edu', 'ac', 'or',
    'ne', 'go', 'me', 'biz', 'info', 'in', 'nom', 'mil', 'sch', 'gob', 'gouv'];

  var DANGEROUS_SCHEMES = ['javascript', 'data', 'file', 'jar', 'intent'];

  var EXECUTABLE_EXTS = ['.apk', '.exe', '.msi', '.bat', '.cmd', '.scr', '.jar',
    '.dmg', '.pkg', '.vbs', '.ps1', '.sh', '.apk.zip'];


  // Visually confusable ASCII substitutions — a brand imitated without ever
  // leaving ASCII, so neither the non-Latin check nor the brand check sees it.
  // A canonical alphabet, not a repair table: each set of confusable glyphs
  // collapses to one representative, and the SAME folding is applied to the
  // brand list so the two meet in the middle. Mapping one way let real attacks
  // through — '1' folded to 'l', which fixed paypa1 but never netfl1x, because
  // the brand stayed 'netflix' and 'netfllx' matched nothing.
  var HOMOGLYPHS = {
    '0': 'o', '1': 'i', 'l': 'i', '|': 'i', '!': 'i',
    '3': 'e', '4': 'a', '5': 's', '7': 't', '9': 'g', '8': 'b', '2': 'z'
  };

  function defold(label) {
    var out = label.replace(/rn/g, 'm').replace(/vv/g, 'w');
    for (var k in HOMOGLYPHS) out = out.split(k).join(HOMOGLYPHS[k]);
    return out;
  }

  // Every brand under the same folding, mapped back to its real spelling.
  var FOLDED_BRANDS = (function () {
    var m = {};
    for (var i = 0; i < BRANDS.length; i++) m[defold(BRANDS[i])] = BRANDS[i];
    return m;
  })();

  // RFC 3492. Without this the punycode check can only be blunt: flag every
  // non-Latin domain (painting legitimate Thai and Chinese sites red) or flag
  // none (letting `xn--pypal-4ve.com` — "pаypal" with a Cyrillic а — past).
  // Decoding lets the mixed-script and homoglyph checks read what the user
  // will actually see, which is the only fair thing to judge.
  function punycodeDecode(label) {
    var base = 36, tmin = 1, tmax = 26, skew = 38, damp = 700;
    function adapt(delta, numPoints, firstTime) {
      delta = firstTime ? Math.floor(delta / damp) : delta >> 1;
      delta += Math.floor(delta / numPoints);
      var k = 0;
      while (delta > ((base - tmin) * tmax) >> 1) {
        delta = Math.floor(delta / (base - tmin));
        k += base;
      }
      return k + Math.floor(((base - tmin + 1) * delta) / (delta + skew));
    }
    var n = 128, i = 0, bias = 72, output = [];
    var basic = label.lastIndexOf('-');
    if (basic > 0) {
      for (var j = 0; j < basic; j++) {
        var c = label.charCodeAt(j);
        if (c >= 128) return null;
        output.push(c);
      }
    } else { basic = -1; }
    var idx = basic + 1;
    if (idx >= label.length) return null;
    while (idx < label.length) {
      var oldi = i, w = 1, k = base;
      for (;;) {
        if (idx >= label.length) return null;
        var cp = label.charCodeAt(idx++), digit;
        if (cp >= 0x30 && cp <= 0x39) digit = cp - 0x30 + 26;
        else if (cp >= 0x61 && cp <= 0x7A) digit = cp - 0x61;
        else if (cp >= 0x41 && cp <= 0x5A) digit = cp - 0x41;
        else return null;
        if (digit > Math.floor((0x7FFFFFFF - i) / w)) return null;
        i += digit * w;
        var t = k <= bias ? tmin : (k >= bias + tmax ? tmax : k - bias);
        if (digit < t) break;
        if (w > Math.floor(0x7FFFFFFF / (base - t))) return null;
        w *= base - t;
        k += base;
      }
      var outLen = output.length + 1;
      bias = adapt(i - oldi, outLen, oldi === 0);
      n += Math.floor(i / outLen);
      i %= outLen;
      if (n > 0x10FFFF || (n >= 0xD800 && n <= 0xDFFF)) return null;
      output.splice(i, 0, n);
      i++;
    }
    return String.fromCodePoint.apply(String, output);
  }

  // The host as a person will see it.
  function renderedHost(host) {
    if (host.indexOf('xn--') === -1) return host;
    return host.split('.').map(function (l) {
      if (l.indexOf('xn--') !== 0) return l;
      return punycodeDecode(l.slice(4)) || l;
    }).join('.');
  }

  function scriptOf(r) {
    if ((r >= 0x41 && r <= 0x5A) || (r >= 0x61 && r <= 0x7A) ||
        (r >= 0xC0 && r <= 0x24F)) return 'latin';
    if (r >= 0x400 && r <= 0x4FF) return 'cyrillic';
    if (r >= 0x370 && r <= 0x3FF) return 'greek';
    if (r >= 0x530 && r <= 0x58F) return 'armenian';
    return null;
  }

  /** True when one label mixes scripts — the homograph attack itself. A
   *  wholly Cyrillic domain like пример.рф is legitimate, not an attack. */
  function mixesScripts(label) {
    var seen = {}, n = 0;
    for (var i = 0; i < label.length; i++) {
      var sc = scriptOf(label.codePointAt(i));
      if (sc && !seen[sc]) { seen[sc] = 1; n++; }
      if (n > 1) return true;
    }
    return false;
  }

  function hasTwoPartSuffix(labels) {
    if (labels.length < 3) return false;
    var head = labels[labels.length - 2];
    var tld = labels[labels.length - 1];
    return tld.length === 2 && SUFFIX_HEADS.indexOf(head) !== -1;
  }

  function isRawAddress(host) {
    if (host.indexOf(':') !== -1) return true;
    var labels = host.split('.');
    if (!labels.length || labels.length > 4) return false;
    for (var i = 0; i < labels.length; i++) {
      var l = labels[i];
      if (!l) return false;
      if (!/^0[xX][0-9a-fA-F]+$/.test(l) && !/^0[0-7]+$/.test(l) &&
        !/^\d+$/.test(l)) return false;
    }
    return true;
  }

  /**
   * @returns {{level:'safe'|'caution'|'danger', reasons:string[]}}
   */
  function check(input) {
    var raw = String(input || '').trim();
    if (!raw) return { level: 'caution', reasons: ["There's nothing to check yet."] };

    var url;
    try { url = new URL(raw.indexOf('://') === -1 && !/^[a-z]+:/i.test(raw) ? 'https://' + raw : raw); }
    catch (e) { return { level: 'caution', reasons: ["This link couldn't be read as a web address."] }; }

    var scheme = url.protocol.replace(':', '').toLowerCase();
    if (DANGEROUS_SCHEMES.indexOf(scheme) !== -1) {
      return {
        level: 'danger',
        reasons: ['Uses the "' + scheme + '" scheme, which can run code or ' +
          'reach files on your device rather than open a page.']
      };
    }
    if (!url.hostname) {
      return { level: 'caution', reasons: ["This link couldn't be read as a web address."] };
    }

    // Percent-decoded, because a browser decodes the host before applying
    // IDNA. Without this, a hand-encoded Cyrillic lookalike reads as pure
    // ASCII and passes every check below.
    var host;
    try { host = decodeURIComponent(url.hostname); }
    catch (e) { host = url.hostname; }
    host = host.toLowerCase().replace(/\.+$/, '');

    var rawAuthority = raw.replace(/^[a-z]+:\/\//i, '').split(/[/?#]/)[0];
    // Wrapped, like the hostname decode above. A truncated escape such as
    // "/%zz" throws URIError out of check(), which emptied the verdict box and
    // left a stale level behind — the security demo dying silently.
    var path;
    try { path = decodeURIComponent(url.pathname || ''); }
    catch (e) { path = url.pathname || ''; }
    path = path.toLowerCase();
    var tail = ((url.search || '') + ' ' + (url.hash || '')).toLowerCase();

    var warnings = [], dangers = [];

    if (scheme === 'http') {
      warnings.push('Uses unencrypted HTTP — anything you send to this site ' +
        'can be read in transit.');
    }
    // The browser normalises hex and octal addresses to dotted decimal before
    // we ever see url.hostname, so the disguise has to be spotted in the text
    // the user actually scanned — otherwise a deliberately obfuscated address
    // is reported as an ordinary bare IP and the reader loses the point.
    var rawHost = rawAuthority.split('@').pop().split(':')[0].toLowerCase();
    var disguised = /^(0x[0-9a-f]+|0[0-7]+)(\.|$)/.test(rawHost) ||
      (/^\d+$/.test(rawHost) && rawHost.length > 3);
    if (disguised) {
      dangers.push('Points at a raw address written in an unusual number ' +
        'format, which hides the real destination from anyone reading it.');
    } else if (/^\d{1,3}(\.\d{1,3}){3}$/.test(host)) {
      dangers.push('Points at a bare IP address instead of a domain name — ' +
        'common in phishing links.');
    } else if (isRawAddress(host)) {
      dangers.push('Points at a raw address instead of a domain name, which ' +
        'hides who actually operates the site.');
    }
    // Measured against the top 4,000 domains this was the single largest
    // source of false alarms: legitimate Thai, Chinese and Arabic sites are
    // all punycode on the wire. Worth reading twice, not a danger on its own —
    // the hostile shapes (a brand beside it, two alphabets in one word) raise
    // their own danger above.
    if (host.indexOf('xn--') !== -1) {
      warnings.push('Uses punycode, so the name you see may not be the ' +
        'letters actually in the address.');
    }
    var hostLabels = host.split('.');
    // Judge the letters the user will actually see: `xn--pypal-4ve.com` is
    // pure ASCII on the wire and renders as "pаypal" with a Cyrillic а.
    var renderedLabels = renderedHost(host).split('.');
    if (hostLabels.some(mixesScripts) ||
        renderedLabels.some(mixesScripts) ||
        rawAuthority.split('.').some(mixesScripts)) {
      dangers.push('The domain mixes letters from two different alphabets in ' +
        'one word — the exact trick used to imitate a trusted site.');
    } else if (/[^\x00-\x7F]/.test(rawAuthority) || /[^\x00-\x7F]/.test(host)) {
      // Unusual, not an attack: an ordinary international domain.
      warnings.push('The domain uses a non-Latin alphabet. That is normal for ' +
        'many countries, but worth a second look on a link you did not expect.');
    }

    var foldTargets = hostLabels.concat(
      renderedLabels.filter(function (l) { return hostLabels.indexOf(l) === -1; }));
    for (var hi = 0; hi < foldTargets.length; hi++) {
      // A label that IS a brand is not imitating one. This replaces the old
      // `folded !== label` test, which stops working once brands are folded
      // too: 'paypal' folds to 'paypai' and would report itself.
      if (BRANDS.indexOf(foldTargets[hi]) !== -1) continue;
      var brand = FOLDED_BRANDS[defold(foldTargets[hi])];
      if (brand) {
        dangers.push('Spells "' + brand + '" using lookalike characters, so ' +
          'it reads as the real brand at a glance but is a different domain.');
        break;
      }
    }
    if (raw.indexOf('@') !== -1) {
      var before = raw.split('@')[0];
      if (before.indexOf('//') !== -1 && before.split('//').pop().indexOf('/') === -1) {
        dangers.push('Hides the real destination after an "@" — everything ' +
          'before it is ignored by the browser.');
      }
    }
    // endsWith, spelled out. An indexOf-based version matched whenever both
    // sides evaluated to -1, which flagged any 11-character domain as a
    // shortener — example.com among them.
    if (SHORTENERS.indexOf(host) !== -1 ||
      SHORTENERS.some(function (s) {
        return host.length > s.length + 1 &&
          host.slice(-(s.length + 1)) === '.' + s;
      })) {
      warnings.push('A link shortener — the real destination is hidden until ' +
        'you open it.');
    }
    var tld = host.split('.').pop();
    if (RISKY_TLDS.indexOf(tld) !== -1) {
      warnings.push('Uses the ".' + tld + '" domain ending, heavily abused ' +
        'for throwaway scam sites.');
    }
    if (/(login|verify|secure|account|update|confirm|banking|wallet)[-.]/.test(host)) {
      warnings.push('The domain contains urgent-sounding words often used to ' +
        'imitate a login page.');
    }
    if ((host.match(/\./g) || []).length >= 4) {
      warnings.push('An unusually deep subdomain chain, often used to push ' +
        'the real domain out of sight on a phone.');
    }

    // Brand impersonation: whole labels are a danger, hyphen-joined tokens a
    // caution. "paypal-billing.com" is the commonest phishing shape there is.
    var labels = host.split('.');
    var regIndex = hasTwoPartSuffix(labels) ? labels.length - 3 : labels.length - 2;
    var tokens = [];
    labels.forEach(function (l) { tokens = tokens.concat(l.split('-')); });
    for (var bi = 0; bi < BRANDS.length; bi++) {
      var brand = BRANDS[bi];
      var whole = labels.indexOf(brand) !== -1;
      if (!whole && tokens.indexOf(brand) === -1) continue;
      // `.google` and `.microsoft` are real top-level domains owned by those
      // companies, so `dns.google` and `cloud.microsoft` are as official as a
      // domain gets. Both were painted red until this line existed.
      // The brand being the registrable label is not enough on its own:
      // `roblox.ly` is not Roblox. The ending has to be one a real brand
      // would plausibly be on.
      var suffix = regIndex >= 0 ? labels.slice(regIndex + 1).join('.') : '';
      var registrable = regIndex >= 0 ? labels.slice(regIndex).join('.') : host;
      var ordinary = ORDINARY_SUFFIXES.indexOf(suffix) !== -1 ||
        ORDINARY_SUFFIXES.indexOf(labels[labels.length - 1]) !== -1;
      var official = labels[labels.length - 1] === brand ||
        BRAND_OWN_DOMAINS.indexOf(registrable) !== -1 ||
        (regIndex >= 0 && labels[regIndex] === brand && ordinary);
      if (!official) {
        var msg = 'Mentions "' + brand + '" but is not an official ' + brand +
          ' domain — a common impersonation trick.';
        if (whole) dangers.push(msg); else warnings.push(msg);
      }
      break;
    }

    for (var ei = 0; ei < EXECUTABLE_EXTS.length; ei++) {
      if (path.slice(-EXECUTABLE_EXTS[ei].length) === EXECUTABLE_EXTS[ei]) {
        dangers.push('Downloads a ' + EXECUTABLE_EXTS[ei] + ' file rather ' +
          'than opening a page.');
        break;
      }
    }
    // An executable can hide in the query as easily as the path:
    // "/get?f=update.apk". The app flags this; the site did not, which made
    // the demo more permissive than the product it advertises.
    var tailTokens = tail.split(/[&=;,\s/]|%2f|%3d/);
    for (var ti = 0; ti < tailTokens.length; ti++) {
      for (var tj = 0; tj < EXECUTABLE_EXTS.length; tj++) {
        var ext = EXECUTABLE_EXTS[tj];
        if (tailTokens[ti].slice(-ext.length) === ext) {
          dangers.push('Carries a ' + ext + ' file in its parameters, so it ' +
            'downloads something rather than opening a page.');
          ti = tailTokens.length;
          break;
        }
      }
    }
    if (/(https?%3a|https?:\/\/|%2f%2f|=\/\/|%252f|%253a)/.test(tail)) {
      warnings.push('Carries another web address inside it — open redirects ' +
        'are used to launder a link through a domain you trust.');
    }
    var asksForCredentials =
      /(password|passwd|signin|log-?in|verify|otp|2fa|seed|recovery|private-?key)/
        .test(path + ' ' + tail);
    if (asksForCredentials) {
      warnings.push('The address asks for credentials, a one-time code or a ' +
        'recovery phrase.');
    }

    // Anonymous hosting. Matched on the registrable suffix, so `evil.pages.dev`
    // counts and a company's own `pages.dev.example.com` does not.
    var freeHost = '';
    for (var fh = 0; fh < FREE_HOSTS.length; fh++) {
      var h = FREE_HOSTS[fh];
      if (host === h || host.slice(-(h.length + 1)) === '.' + h) {
        freeHost = h; break;
      }
    }
    if (freeHost) {
      var msg = 'Published on "' + freeHost + '", where anyone can put a page ' +
        'up in minutes without identifying themselves.';
      // Anyone-can-publish plus asking for a password is the combination;
      // either alone is ordinary.
      if (asksForCredentials) dangers.push(msg); else warnings.push(msg);
    }
    var port = url.port;
    if (port && port !== '80' && port !== '443') {
      warnings.push('Connects on port ' + port + ' rather than the standard ' +
        'web ports, which is unusual for a legitimate public site.');
    }
    if (raw.length > 150) {
      warnings.push('Unusually long, which is often used to bury the real ' +
        'destination.');
    }

    var level = dangers.length ? 'danger' : (warnings.length ? 'caution' : 'safe');
    return { level: level, reasons: dangers.concat(warnings) };
  }

  global.TrustScanSafety = { check: check };
})(typeof window !== 'undefined' ? window : self);
