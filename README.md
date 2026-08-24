# trustscanqr.com

Static site. No build step for deployment — upload the folder as-is to any
host. Everything works from `file://` too, apart from the fonts.

## Deploying

Upload the whole `site/` folder to the web root of `trustscanqr.com`. That is
it. There is no server code, no database and no API.

**Set `404.html` as the error page** in your host's settings so mistyped URLs
land somewhere useful.

### Two files that must sit at the root

| File | Why |
|---|---|
| `app-ads.txt` | AdMob only ever fetches `https://trustscanqr.com/app-ads.txt`. If the developer website in your Play listing points here, this file has to be reachable at exactly that address or your ad revenue drops. It already contains your real publisher id. |
| `robots.txt` | Points crawlers at `sitemap.xml`. |

After deploying, submit `https://trustscanqr.com/sitemap.xml` in Google Search
Console.

## Adding or editing a QR code type

Everything is generated from one list. **Do not edit the generator pages by
hand** — they are overwritten.

1. Add a dict to `TYPES` in `build.py`
2. `python3 build.py`

That writes the page, adds it to every sidebar, adds it to the homepage grid,
and adds it to `sitemap.xml`.

Each entry needs:

```python
{
  "id": "wifi",                          # matches window.QR_TYPES key
  "slug": "wifi-qr-code-generator",      # the URL, and the keyword
  "nav": "Wi-Fi",                        # sidebar label
  "h1": "Wi-Fi QR Code Generator",       # the exact search phrase
  "title": "...| TrustScan",             # <title>, ~60 chars
  "desc": "...",                         # meta description, ~155 chars
  "kw": "wifi qr code generator, ...",   # comma-separated
  "intro": "...",                        # one paragraph under the h1
  "fields": [...],                       # form fields
  "build": "return ...;",                # JS body: v -> payload string
  "body": [("Heading", "Paragraph"), …], # long-form copy for SEO
}
```

The `h1` should *be* the keyword you want to rank for, not a paraphrase of it.
That is the whole reason there is a page per type rather than one page with
tabs.

## How it fits together

```
build.py              the single source of truth
  ├─ *.html           32 generator pages, one per keyword
  ├─ assets/js/types.js   field definitions + payload builders
  └─ sitemap.xml

assets/js/qr.js       QR encoder — byte mode, versions 1–40, ECC L/M/Q/H
assets/js/generator.js  form, styled canvas/SVG rendering, downloads
assets/js/safety.js   the app's 14 link checks, ported to JS
assets/js/site.js     nav toggle, homepage link checker
```

Hand-written pages, not generated: `index.html`, `qr-code-safety.html`,
`privacy.html`, `support.html`, `404.html`.

## Why it all runs client-side

Nothing typed into the generator or the link checker is ever transmitted. That
is not a technical accident — it is the claim the whole product rests on, and
a site that quietly logged what you generated would make the app's privacy
policy a lie. It also means the site costs nothing to run and cannot leak what
it never received.

The link checker is a genuine port of `lib/services/url_safety.dart`, so what
a visitor sees on the homepage is what the app would tell them on their phone.
**If you change the checks in the app, change them here too** — a demo that
disagrees with the product is worse than no demo.

## Verifying a change

The QR encoder has been checked against macOS's own detector (`CIDetector`)
across versions, ECC levels, UTF-8 payloads and every module/eye shape
combination. If you touch `qr.js` or the renderer, re-verify — a QR code that
looks right and does not scan is the worst possible bug here, because nobody
notices until it is printed.

## Local preview

```
python3 -m http.server 4173 --directory site
```

Fonts need to be served over HTTP, so opening `index.html` directly will fall
back to the system sans-serif.
