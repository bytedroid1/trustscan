#!/usr/bin/env python3
"""Static site builder for trustscanqr.com.

One page per QR code type, because that is how you rank for forty keywords
instead of three. Each page owns its slug, its <h1>, its title tag and its
long-form copy — the H1 *is* the search phrase, not a paraphrase of it.

Run:  python3 build.py
Everything is regenerated from TYPES below, so adding a new QR type is one
dict entry, not a new HTML file.
"""

import json
import pathlib
import html

SITE = "https://trustscanqr.com"
PLAY_URL = "https://play.google.com/store/apps/details?id=com.trustscan.scanner"
# Flip to False and rebuild if the App Store listing is ever pulled — the URL
# 404s until Apple approves the app, so publish before deploying the site.
IOS_LIVE = True
IOS_URL = "https://apps.apple.com/app/id6804426564"
LASTMOD = "2026-08-24"
OUT = pathlib.Path(__file__).parent

# --- field kinds reused across types ---------------------------------------

F_URL = [{"name": "url", "label": "Link", "placeholder": "https://example.com", "type": "url"}]


def social(name, label, placeholder, prefix):
    """A social profile type: user types a handle, we build the profile URL."""
    return {
        "fields": [{"name": "handle", "label": label, "placeholder": placeholder}],
        "build": f"return v.handle ? '{prefix}' + String(v.handle).replace(/^@/, '') : '';",
    }



FAQS = {
  "url": [
    ("Is this QR code generator free?",
     "Yes. There is no account, no watermark, no scan limit and no expiry. It runs on your own device, so it costs nothing to provide."),
    ("Do QR codes expire?",
     "Static QR codes never expire. The destination is encoded in the pattern itself, so a printed code works for as long as the page it points to exists."),
    ("How many scans does a QR code allow?",
     "Unlimited. A static QR code has no counter and no server behind it, so there is nothing to meter."),
  ],
  "wifi": [
    ("How do I make a QR code for my Wi-Fi password?",
     "Enter your network name, the password and the security type above, then download and print the code. Guests point a camera at it and their phone offers to join."),
    ("Does a Wi-Fi QR code work on iPhone and Android?",
     "Yes. Android has supported Wi-Fi QR codes for years and iPhone since iOS 11. On both, the built-in camera app is enough — no app needed."),
    ("Is it safe to print my Wi-Fi password as a QR code?",
     "The code contains the password in readable form, so anyone who photographs it has it. Use it for a guest network rather than the network your till and back-office computers use."),
  ],
  "vcard": [
    ("What is a vCard QR code?",
     "A QR code containing your contact details in the vCard format phones already understand. One scan saves your name, company, phone, email and website straight into the contacts app."),
    ("How do I put a QR code on my business card?",
     "Fill in the fields above, download the SVG, and place it on the back of your card at 2 cm or larger. Keep the fields minimal — every extra line makes the code denser and harder to scan."),
  ],
  "logo": [
    ("Can I add a logo to a QR code?",
     "Yes. Upload one above and it is placed in the centre. Set error correction to Highest so the code still reads with the middle covered."),
    ("Will a logo stop my QR code from scanning?",
     "Not if it covers less than about a fifth of the code and never touches the three large corner squares. QR codes carry error correction precisely so part of the pattern can be lost. Always test before printing."),
  ],
  "review": [
    ("How do I create a Google review QR code?",
     "Open your Google Business Profile, choose Reviews and then Get more reviews, and copy the short link ending in /review. Paste it above."),
    ("Where should I put a review QR code?",
     "On the receipt, the counter or the table card. The best moment to ask is right after you have done the thing the customer is happy about, while they are still there."),
  ],
  "menu": [
    ("How do I make a QR code for a restaurant menu?",
     "Paste the address of your menu page or PDF above. Print the code at 3 to 4 cm for a table card and test it from a seated position in your evening lighting."),
    ("Do menu QR codes cost anything monthly?",
     "Not these. A static code points straight at your menu, so there is no subscription and no company that can switch it off or start charging."),
  ],
  "bulk": [
    ("How do I generate many QR codes at once?",
     "Paste one link per line above. For a large batch, the TrustScan app imports a CSV and exports every code as a zip with sensible filenames."),
    ("Is there a limit on how many QR codes I can make?",
     "No. There is no account and no quota, because the codes are generated on your own device."),
  ],
  "whatsapp": [
    ("How do I create a WhatsApp QR code?",
     "Enter your number with its country code and no plus sign, and optionally a message to pre-fill. Scanning opens a chat with you."),
    ("Can I add a message to a WhatsApp QR code?",
     "Yes. A pre-filled message like \u201cBooking enquiry\u201d tells you what the customer wants and saves them writing the first line."),
  ],
  "text": [
    ("How much text fits in a QR code?",
     "Roughly 1,800 characters at a comfortable error correction level. Longer text makes a denser code that needs to be printed larger to scan reliably."),
  ],
  "paypal": [
    ("How do I make a PayPal QR code?",
     "Enter your PayPal.Me name above, and optionally an amount. Create your PayPal.Me link in the PayPal app under Request money."),
  ],
  "upi": [
    ("How do I create a UPI QR code?",
     "Enter your UPI ID and name above. The code works with Google Pay, PhonePe, Paytm, BHIM and every other UPI app."),
  ],
  "bitcoin": [
    ("How do I make a Bitcoin QR code?",
     "Paste your wallet address above, with an optional amount. Copy and paste the address rather than typing it, then scan your own code to confirm it before use."),
  ],
}

TYPES = [
    # --- core -------------------------------------------------------------
    {
        "id": "url", "slug": "qr-code-generator", "nav": "Website link",
        "h1": "Free QR Code Generator",
        "title": "Free QR Code Generator — No Sign-Up, No Watermark | TrustScan",
        "desc": "Free QR code generator for any website link. Create a QR code online in seconds and download it as PNG or SVG. No account, no watermark, no expiry, nothing uploaded.",
        "kw": "qr code generator, free qr code generator, create qr code, qr code maker, qr code generator online",
        "intro": "Turn any link into a QR code. It runs in your browser, so what you type is never uploaded, and the code you get is static — it holds the address itself rather than pointing at someone else's redirect.",
        "fields": F_URL,
        "build": "return v.url || '';",
        "body": [
            ("What is a QR code generator?",
             "A QR code is a picture of text. A generator takes the text — usually a web address — and lays it out as the black and white pattern a camera can read. Everything needed to open the link is in the pattern itself, which is why a printed code keeps working with no internet connection on the printing side and no service subscription."),
            ("Static versus dynamic QR codes",
             "Codes made here are static: the destination is encoded directly. A dynamic QR code instead encodes a short link on a third party's server, which forwards the scanner onward. That lets the owner change the destination later, but it also means the code stops working if that company folds, starts charging, or decides to redirect elsewhere. For a printed menu, a shop window or product packaging, static is the safer choice."),
            ("How to make a QR code for a website",
             "Paste the full address including https://, check the preview, and download. Use SVG for anything that gets printed and PNG for screens. Test the result with the actual phone your audience will use before committing it to print."),
        ],
    },
    {
        "id": "logo", "slug": "qr-code-generator-with-logo", "nav": "Logo QR code",
        "h1": "QR Code Generator With Logo",
        "title": "QR Code Generator With Logo — Free, High Resolution",
        "desc": "Add your logo to a QR code and download it in high resolution. Free QR code generator with logo, custom colours and SVG export — no sign-up.",
        "kw": "qr code generator with logo, qr code with logo, custom qr code, high resolution qr code",
        "intro": "A logo in the middle of a QR code turns an anonymous square into something recognisably yours. Set the error correction to Highest below so the code still reads with the centre covered.",
        "fields": F_URL,
        "build": "return v.url || '';",
        "body": [
            ("How a logo fits inside a QR code",
             "QR codes carry error correction — spare data that lets a scanner reconstruct the content even when part of the pattern is missing. At the highest level roughly 30% of the code can be obscured and it still reads. That headroom is what a centre logo consumes."),
            ("Keeping a logo QR code scannable",
             "Cover no more than about a fifth of the code, keep the logo square and centred, and never let it touch the three large corner squares — those are the finder patterns a scanner uses to locate and orient the code. Always test before printing."),
            ("Placing your logo in the app",
             "The TrustScan app places a logo in the centre of any code you create and raises the error correction automatically, then exports at 2,400 px or as vector SVG. Set the colours and error correction here, then use the app when you need the logo baked in."),
        ],
    },
    {
        "id": "text", "slug": "text-to-qr-code-generator", "nav": "Plain text",
        "h1": "Text to QR Code Generator",
        "title": "Text to QR Code Generator — Free Plain Text QR",
        "desc": "Convert any text into a QR code for free. Plain text QR codes for instructions, serial numbers, passwords, notes and labels. Download PNG or SVG.",
        "kw": "text to qr code, plain text qr code, qr code for text, text qr generator",
        "intro": "Not every QR code needs to open a website. A plain text code shows its contents on screen and goes no further — useful for instructions, asset tags, serial numbers and anything you want readable but not clickable.",
        "fields": [{"name": "text", "label": "Text", "placeholder": "Anything you like", "el": "textarea"}],
        "build": "return v.text || '';",
        "body": [
            ("When plain text beats a link",
             "A text code cannot take anyone anywhere, which is exactly the point for equipment labels, warehouse tags and safety instructions. There is no destination to be hijacked and no page that can go offline."),
            ("How much text fits in a QR code",
             "A single QR code holds roughly 2,900 bytes at the lowest error correction — about 1,800 characters at a comfortable level. Long text makes a dense code that needs to be printed larger to scan reliably. The preview shows the version and module count as you type."),
        ],
    },
    {
        "id": "wifi", "slug": "wifi-qr-code-generator", "nav": "Wi-Fi",
        "h1": "Wi-Fi QR Code Generator",
        "title": "Wi-Fi QR Code Generator — Free Guest Network QR",
        "desc": "Create a free Wi-Fi QR code so guests join by scanning. Works with WPA, WPA2, WPA3 and open networks. Print it for your café or office.",
        "kw": "wifi qr code generator, wifi qr code, guest wifi qr code, qr code for wifi password",
        "intro": "Guests point a camera at the code and join. No password read out across a room, no handwritten card behind the counter, no typos.",
        "fields": [
            {"name": "ssid", "label": "Network name (SSID)", "placeholder": "Cafe Guest"},
            {"name": "password", "label": "Password", "placeholder": "Leave blank if the network is open"},
            {"name": "enc", "label": "Security type", "el": "select", "options": [["WPA", "WPA / WPA2 / WPA3"], ["WEP", "WEP"], ["nopass", "Open — no password"]]},
            {"name": "hidden", "label": "Hidden network", "el": "select", "options": [["false", "No"], ["true", "Yes"]]},
        ],
        "build": "if(!v.ssid)return '';"
                 "var esc=function(s){return String(s||'').replace(/([\\\\;,\":])/g,'\\\\$1');};"
                 "return 'WIFI:T:'+(v.enc||'WPA')+';S:'+esc(v.ssid)+';P:'+esc(v.password)+"
                 "';H:'+(v.hidden==='true'?'true':'false')+';;';",
        "body": [
            ("How a Wi-Fi QR code works",
             "The code contains the network name, the security type and the password in a short standard format. Phones recognise it and offer to join. Android has supported this for years and iPhones have since iOS 11 — on both, the camera app is enough."),
            ("Which security type to choose",
             "Pick WPA unless your router is genuinely ancient; it covers WPA, WPA2 and WPA3. Choose Open only if the network really has no password. WEP is obsolete and should be replaced rather than shared."),
            ("A word about printing your password",
             "This code contains your Wi-Fi password in readable form. Anyone who photographs the printed card has it. Put it on your guest network rather than the network your till, cameras and back-office computers sit on."),
        ],
    },
    {
        "id": "vcard", "slug": "vcard-qr-code-generator", "nav": "vCard contact",
        "h1": "vCard QR Code Generator",
        "title": "vCard QR Code Generator — Digital Business Card",
        "desc": "Create a free vCard QR code for your business card. One scan saves your name, company, phone, email, website and address straight into the phone's contacts.",
        "kw": "vcard qr code generator, qr code business card, digital business card qr, contact qr code",
        "intro": "One scan and your details are in their contacts app — spelled correctly, with the right country code, and without anyone typing anything.",
        "fields": [
            {"name": "first", "label": "First name", "placeholder": "Alex"},
            {"name": "last", "label": "Last name", "placeholder": "Carter"},
            {"name": "org", "label": "Company", "placeholder": "TrustScan"},
            {"name": "title", "label": "Job title", "placeholder": "Founder"},
            {"name": "phone", "label": "Mobile", "placeholder": "+92 300 1234567", "type": "tel"},
            {"name": "work", "label": "Work phone", "placeholder": "Optional", "type": "tel"},
            {"name": "email", "label": "Email", "placeholder": "info@trustscanqr.com", "type": "email"},
            {"name": "website", "label": "Website", "placeholder": "https://trustscanqr.com", "type": "url"},
            {"name": "street", "label": "Street", "placeholder": "Optional"},
            {"name": "city", "label": "City", "placeholder": "Optional"},
            {"name": "country", "label": "Country", "placeholder": "Optional"},
        ],
        "build": "if(!v.first&&!v.last&&!v.org&&!v.phone&&!v.email)return '';"
                 # RFC 2426 treats ; , and \\ as structural. A company name
                 # like \"Smith, Jones & Co; Ltd\" split into extra fields.
                 "var e=function(x){return String(x||'').replace(/([\\\\;,])/g,'\\\\$1')"
                 ".replace(/\\r?\\n/g,'\\\\n');};"
                 "var L=['BEGIN:VCARD','VERSION:3.0'];"
                 "L.push('N:'+e(v.last)+';'+e(v.first)+';;;');"
                 "L.push('FN:'+e([v.first,v.last].filter(Boolean).join(' ')));"
                 "if(v.org)L.push('ORG:'+e(v.org)); if(v.title)L.push('TITLE:'+e(v.title));"
                 "if(v.phone)L.push('TEL;TYPE=CELL:'+v.phone);"
                 "if(v.work)L.push('TEL;TYPE=WORK:'+v.work);"
                 "if(v.email)L.push('EMAIL:'+v.email); if(v.website)L.push('URL:'+v.website);"
                 "if(v.street||v.city||v.country)L.push('ADR:;;'+e(v.street)+';'+e(v.city)+';;;'+e(v.country));"
                 "L.push('END:VCARD'); return L.join('\\n');",
        "body": [
            ("What is a vCard QR code?",
             "vCard is the standard format contacts apps already understand — the same thing that arrives when someone shares a contact. Encoding one as a QR code means the recipient scans, taps save, and has you in their phone."),
            ("Keep it short",
             "Every field makes the code denser and harder to scan from a distance. Name, company, one phone number, one email and a website is usually enough. Leave the street address out unless people genuinely need to post you things."),
            ("Where to put it",
             "The back of a printed business card, an email signature, a conference badge, or a shop window. It works offline, so it keeps working in a basement exhibition hall with no signal."),
        ],
    },
    {
        "id": "email", "slug": "email-qr-code-generator", "nav": "Email",
        "h1": "Email QR Code Generator",
        "title": "Email QR Code Generator — Free Mailto QR Codes | TrustScan",
        "desc": "Create a free email QR code. Scanning opens a new message to your address with the subject and body already filled in.",
        "kw": "email qr code generator, mailto qr code, qr code for email",
        "intro": "Scanning opens a new email addressed to you, optionally with the subject and message already written. Good for support desks, feedback requests and warranty claims.",
        "fields": [
            {"name": "to", "label": "Send to", "placeholder": "info@trustscanqr.com", "type": "email"},
            {"name": "subject", "label": "Subject", "placeholder": "Optional"},
            {"name": "body", "label": "Message", "placeholder": "Optional", "el": "textarea"},
        ],
        "build": "if(!v.to)return ''; var q=[]; if(v.subject)q.push('subject='+encodeURIComponent(v.subject));"
                 "if(v.body)q.push('body='+encodeURIComponent(v.body));"
                 "return 'mailto:'+(v.to||'')+(q.length?'?'+q.join('&'):'');",
        "body": [
            ("Pre-filling the subject line",
             "A subject like “Support request — model X” lets you route mail automatically and tells you which sign the customer scanned. It saves the sender thinking of one, which measurably increases how many actually write."),
        ],
    },
    {
        "id": "sms", "slug": "sms-qr-code-generator", "nav": "SMS",
        "h1": "SMS QR Code Generator",
        "title": "SMS QR Code Generator — Free Text Message QR Codes | TrustScan",
        "desc": "Create a free SMS QR code. Scanning opens a text message to your number with the message already typed — ideal for opt-in keywords, voting and quick orders.",
        "kw": "sms qr code generator, text message qr code, qr code for sms",
        "intro": "Scanning opens the messaging app with your number and message ready to send. Used for keyword opt-ins, table service and quick reorders.",
        "fields": [
            {"name": "number", "label": "Phone number", "placeholder": "+92 300 1234567", "type": "tel"},
            {"name": "body", "label": "Message", "placeholder": "Optional", "el": "textarea"},
        ],
        "build": "var n=String(v.number||'').replace(/[^0-9+]/g,'');"
                 "return n?('SMSTO:'+n+(v.body?':'+v.body:'')):'';",
        "body": [
            ("Use the international format",
             "Write the number with its country code, like +92 300 1234567. A local-format number works only for people whose phone already assumes your country."),
        ],
    },
    {
        "id": "call", "slug": "phone-call-qr-code-generator", "nav": "Phone call",
        "h1": "Phone Call QR Code Generator",
        "title": "Phone Number QR Code Generator — Click to Call",
        "desc": "Create a free phone call QR code. Scanning starts a call to your number — useful on vehicle livery, for-sale boards, delivery notes and shop signage.",
        "kw": "phone qr code generator, call qr code, qr code for phone number, click to call qr",
        "intro": "Scanning brings up your number ready to dial. Good on vehicles, estate agent boards, machinery and anywhere someone needs to reach you quickly.",
        "fields": [{"name": "number", "label": "Phone number", "placeholder": "+92 300 1234567", "type": "tel"}],
        "build": "var n=String(v.number||'').replace(/[^0-9+]/g,'');"
                 "return n?('tel:'+n):'';",
        "body": [
            ("Most phones ask first",
             "Scanning does not usually dial straight away — the phone shows the number and waits for a tap. That is a safety feature, and it means the number is visible before the call connects."),
        ],
    },
    {
        "id": "whatsapp", "slug": "whatsapp-qr-code-generator", "nav": "WhatsApp",
        "h1": "WhatsApp QR Code Generator",
        "title": "WhatsApp QR Code Generator — Free Chat Link QR | TrustScan",
        "desc": "Create a free WhatsApp QR code. Scanning opens a chat with your number, optionally with a message already typed. Great for orders, bookings and customer support.",
        "kw": "whatsapp qr code generator, whatsapp qr code, wa.me qr code, whatsapp business qr",
        "intro": "Scanning opens a WhatsApp chat with you, with an optional message already written. Widely used for order enquiries, bookings and support.",
        "fields": [
            {"name": "number", "label": "Number with country code, no plus sign", "placeholder": "923001234567"},
            {"name": "text", "label": "Pre-filled message", "placeholder": "Optional", "el": "textarea"},
        ],
        "build": "var n=String(v.number||'').replace(/\\D/g,'');"
                 "return n?'https://wa.me/'+n+(v.text?'?text='+encodeURIComponent(v.text):''):'';",
        "body": [
            ("Getting the number format right",
             "WhatsApp links need the country code with no plus sign, no spaces and no leading zero. A Pakistani number 0300 1234567 becomes 923001234567."),
            ("Pre-filled messages do the work",
             "“I'd like to order table 4” or “Booking enquiry — Saturday” tells you instantly what the customer wants and removes the awkward first message."),
        ],
    },
    {
        "id": "location", "slug": "location-qr-code-generator", "nav": "Location",
        "h1": "Location QR Code Generator",
        "title": "Location QR Code Generator — Free GPS Map QR",
        "desc": "Create a free location QR code from GPS coordinates. Scanning opens the map app at the exact spot — for venue signage, delivery instructions and meeting points.",
        "kw": "location qr code generator, gps qr code, map qr code, qr code for address",
        "intro": "Scanning opens the phone's map app at exact coordinates. Better than an address for building entrances, festival gates, sites and rural properties.",
        "fields": [
            {"name": "lat", "label": "Latitude", "placeholder": "25.3960"},
            {"name": "lng", "label": "Longitude", "placeholder": "68.3578"},
        ],
        "build": "return (v.lat&&v.lng)?('geo:'+v.lat+','+v.lng):'';",
        "body": [
            ("Finding your coordinates",
             "Long-press your spot in Google Maps and the coordinates appear at the top. Copy the two numbers in order — latitude first, then longitude."),
            ("Why coordinates beat an address",
             "An address takes people to the front of a building. Coordinates take them to the loading bay, the side gate or the field entrance you actually meant."),
        ],
    },
    {
        "id": "event", "slug": "event-qr-code-generator", "nav": "Calendar event",
        "h1": "Event QR Code Generator",
        "title": "Calendar Event QR Code Generator — Free iCal QR | TrustScan",
        "desc": "Create a free calendar event QR code. Scanning adds the event, its date, time and location straight to the phone's calendar.",
        "kw": "event qr code generator, calendar qr code, ical qr code, add to calendar qr",
        "intro": "Scanning offers to add the event to their calendar, with the date, time and place already filled in. Put it on invitations, posters and tickets.",
        "fields": [
            {"name": "title", "label": "Event name", "placeholder": "Product launch"},
            {"name": "location", "label": "Location", "placeholder": "Optional"},
            {"name": "start", "label": "Starts", "type": "datetime-local"},
            {"name": "end", "label": "Ends", "type": "datetime-local"},
        ],
        "build": "if(!v.title&&!v.start)return '';"
                 # A value carrying seconds produced 8 digits after T, which is
                 # not a valid iCalendar timestamp.
                 "var f=function(s){if(!s)return ''; var d=s.replace(/[-:]/g,'');"
                 "d=d.replace(/T(\\d{4})$/,'T$100'); return d.slice(0,15);};"
                 # RFC 5545 TEXT escaping.
                 "var e=function(x){return String(x||'').replace(/([\\\\;,])/g,'\\\\$1')"
                 ".replace(/\\r?\\n/g,'\\\\n');};"
                 "var L=['BEGIN:VEVENT']; if(v.title)L.push('SUMMARY:'+e(v.title));"
                 "if(v.location)L.push('LOCATION:'+e(v.location));"
                 "if(v.start)L.push('DTSTART:'+f(v.start)); if(v.end)L.push('DTEND:'+f(v.end));"
                 "L.push('END:VEVENT'); return L.join('\\n');",
        "body": [
            ("Times are local",
             "The times you enter are treated as local to whoever scans. For an event in a single place that is what you want; for an online event across time zones, put the time zone in the event name too."),
        ],
    },

    # --- business ---------------------------------------------------------
    {
        "id": "review", "slug": "google-review-qr-code-generator", "nav": "Google review",
        "h1": "Google Review QR Code Generator",
        "title": "Google Review QR Code Generator — Get More Reviews",
        "desc": "Create a free Google review QR code. Customers scan and land straight on your review form. Print it for the counter, the receipt or the table.",
        "kw": "google review qr code generator, review qr code, google reviews qr, qr code for reviews",
        "intro": "Point customers straight at your Google review form while they are still standing in front of you. Paste the review link from your Google Business Profile.",
        "fields": [{"name": "url", "label": "Google review link", "placeholder": "https://g.page/r/…/review", "type": "url"}],
        "build": "return v.url || '';",
        "body": [
            ("Finding your review link",
             "In your Google Business Profile, open the Reviews section and choose “Get more reviews” — Google gives you a short link ending in /review. That is the one to paste here. It opens the star rating form directly rather than your listing."),
            ("Where to put it",
             "On the receipt, the counter, the table card, or the back of the delivery slip. The best moment to ask is immediately after the thing you did well, while the customer is still there."),
            ("Ask honestly",
             "Ask for a review, not a five-star review. Offering anything in exchange breaks Google's policies and can get your reviews removed."),
        ],
    },
    {
        "id": "menu", "slug": "restaurant-menu-qr-code-generator", "nav": "Restaurant menu",
        "h1": "Restaurant Menu QR Code Generator",
        "title": "Restaurant Menu QR Code Generator — Free",
        "desc": "Create a free QR code for your restaurant menu. Customers scan the table card and your menu opens — no app, no subscription, no per-scan fee.",
        "kw": "restaurant menu qr code, menu qr code generator, digital menu qr code, table qr code",
        "intro": "Link the table card straight to your menu page or PDF. Static, so there is no monthly fee and no service that can switch it off.",
        "fields": [{"name": "url", "label": "Menu page or PDF address", "placeholder": "https://example.com/menu", "type": "url"}],
        "build": "return v.url || '';",
        "body": [
            ("Host the menu somewhere you control",
             "A page on your own website is better than a PDF in a file-sharing account, which often expires or demands a login. If you must use a PDF, keep it on your own domain."),
            ("Printing table cards",
             "Print at 3–4 cm across and test from a seated position, in your actual evening lighting. Laminate them — a QR code with a coffee ring through the corner can still work, but one that is scratched through the middle will not."),
            ("Watch for sticker fraud",
             "Restaurant tables are a favourite target: someone covers your code with theirs and takes payment details. Check your table cards periodically, and consider printing directly onto the card rather than using stickers."),
        ],
    },
    {
        "id": "bulk", "slug": "bulk-qr-code-generator", "nav": "Bulk generate",
        "h1": "Bulk QR Code Generator",
        "title": "Bulk QR Code Generator — Free and Unlimited",
        "desc": "Generate many QR codes at once, free and unlimited. Paste one link per line and download them all. No account, no per-code fee, nothing uploaded.",
        "kw": "bulk qr code generator, mass qr code generator, multiple qr codes, batch qr code",
        "intro": "One link per line. Each becomes its own QR code, and you can download them one by one — or use the app's CSV import to get the whole batch as a zip.",
        "fields": [{"name": "text", "label": "One link or text per line", "placeholder": "https://example.com/table-1\nhttps://example.com/table-2\nhttps://example.com/table-3", "el": "textarea"}],
        "build": "return String(v.text||'').split('\\n')[0].trim();",
        "bulk": True,
        "body": [
            ("What bulk generation is for",
             "Table numbers, asset tags, ticket batches, inventory labels, classroom equipment — anything where you need dozens or hundreds of codes that differ only slightly."),
            ("Doing it properly with CSV",
             "The TrustScan app takes a CSV with the content in the first column and an optional name in the second, generates every code, and hands you a zip of PNGs or SVGs with sensible filenames. That is far less tedious than downloading them individually."),
        ],
    },
    {
        "id": "app", "slug": "app-download-qr-code-generator", "nav": "App download",
        "h1": "App Download QR Code Generator",
        "title": "App Store QR Code Generator — Free App Download QR | TrustScan",
        "desc": "Create a free QR code for your app. Scanning opens your App Store or Google Play listing so people can install without searching.",
        "kw": "app store qr code, google play qr code, app download qr code generator",
        "intro": "Put your store listing on a poster, a slide or a business card. Scanning opens the listing so nobody has to search a store and pick the wrong result.",
        "fields": [{"name": "url", "label": "App Store or Google Play link", "placeholder": "https://play.google.com/store/apps/details?id=…", "type": "url"}],
        "build": "return v.url || '';",
        "body": [
            ("One code for both stores",
             "If you publish on both, point the code at a page on your own site that detects the device and forwards accordingly. That keeps one printed code valid for everyone."),
        ],
    },
    {
        "id": "zoom", "slug": "zoom-meeting-qr-code-generator", "nav": "Zoom meeting",
        "h1": "Zoom Meeting QR Code Generator",
        "title": "Zoom QR Code Generator — Free Meeting Link QR Code | TrustScan",
        "desc": "Create a free QR code for a Zoom, Teams or Meet link. Scanning joins the meeting — no long link to type, no meeting ID to read out.",
        "kw": "zoom qr code generator, meeting qr code, teams meeting qr code, google meet qr code",
        "intro": "Paste any meeting link — Zoom, Teams, Google Meet — and print the code on the room card, the agenda or the slide.",
        "fields": [{"name": "url", "label": "Meeting link", "placeholder": "https://zoom.us/j/1234567890", "type": "url"}],
        "build": "return v.url || '';",
        "body": [
            ("A note on recurring meetings",
             "Use the recurring meeting link rather than a one-off, otherwise the printed code is dead after the first session."),
        ],
    },
    {
        "id": "form", "slug": "google-form-qr-code-generator", "nav": "Google Form",
        "h1": "Google Form QR Code Generator",
        "title": "Google Form QR Code Generator — Free Survey QR",
        "desc": "Create a free QR code for a Google Form or survey. Scanning opens the form so people can respond on the spot — no link to type.",
        "kw": "google form qr code, survey qr code generator, feedback qr code, form qr code",
        "intro": "Feedback forms, sign-up sheets, registers, quizzes. Paste the form link and print the code where people are standing.",
        "fields": [{"name": "url", "label": "Form link", "placeholder": "https://forms.gle/…", "type": "url"}],
        "build": "return v.url || '';",
        "body": [
            ("Use the short share link",
             "Google's forms.gle short link makes a much less dense code than the long /viewform address, which means it scans faster and prints smaller."),
        ],
    },
    {
        "id": "pdf", "slug": "pdf-qr-code-generator", "nav": "PDF document",
        "h1": "PDF QR Code Generator",
        "title": "PDF QR Code Generator — Free Document QR Code",
        "desc": "Create a free QR code that opens a PDF. Manuals, price lists, brochures, certificates and instructions — scanned straight from print.",
        "kw": "pdf qr code generator, qr code for pdf, document qr code",
        "intro": "Link a printed page to the full document. Manuals, spec sheets, price lists, safety instructions and certificates.",
        "fields": [{"name": "url", "label": "PDF address", "placeholder": "https://example.com/manual.pdf", "type": "url"}],
        "build": "return v.url || '';",
        "body": [
            ("The file has to be public",
             "The QR code just carries the address. If the file sits behind a login or in a private drive folder, scanning gets a permission screen. Upload it somewhere openly readable."),
        ],
    },

    # --- payment ----------------------------------------------------------
    {
        "id": "paypal", "slug": "paypal-qr-code-generator", "nav": "PayPal",
        "h1": "PayPal QR Code Generator",
        "title": "PayPal QR Code Generator — Free PayPal.Me QR",
        "desc": "Create a free PayPal QR code from your PayPal.Me name. Customers scan and pay you — optionally with the amount already filled in.",
        "kw": "paypal qr code generator, paypal me qr code, payment qr code",
        "intro": "Turn your PayPal.Me name into a code customers can scan to pay. Add an amount to pre-fill it.",
        "fields": [
            {"name": "name", "label": "PayPal.Me name", "placeholder": "yourname"},
            {"name": "amount", "label": "Amount", "placeholder": "Optional, e.g. 25.00"},
        ],
        "build": "var n=String(v.name||'').replace(/^.*paypal\\.me\\//i,'').replace(/^\\//,'');"
                 "return n?('https://paypal.me/'+n+(v.amount?'/'+v.amount:'')):'';",
        "body": [
            ("Setting up PayPal.Me",
             "Create your PayPal.Me link in the PayPal app under “Request money”. It is a short public name, not your email address, so you can print it without exposing your account address."),
            ("Check the name before you print",
             "Scan your own code and confirm it lands on your page with your name showing. A printed payment code with a typo sends money to whoever owns that name."),
        ],
    },
    {
        "id": "upi", "slug": "upi-qr-code-generator", "nav": "UPI payment",
        "h1": "UPI QR Code Generator",
        "title": "UPI QR Code Generator — Free UPI Payment QR Code | TrustScan",
        "desc": "Create a free UPI QR code from your UPI ID. Works with Google Pay, PhonePe, Paytm and any UPI app. Add an amount and a note.",
        "kw": "upi qr code generator, upi payment qr code, google pay qr code, phonepe qr code",
        "intro": "Enter your UPI ID and the code works with every UPI app — Google Pay, PhonePe, Paytm, BHIM and the rest.",
        "fields": [
            {"name": "pa", "label": "UPI ID", "placeholder": "yourname@bank"},
            {"name": "pn", "label": "Your name", "placeholder": "As it should appear"},
            {"name": "am", "label": "Amount", "placeholder": "Optional"},
            {"name": "tn", "label": "Note", "placeholder": "Optional"},
        ],
        "build": "if(!v.pa)return ''; var q=['pa='+encodeURIComponent(v.pa)];"
                 "if(v.pn)q.push('pn='+encodeURIComponent(v.pn));"
                 "if(v.am)q.push('am='+encodeURIComponent(v.am));"
                 "if(v.tn)q.push('tn='+encodeURIComponent(v.tn));"
                 "q.push('cu=INR'); return 'upi://pay?'+q.join('&');",
        "body": [
            ("What goes in a UPI QR code",
             "The payee address (your UPI ID), your display name, and optionally a fixed amount and note. Leave the amount blank for a tip jar or an open counter and the payer types their own."),
            ("Verify before printing at scale",
             "Scan it with your own phone and check the name that appears matches yours before you print a hundred of them."),
        ],
    },
    {
        "id": "bitcoin", "slug": "bitcoin-qr-code-generator", "nav": "Bitcoin",
        "h1": "Bitcoin QR Code Generator",
        "title": "Bitcoin QR Code Generator — Free BTC Address QR",
        "desc": "Create a free Bitcoin QR code from your wallet address, with an optional amount and label. Standard BIP-21 format, works with every wallet.",
        "kw": "bitcoin qr code generator, btc qr code, crypto wallet qr code, bitcoin address qr",
        "intro": "Encode a Bitcoin address in the standard BIP-21 format every wallet understands, with an optional amount and label.",
        "fields": [
            {"name": "address", "label": "Bitcoin address", "placeholder": "bc1q…"},
            {"name": "amount", "label": "Amount in BTC", "placeholder": "Optional, e.g. 0.005"},
            {"name": "label", "label": "Label", "placeholder": "Optional"},
        ],
        "build": "if(!v.address)return ''; var q=[];"
                 "if(v.amount)q.push('amount='+encodeURIComponent(v.amount));"
                 "if(v.label)q.push('label='+encodeURIComponent(v.label));"
                 "return 'bitcoin:'+v.address+(q.length?'?'+q.join('&'):'');",
        "body": [
            ("Check every character",
             "A crypto payment cannot be reversed. Copy and paste the address rather than typing it, then scan your own printed code with a wallet and confirm the address matches before you use it."),
            ("Use a high error correction level",
             "Wallet addresses are long, which makes a dense code. Set error correction to High or Highest and print larger than you think you need."),
        ],
    },
    {
        "id": "crypto", "slug": "ethereum-qr-code-generator", "nav": "Ethereum",
        "h1": "Ethereum QR Code Generator",
        "title": "Ethereum QR Code Generator — Free ETH Wallet QR",
        "desc": "Create a free Ethereum QR code from your wallet address, with an optional amount. Standard EIP-681 format, compatible with MetaMask and other wallets.",
        "kw": "ethereum qr code generator, eth qr code, metamask qr code, crypto address qr",
        "intro": "Encode an Ethereum address in the standard format wallets recognise, with an optional amount.",
        "fields": [
            {"name": "address", "label": "Ethereum address", "placeholder": "0x…"},
            {"name": "amount", "label": "Amount in ETH", "placeholder": "Optional"},
        ],
        "build": "if(!v.address)return '';"
                 "if(!v.amount)return 'ethereum:'+v.address;"
                 # EIP-681 value is denominated in wei, not ETH.
                 "var eth=parseFloat(v.amount); if(!isFinite(eth)||eth<=0)return 'ethereum:'+v.address;"
                 "return 'ethereum:'+v.address+'?value='+eth+'e18';",
        "body": [
            ("Verify before you publish",
             "Scan your own code with the wallet you intend people to use and check the address matches character for character. Transfers to a wrong address are permanent."),
        ],
    },

    # --- social -----------------------------------------------------------
    {"id": "instagram", "slug": "instagram-qr-code-generator", "nav": "Instagram",
     "h1": "Instagram QR Code Generator",
     "title": "Instagram QR Code Generator — Free Profile QR Code | TrustScan",
     "desc": "Create a free Instagram QR code for your profile. Scanning opens your account so people can follow you without searching.",
     "kw": "instagram qr code generator, instagram profile qr code, social media qr code",
     "intro": "Put your Instagram profile on a poster, a shop window or the back of a card.",
     **social("instagram", "Instagram username", "yourname", "https://instagram.com/"),
     "body": [("Why not the in-app code?", "Instagram's own nametag code only works inside the Instagram app. This one is a normal web link, so any camera opens it — including for people who do not have the app installed yet, who get the profile in a browser and a prompt to install.")]},

    {"id": "facebook", "slug": "facebook-qr-code-generator", "nav": "Facebook",
     "h1": "Facebook QR Code Generator",
     "title": "Facebook QR Code Generator — Free Page QR Code | TrustScan",
     "desc": "Create a free Facebook QR code for your page or profile. Scanning opens it directly so customers can follow, message or review you.",
     "kw": "facebook qr code generator, facebook page qr code, fb qr code",
     "intro": "Link straight to your Facebook page. Works for business pages, groups and personal profiles.",
     **social("facebook", "Facebook page name or username", "yourpage", "https://facebook.com/"),
     "body": [("Use your page's username", "Set a custom username for your page in Facebook settings — it makes a much shorter, cleaner code than the numeric profile ID.")]},

    {"id": "youtube", "slug": "youtube-qr-code-generator", "nav": "YouTube",
     "h1": "YouTube QR Code Generator",
     "title": "YouTube QR Code Generator — Channel and Video QR",
     "desc": "Create a free YouTube QR code for a channel or video. Scanning opens it straight in the YouTube app — for packaging, manuals and signage.",
     "kw": "youtube qr code generator, youtube video qr code, channel qr code",
     "intro": "Link a printed page to a video — assembly instructions, product demos, tutorials. Paste any YouTube address.",
     "fields": [{"name": "url", "label": "YouTube channel or video link", "placeholder": "https://youtube.com/watch?v=…", "type": "url"}],
     "build": "return v.url || '';",
     "body": [("Great on packaging", "A short assembly video reached by scanning the box beats a folded instruction sheet nobody reads, and costs nothing to update.")]},

    {"id": "tiktok", "slug": "tiktok-qr-code-generator", "nav": "TikTok",
     "h1": "TikTok QR Code Generator",
     "title": "TikTok QR Code Generator — Free Profile QR Code | TrustScan",
     "desc": "Create a free TikTok QR code for your profile. Scanning opens your account so people can follow you straight away.",
     "kw": "tiktok qr code generator, tiktok profile qr code",
     "intro": "Send people to your TikTok profile from anything printed.",
     **social("tiktok", "TikTok username, without the @", "yourname", "https://tiktok.com/@"),
     "body": [("Handles change, codes do not", "A printed code points at whatever username you enter today. Change your handle later and the code breaks — so print in quantity only once the name is settled.")]},

    {"id": "x", "slug": "twitter-x-qr-code-generator", "nav": "X / Twitter",
     "h1": "X (Twitter) QR Code Generator",
     "title": "X Twitter QR Code Generator — Free Profile QR Code | TrustScan",
     "desc": "Create a free QR code for your X (formerly Twitter) profile. Scanning opens your account directly, from print, slides or signage.",
     "kw": "twitter qr code generator, x qr code, twitter profile qr code",
     "intro": "Link to your X profile from print, slides or signage.",
     **social("x", "X username, without the @", "yourname", "https://x.com/"),
     "body": [("x.com and twitter.com", "Both addresses still resolve to the same profile. This uses x.com, which is the current canonical form.")]},

    {"id": "linkedin", "slug": "linkedin-qr-code-generator", "nav": "LinkedIn",
     "h1": "LinkedIn QR Code Generator",
     "title": "LinkedIn QR Code Generator — Free Profile QR Code | TrustScan",
     "desc": "Create a free LinkedIn QR code for your profile or company page. Ideal for conference badges, CVs and business cards.",
     "kw": "linkedin qr code generator, linkedin profile qr code, qr code for cv",
     "intro": "Put your LinkedIn profile on a conference badge, a CV or a business card.",
     **social("linkedin", "LinkedIn profile path, e.g. in/yourname", "in/yourname", "https://linkedin.com/"),
     "body": [("Where to find your path", "Open your LinkedIn profile and copy the part of the address after linkedin.com — usually in/yourname for a person, or company/yourcompany for an organisation.")]},

    {"id": "telegram", "slug": "telegram-qr-code-generator", "nav": "Telegram",
     "h1": "Telegram QR Code Generator",
     "title": "Telegram QR Code Generator — Channel and Chat QR",
     "desc": "Create a free Telegram QR code for your username, channel or group. Scanning opens the chat directly, with no link to type out.",
     "kw": "telegram qr code generator, telegram channel qr code, telegram link qr",
     "intro": "Link to a Telegram profile, channel or group.",
     **social("telegram", "Telegram username or channel, without the @", "yourname", "https://t.me/"),
     "body": [("Channels and groups too", "The same format works for public channels and groups — use the public name exactly as it appears after t.me in the invite link.")]},

    {"id": "snapchat", "slug": "snapchat-qr-code-generator", "nav": "Snapchat",
     "h1": "Snapchat QR Code Generator",
     "title": "Snapchat QR Code Generator — Free Profile QR Code | TrustScan",
     "desc": "Create a free Snapchat QR code for your username. Scanning opens your profile so people can add you — works with any phone camera.",
     "kw": "snapchat qr code generator, snapchat username qr code",
     "intro": "Send people to your Snapchat profile from anywhere printed.",
     **social("snapchat", "Snapchat username", "yourname", "https://snapchat.com/add/"),
     "body": [("Different from Snapcodes", "Snapchat's own Snapcode is a proprietary pattern that only the Snapchat camera reads. This is an ordinary QR code, so any phone camera works.")]},

    {"id": "spotify", "slug": "spotify-qr-code-generator", "nav": "Spotify",
     "h1": "Spotify QR Code Generator",
     "title": "Spotify QR Code Generator — Playlist and Track QR",
     "desc": "Create a free Spotify QR code for a track, album, artist or playlist. Scanning opens it in Spotify — good for posters, menus and events.",
     "kw": "spotify qr code generator, spotify playlist qr code, music qr code",
     "intro": "Share a playlist, album or track. Paste any Spotify link.",
     "fields": [{"name": "url", "label": "Spotify link", "placeholder": "https://open.spotify.com/playlist/…", "type": "url"}],
     "build": "return v.url || '';",
     "body": [("Getting the link", "In Spotify, use Share → Copy link. The copied address works for tracks, albums, artists and playlists alike.")]},

    {"id": "pinterest", "slug": "pinterest-qr-code-generator", "nav": "Pinterest",
     "h1": "Pinterest QR Code Generator",
     "title": "Pinterest QR Code Generator — Free Profile QR Code | TrustScan",
     "desc": "Create a free Pinterest QR code for your profile or board. Scanning opens it directly, so people can follow you without searching.",
     "kw": "pinterest qr code generator, pinterest board qr code",
     "intro": "Link to your Pinterest profile or a specific board.",
     **social("pinterest", "Pinterest username", "yourname", "https://pinterest.com/"),
     "body": [("Boards work too", "For a single board, use the Website link type instead and paste the full board address.")]},
]



# --- informational cluster -------------------------------------------------
#
# The 32 tool pages all chase transactional "X qr code generator" terms, which
# are dominated by domains with fifteen years of authority. A new domain does
# not win those. These pages target question queries instead: lower
# competition, clearer intent, and they funnel to the tools.
#
# Each opens with a 40-55 word direct answer immediately after the H2 question.
# That is the shape Google lifts for a featured snippet; burying the answer
# under three paragraphs of preamble forfeits it.

GUIDES = [
  {
    "slug": "why-is-my-qr-code-not-scanning",
    "h1": "Why Is My QR Code Not Scanning?",
    "title": "Why Is My QR Code Not Scanning? 12 Causes and Fixes",
    "desc": "Your QR code will not scan? The twelve real causes in the order they actually happen — size, quiet zone, contrast, density, curved surfaces and more.",
    "kw": "qr code not scanning, qr code won't scan, why won't my qr code scan, qr code not working, qr code scanning problems",
    "answer": "A QR code usually fails to scan for one of three reasons: it is printed too small for the distance it is read from, its white border has been cropped, or there is too little contrast between the code and its background. Size and quiet zone account for most real-world failures.",
    "sections": [
      ("Start here: is it the code or the destination?",
       """<p>Before redesigning anything, rule out the boring possibility. Scan the
      code yourself and read what comes back. If your phone shows the correct
      address and the page simply fails to load, the code is fine and the
      problem is your website, your hosting, or a typo in the URL you encoded.</p>
      <p>This catches a surprising share of reported failures, particularly with
      <a href="restaurant-menu-qr-code-generator.html">menu QR codes</a> pointing
      at a PDF that was moved or a file-sharing link that expired. Fixing the
      destination costs nothing; reprinting a thousand table cards does not.</p>"""),

      ("1. It is printed too small",
       """<p>This is the most common cause by a wide margin. A QR code needs to be
      roughly one tenth of the distance it will be scanned from. Below about
      2 cm, phone cameras cannot reliably resolve individual modules no matter
      how good the camera is, because of minimum focus distance rather than
      resolution.</p>
      <table>
        <thead><tr><th>Where it is</th><th>Scan distance</th><th>Minimum width</th></tr></thead>
        <tbody>
          <tr><td>Business card</td><td>20–25 cm</td><td>2–2.5 cm</td></tr>
          <tr><td>Restaurant table card</td><td>30–40 cm</td><td>3–4 cm</td></tr>
          <tr><td>Product packaging</td><td>25 cm</td><td>2.5 cm</td></tr>
          <tr><td>A4 poster</td><td>1 m</td><td>10 cm</td></tr>
          <tr><td>Shop window</td><td>2 m</td><td>20 cm</td></tr>
          <tr><td>Van livery</td><td>3 m</td><td>30 cm</td></tr>
          <tr><td>Billboard</td><td>10 m</td><td>1 m</td></tr>
        </tbody>
      </table>
      <p>Vehicle livery is the one people underestimate most: a code on a van
      door that looks generous in the artwork is unreadable from the pavement.
      There is more detail in the
      <a href="qr-code-size-for-printing.html">guide to QR code size for
      printing</a>.</p>"""),

      ("2. The quiet zone has been cropped",
       """<p>Every QR code needs a clear margin around it — the quiet zone — equal
      to four modules on each side. Scanners use it to work out where the code
      ends and the world begins. Without it, the algorithm cannot lock onto the
      code's boundary and simply never sees a code at all.</p>
      <p>Designers crop it constantly, because to the eye it looks like wasted
      white space in a tight layout. If your code sits flush against a coloured
      block, a photograph or the edge of a card, this is very likely your
      problem. Every code downloaded from this site already includes the quiet
      zone — do not trim it, and do not let a printer bleed into it.</p>"""),

      ("3. Contrast is too low, or inverted",
       """<p>Dark modules on a light background. That is the rule, and the margin
      for creativity is smaller than designers expect.</p>
      <ul>
        <li><strong>Pale grey on white</strong> fails on most phones. Anything
          lighter than about 40% grey is asking for trouble.</li>
        <li><strong>Light code on a dark background</strong> — an inverted code
          — works on modern iPhones and recent Android but fails on plenty of
          older scanners, which assume dark-on-light.</li>
        <li><strong>Two mid-tone colours</strong>, like a mid-blue code on a
          mid-green background, can look high-contrast to the eye while being
          nearly identical in luminance, which is what the scanner measures.</li>
      </ul>
      <p>If you are colouring a code on the
      <a href="qr-code-generator.html">generator</a>, keep the modules genuinely
      dark and the background genuinely light. The preset swatches there are all
      tested combinations.</p>"""),

      ("4. It is too dense for the size you printed",
       """<p>A long URL with tracking parameters, or a full
      <a href="vcard-qr-code-generator.html">vCard</a> with every field filled
      in, produces a version 10 or higher code with hundreds of tiny modules.
      Printed at the same physical size as a short code, each module is a
      fraction of the width, and the whole thing falls below what a camera can
      resolve.</p>
      <p>The fix is to shorten the content rather than enlarge the code. Drop
      UTM parameters. Use a short path on your own domain. For a vCard, include
      a name, one phone number, one email and a website — not a postal address,
      a fax number and three social profiles.</p>
      <p>Every generator on this site shows the version and module count as you
      type, so you can watch density climb and stop before it becomes a
      problem.</p>"""),

      ("5. The surface is curved, glossy or wet",
       """<p>Bottles, cups, tins and pens all wrap the code around a curve, which
      distorts its geometry. Scanners tolerate a little perspective distortion —
      that is what the corner finder patterns are for — but a tight curve breaks
      the grid entirely.</p>
      <p>Gloss laminate is the other frequent culprit: it throws the phone's
      flash straight back into the lens. Matt finishes scan far more reliably,
      and matt lamination on a restaurant table card is worth the small extra
      cost purely for scan rate.</p>"""),

      ("6. The camera cannot focus that close",
       """<p>Phone cameras have a minimum focus distance, commonly around 10 cm and
      worse on cheaper handsets. When a code will not scan, the instinct is to
      move closer — which pushes it inside the focus range and makes it worse.</p>
      <p>If you are testing and it will not read, back off to arm's length
      first. If your users are consistently holding it too close, the code is
      too small for the job.</p>"""),

      ("7. A logo is covering too much",
       """<p>A centre logo consumes error correction. Keep it under about a fifth
      of the code's area, and never let it touch the three large corner squares
      — those are the finder patterns the scanner uses to locate and orient the
      code at all.</p>
      <p>If you need a logo, raise error correction to High or Highest first.
      The full explanation of how much you can safely cover is in the
      <a href="qr-code-with-logo-scannable.html">logo guide</a>, and the
      <a href="qr-code-generator-with-logo.html">logo generator</a> handles the
      padding automatically.</p>"""),

      ("8. The code is damaged or partly obscured",
       """<p>Error correction can rebuild a remarkable amount — up to roughly 30%
      of the pattern at the highest level — but not if the damage lands on the
      three corner finder patterns. A scratch across the middle is usually
      survivable. A coffee ring over the top-left square is not.</p>
      <p>On printed material that gets handled, laminate it, and set error
      correction to High rather than the default Medium. The extra density is a
      worthwhile trade for something that lives on a table.</p>"""),

      ("9. Someone replaced it",
       """<p>Worth considering if a code that worked yesterday stopped working
      today, or if customers report being taken somewhere unexpected. Criminals
      place stickers over genuine QR codes on parking meters, tables and
      delivery cards, and a badly aligned sticker often fails to scan at all.</p>
      <p>Run a fingernail along the edge — a sticker over print has a lip you
      can catch. There is more on this in the guide to
      <a href="qr-code-sticker-scams.html">QR code sticker scams</a>, and you
      can <a href="qr-code-safety.html">check any address</a> a code gives you
      before opening it.</p>"""),

      ("10. The printer rendered it badly",
       """<p>Inkjet bleed thickens modules and closes the gaps between them.
      Screen printing on fabric distorts the grid. Thermal receipt printers fade
      within weeks. Anti-aliasing from a low-resolution PNG softens module edges
      into grey, which is exactly where a scanner looks for a hard transition.</p>
      <p>Use the <strong>SVG</strong> download for anything printed. It is
      mathematically sharp at any size, so the printer's RIP produces clean
      edges rather than interpolating a fixed pixel grid.</p>"""),

      ("11. It is a dynamic code and the service stopped",
       """<p>If the code came from a subscription QR service, it does not contain
      your destination — it contains a short link on that company's server,
      which forwards the scanner onward. If the subscription lapsed, the trial
      ended or the company shut down, every printed code dies at once and there
      is nothing wrong with the pattern at all.</p>
      <p>Scan it and read the address. If it shows a domain you have never heard
      of rather than your own, that is what happened. See
      <a href="do-qr-codes-expire.html">do QR codes expire</a> for the full
      explanation.</p>"""),

      ("12. You are testing with an unusual scanner",
       """<p>Some third-party scanner apps are worse than the built-in camera, and
      a few refuse formats the camera handles fine. Before concluding a code is
      broken, test with at least two phones — ideally one recent iPhone and one
      cheap Android, because that spread covers most of what your audience
      actually carries.</p>"""),

      ("A checklist before any print run",
       """<ol>
        <li>Print one at final size, on the final material.</li>
        <li>Scan it with a cheap Android phone, not just your own.</li>
        <li>Test it in the light the code will actually live in — dim restaurant,
          bright shop window, night-time street.</li>
        <li>Have someone unfamiliar with it try, from where a customer would
          stand.</li>
        <li>Confirm the destination loads, not just that the code reads.</li>
      </ol>
      <p>Five minutes here has saved more reprints than any other advice on this
      page.</p>"""),
    ],
    "cta": ("qr-code-generator.html", "Make a fresh QR code"),
  },
  {
    "slug": "qr-code-size-for-printing",
    "h1": "What Size Should a QR Code Be for Printing?",
    "title": "QR Code Size for Printing — The Rule That Actually Works",
    "desc": "How big a QR code needs to be for business cards, table cards, posters and billboards, with the distance rule and the minimum size below which nothing scans.",
    "kw": "qr code size, qr code minimum size, how big should a qr code be, qr code size for printing",
    "answer": "The working rule is that a QR code should be about one tenth of the distance it will be scanned from. A code read at 30 cm needs to be roughly 3 cm across; one read at 2 metres needs about 20 cm. The practical minimum is 2 cm regardless of distance.",
    "sections": [
      ("The distance rule",
       "Scanning distance divided by ten gives you the minimum width. It is a rule of thumb, not a standard, but it is derived from the resolution ordinary phone cameras achieve and it holds up well in practice. Add a margin if your audience skews older, since minimum focus distance worsens with cheaper and older phones."),
      ("Sizes for common uses",
       "Business card: 2–2.5 cm. Restaurant table card: 3–4 cm. A4 poster read from a metre: 10 cm. Shop window read from two metres: 20 cm. Billboard read from ten metres: a full metre. Vehicle livery is the one people underestimate most — a code on a van door read from three metres wants to be 30 cm."),
      ("Why 2 cm is the floor",
       "Below that, individual modules on a dense code fall under the size a phone camera can resolve at its minimum focus distance. A short URL in a version 2 code might survive at 1.5 cm; a vCard will not. If you are stuck with a small space, shorten the content rather than shrinking the code."),
      ("Use vector for print",
       "Download the SVG, not the PNG. A PNG has a fixed pixel grid and softens when enlarged; an SVG is mathematically sharp at any size, which matters most at the edges of modules where scanners look for transitions. Every generator on this site exports both."),
      ("Test before you commit to a print run",
       "Print one at final size, on the final material, and scan it with the cheapest Android phone you can find in the light the code will actually live in. Testing on a new iPhone under office lighting tells you almost nothing about a laminated card in a dim restaurant."),
    ],
    "cta": ("qr-code-generator.html", "Create a QR code and download the SVG"),
  },
  {
    "slug": "do-qr-codes-expire",
    "h1": "Do QR Codes Expire?",
    "title": "Do QR Codes Expire? Static vs Dynamic, Explained",
    "desc": "Static QR codes never expire — the destination is in the pattern. Dynamic ones can stop working at any time. Here is how to tell which kind you have.",
    "kw": "do qr codes expire, qr code expiry, does a qr code expire, qr code stop working",
    "answer": "Static QR codes never expire. The destination is encoded in the pattern itself, so a printed code works for as long as the page it points to exists. Dynamic QR codes can expire at any time, because they point at a third party's redirect service rather than at your content.",
    "sections": [
      ("What actually expires",
       "The code does not degrade and there is no clock inside it. What expires is the service in the middle. A dynamic code encodes something like <code>qrco.de/abc123</code>, and that short link only works while the company running it keeps working, keeps your account active, and keeps the redirect pointing where you asked."),
      ("How to tell which kind you have",
       "Scan it and read the address. If it shows your own domain, it is static. If it shows a short link on a company you have never printed on your packaging, it is dynamic — and that company controls where your customers go."),
      ("The trade-off, stated honestly",
       "Dynamic codes are genuinely useful: you can change the destination after printing and see scan counts. That is worth paying for in some campaigns. The cost is a permanent dependency and, usually, a subscription. For a menu, a Wi-Fi card or product packaging that has to work in five years, static is the safer choice."),
      ("What happens when a redirect service closes",
       "Every printed code pointing at it becomes a dead link at once. This has happened repeatedly as URL shorteners have shut down — Google's own goo.gl stopped serving most links in 2025. Anything printed at scale outlives the average startup."),
      ("Codes from this site are static",
       "Every generator here encodes the destination directly. There is no redirect, no account, no scan counter and nothing to renew. That also means we cannot change a code after you print it, which is the honest trade."),
    ],
    "cta": ("qr-code-generator.html", "Make a static QR code"),
  },
  {
    "slug": "can-a-qr-code-steal-your-information",
    "h1": "Can a QR Code Steal Your Information?",
    "title": "Can a QR Code Steal Your Information? What Is Really Possible",
    "desc": "A QR code cannot hack your phone by itself — it is only text. What it can do is take you somewhere designed to take your details. Here is the real risk.",
    "kw": "can a qr code steal your information, are qr codes safe, qr code virus, can qr codes hack your phone",
    "answer": "A QR code cannot steal anything by itself. It contains only text, and scanning it does not run code on your phone. The risk is where it sends you: a convincing fake login page, a payment form, or a file download. The danger is the destination, not the square.",
    "sections": [
      ("What a QR code physically is",
       "A pattern encoding a short piece of text — usually a web address. Your camera reads the text and offers to act on it. There is no program inside it and no mechanism for it to run anything. Claims that a QR code can install a virus by being looked at are wrong."),
      ("What can actually go wrong",
       "Three things. It opens a page that imitates a bank, a parking service or a delivery company, and you type your details in. It starts a file download that you then install. Or it connects your phone to a network someone else controls. All three require you to do something after scanning — which is precisely why reading the address first matters."),
      ("Why reading the address is hard on a phone",
       "Built-in scanners show a truncated preview in a small banner, and the truncation usually falls at the end of the domain, which is exactly where deception lives. <code>paypal.com.secure-billing.xyz</code> and <code>paypal.com</code> look identical when the tail is cut off in a phone-sized font."),
      ("The tricks that get past a quick glance",
       "Cyrillic letters that render identically to Latin ones. Punycode domains. A brand name hyphenated onto an unrelated domain. An <code>@</code> in the address, everything before which the browser ignores. Raw IP addresses written in hexadecimal. These are structural, which means software can catch them even when a person cannot."),
      ("What actually protects you",
       "Read the full address before opening. Never enter card details or passwords on a page you reached by scanning a code in public — type the company's address yourself instead. And use a scanner that checks the link rather than one that just opens it."),
    ],
    "cta": ("qr-code-safety.html", "Check a link now"),
  },
  {
    "slug": "qr-code-sticker-scams",
    "h1": "QR Code Sticker Scams: How They Work",
    "title": "QR Code Sticker Scams — Parking Meters, Menus and Deliveries",
    "desc": "Criminals stick their own QR code over the real one on parking meters, restaurant tables and delivery cards. How the scam works and how to spot a fake.",
    "kw": "qr code sticker scam, parking meter qr code scam, fake qr code, quishing, qr code fraud",
    "answer": "The scam is physical: a criminal prints a QR code sticker and places it over the genuine one on a parking meter, restaurant table or delivery card. Scanning it opens a convincing payment or login page. The code is not hacked — it has simply been replaced.",
    "sections": [
      ("Where it happens most",
       "Parking meters and pay-and-display machines, restaurant tables and menus, EV charging points, delivery cards pushed through letterboxes, and posters in stations. The pattern is consistent: places where paying by phone is normal, where you are in a hurry, and where nobody is watching the sign."),
      ("Why it works so well",
       "Every other kind of phishing gives you something to inspect. An email shows a sender address and a link you can hover over. A QR code shows a pattern of squares that means nothing to a human eye. You are being asked to trust something you cannot read, in a context that has trained you to scan without thinking."),
      ("How to spot a tampered code",
       "Run a fingernail along the edge — a sticker placed over print has a lip you can catch. Look for a mismatched shade of white, a slightly different size, or a code that sits oddly relative to the surrounding design. On official machinery, be suspicious of any code on a sticker at all: most councils and operators print directly onto the housing."),
      ("The pretexts to distrust",
       "Parking fines, failed deliveries and account suspensions. All three manufacture urgency, and urgency is the entire mechanism. A genuine parking machine takes payment without needing your card details typed into a web form on your phone."),
      ("What to do if you already scanned one",
       "Scanning alone does almost certainly nothing. If you entered card details, call your bank now and freeze the card. If you entered a password, change it wherever else you used it. If you installed anything, remove it. Then report the sticker to whoever owns the machine — most have no idea it is there."),
    ],
    "cta": ("qr-code-safety.html", "Check a link you scanned"),
  },
  {
    "slug": "qr-code-with-logo-scannable",
    "h1": "Will a Logo Stop a QR Code From Scanning?",
    "title": "QR Code With Logo — How Much You Can Cover Safely",
    "desc": "You can put a logo in a QR code without breaking it. How error correction makes that possible, how much you can cover, and the one area you must never touch.",
    "kw": "qr code with logo, can you put a logo on a qr code, qr code logo scannable, custom qr code logo",
    "answer": "A logo will not break a QR code if it covers less than about 20% of the area and never touches the three large corner squares. QR codes carry error correction that can rebuild up to 30% of a damaged pattern, and a centre logo simply consumes some of that headroom.",
    "sections": [
      ("How error correction makes it possible",
       "A QR code stores more data than it strictly needs. At the highest level, roughly 30% of the pattern can be missing and a scanner can still reconstruct the content from what remains. That redundancy exists for smudges, scratches and bad printing — a logo just spends it deliberately."),
      ("The three squares you must never cover",
       "The large squares at the top-left, top-right and bottom-left are the finder patterns. A scanner uses them to locate the code, work out its orientation and correct for the angle you are holding the phone at. Cover any part of one and the code becomes unreadable, no matter how much error correction you set."),
      ("Set error correction to High or Highest",
       "If you are adding a logo, raise the level. It makes the code denser — more modules for the same content — but it buys the redundancy the logo is about to consume. Our generator pages let you set this, and show the resulting version and module count as you change it."),
      ("Keep contrast, keep the pad",
       "Put the logo on a small pad of the background colour rather than directly over the modules. It gives the scanner a clean boundary and stops the logo's own edges being mistaken for data. Our renderer does this automatically."),
      ("Always test the final artwork",
       "Not the preview on your monitor — the actual printed piece, at final size, on the final material, with more than one phone. A logo QR that scans on your iPhone and fails on a five-year-old Android is a common and expensive discovery."),
    ],
    "cta": ("qr-code-generator-with-logo.html", "Add a logo to a QR code"),
  },
]

# --- rendering --------------------------------------------------------------

def nav_html(active_slug):
    items = []
    for t in TYPES:
        cls = ' class="active"' if t["slug"] == active_slug else ""
        items.append(f'<li><a href="{t["slug"]}.html"{cls}>{t["nav"]}</a></li>')
    return "\n        ".join(items)


# Replace with the Chrome Web Store listing URL the moment the extension is
# published. Until then the button lands on the download section, which is true;
# a dead store link is worse than a redirect.
CHROME_URL = "index.html#get"

HEADER = f"""<header class="site-head">
  <div class="wrap">
    <a class="brand" href="index.html"><img src="assets/img/logo96.png" alt="" width="32" height="32">TrustScan</a>
    <button class="nav-toggle" aria-label="Menu" aria-expanded="false"><span></span></button>
    <nav class="nav" data-open="false">
      <a href="qr-code-generator.html">QR generator</a>
      <a href="qr-code-safety.html">Link safety</a>
      <a href="index.html#faq">FAQ</a>
      <a href="support.html">Support</a>
      <a class="btn btn-chrome" href="{CHROME_URL}"><svg class="chrome-mark" viewBox="0 0 48 48" width="17" height="17" aria-hidden="true"><path fill="#EA4335" d="M14 6.68A20 20 0 0 1 44 24H34a10 10 0 0 0-15-8.66Z"/><path fill="#FBBC04" d="M44 24a20 20 0 0 1-30 17.32L19 32.66A10 10 0 0 0 34 24Z"/><path fill="#34A853" d="M14 41.32A20 20 0 0 1 14 6.68L19 15.34a10 10 0 0 0 0 17.32Z"/><circle cx="24" cy="24" r="10.5" fill="#fff"/><circle cx="24" cy="24" r="8.6" fill="#4285F4"/></svg>Chrome extension</a>
      <a class="btn btn-primary" href="index.html#get">Get the app</a>
    </nav>
  </div>
</header>"""

FOOTER_LINKS = """      <div>
        <h2>Popular</h2>
        <ul>
          <li><a href="qr-code-generator.html">QR code generator</a></li>
          <li><a href="wifi-qr-code-generator.html">Wi-Fi QR code</a></li>
          <li><a href="vcard-qr-code-generator.html">vCard QR code</a></li>
          <li><a href="google-review-qr-code-generator.html">Google review QR</a></li>
          <li><a href="bulk-qr-code-generator.html">Bulk QR codes</a></li>
        </ul>
      </div>
      <div>
        <h2>Guides</h2>
        <ul>
          <li><a href="why-is-my-qr-code-not-scanning.html">QR code not scanning</a></li>
          <li><a href="qr-code-size-for-printing.html">QR code size for print</a></li>
          <li><a href="do-qr-codes-expire.html">Do QR codes expire?</a></li>
          <li><a href="qr-code-sticker-scams.html">QR sticker scams</a></li>
        </ul>
      </div>
      <div>
        <h2>App</h2>
        <ul>
          <li><a href="https://play.google.com/store/apps/details?id=com.trustscan.scanner" rel="noopener noreferrer">Google Play</a></li>
          <li><a href="https://apps.apple.com/app/id6804426564" rel="noopener">App Store</a></li>
          <li><a href="qr-code-safety.html">Safety checks</a></li>
        </ul>
      </div>
      <div>
        <h2>Company</h2>
        <ul>
          <li><a href="about.html">About</a></li>
          <li><a href="support.html">Support</a></li>
          <li><a href="privacy.html">Privacy</a></li>
          <li><a href="mailto:info@trustscanqr.com">info@trustscanqr.com</a></li>
        </ul>
      </div>"""


def footer():
    return f"""<footer class="site-foot">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <a class="brand" href="index.html"><img src="assets/img/logo96.png" alt="" width="32" height="32">TrustScan</a>
        <p style="color:var(--muted);margin-top:.8rem;max-width:34ch">A QR code
          scanner that reads the link before you do.</p>
      </div>
{FOOTER_LINKS}
    </div>
    <div class="foot-legal">
      <span>© 2026 TrustScan</span>
      <span>Google Play is a trademark of Google LLC. App Store is a trademark of Apple Inc. All other trademarks belong to their respective owners.</span>
    </div>
  </div>
</footer>"""


def render_type_page(t):
    body_html = "\n".join(
        f"    <h2>{html.escape(h)}</h2>\n    <p>{p}</p>" for h, p in t["body"])

    preview_hidden = ' hidden' if t.get("bulk") else ''
    bulk_html = ("""
      <p class="preview-meta" id="bulk-count"></p>
      <div class="bulk-grid" id="bulk-out"></div>""" if t.get("bulk") else "")

    faq = FAQS.get(t["id"], [])
    faq_html = ""
    if faq:
        rows = "\n".join(
            f"      <details><summary>{html.escape(q)}</summary>"
            f"<p>{html.escape(a)}</p></details>" for q, a in faq)
        faq_html = f'''
    <h2>Frequently asked questions</h2>
    <div class="faq">
{rows}
    </div>
'''

    schemas = [{
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "QR code generators",
             "item": SITE + "/qr-code-generator.html"},
            {"@type": "ListItem", "position": 3, "name": t["h1"],
             "item": f"{SITE}/{t['slug']}.html"},
        ],
    }]
    if faq:
        schemas.append({
            "@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": q,
                 "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq],
        })
    schema_html = "\n".join(
        '<script type="application/ld+json">' + json.dumps(x) + "</script>"
        for x in schemas)
    other = [x for x in TYPES if x["id"] != t["id"]][:6]
    related = "\n".join(
        f'        <li><a href="{o["slug"]}.html">{o["h1"]}</a></li>' for o in other)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t["title"]}</title>
<meta name="description" content="{html.escape(t["desc"], quote=True)}">
<meta name="keywords" content="{t["kw"]}">
<link rel="canonical" href="{SITE}/{t["slug"]}.html">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta property="og:type" content="website">
<meta property="og:title" content="{html.escape(t["h1"], quote=True)} — free, nothing uploaded">
<meta property="og:description" content="{html.escape(t["desc"], quote=True)}">
<meta property="og:url" content="{SITE}/{t["slug"]}.html">
<meta property="og:image" content="{SITE}/assets/img/logo96.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="assets/img/logo96.png" type="image/png">
<meta name="referrer" content="strict-origin-when-cross-origin">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; font-src 'self'; connect-src 'none'; base-uri 'self'; form-action 'none';">
<link rel="preload" href="assets/fonts/Manrope-ExtraBold.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/Manrope-Regular.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/css/style.css">
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "WebApplication",
  "name": "{t["h1"]}",
  "url": "{SITE}/{t["slug"]}.html",
  "applicationCategory": "DesignApplication",
  "operatingSystem": "Any",
  "browserRequirements": "Requires JavaScript",
  "offers": {{ "@type": "Offer", "price": "0", "priceCurrency": "USD" }},
  "publisher": {{ "@type": "Organization", "name": "TrustScan", "url": "{SITE}/" }}
}}
</script>
</head>
<body data-qr-type="{t["id"]}">
<a class="skip" href="#main">Skip to the generator</a>
{HEADER}
<main id="main" tabindex="-1">
<section class="tool">
  <div class="wrap tool-grid">

    <details class="tool-nav" open>
      <summary>Other QR code types</summary>
      <p class="tool-nav-label">QR code types</p>
      <nav aria-label="QR code types"><ul>
        {nav_html(t["slug"])}
      </ul></nav>
    </details>

    <div class="tool-main">
      <h1>{t["h1"]}</h1>
      <p class="lede">{t["intro"]}</p>
      <div id="gen-fields"></div>
{bulk_html}
      <p class="hint">Free, unlimited, and no sign-up. Everything runs in this tab —
        what you type is never uploaded.</p>
    </div>

    <aside class="preview"{preview_hidden}>
      <div class="frame" style="padding:14px">
        <span class="frame-b1"></span><span class="frame-b2"></span>
        <canvas id="gen-canvas" role="img" width="330" height="330"
          aria-label="Live preview of your QR code">Your QR code appears here once you fill in the form.</canvas>
      </div>
      <p class="preview-meta" id="gen-meta" role="status" aria-live="polite"></p>
      <p class="gen-error" id="gen-error" role="alert"></p>

      <div class="field" style="text-align:left;margin-top:1rem">
        <label for="gen-ecc">Error correction</label>
        <select id="gen-ecc">
          <option value="L">Low — smallest code</option>
          <option value="M" selected>Medium — recommended</option>
          <option value="Q">High</option>
          <option value="H">Highest — survives damage</option>
        </select>
      </div>
      <div class="field" style="text-align:left">
        <label for="gen-shape">Module shape</label>
        <select id="gen-shape">
          <option value="rounded" selected>Rounded — modern</option>
          <option value="dots">Dots</option>
          <option value="square">Square — classic</option>
          <option value="diamond">Diamond</option>
        </select>
      </div>
      <div class="field" style="text-align:left">
        <label for="gen-eye">Corner style</label>
        <select id="gen-eye">
          <option value="rounded" selected>Rounded</option>
          <option value="circle">Circle</option>
          <option value="leaf">Leaf</option>
          <option value="square">Square</option>
        </select>
      </div>

      <div class="swatches">
        <label for="gen-fg">Code</label>
        <input type="color" id="gen-fg" value="#10111A">
        <label for="gen-eyecolor">Corners</label>
        <input type="color" id="gen-eyecolor" value="#0B5CFF">
        <label for="gen-bg">Back</label>
        <input type="color" id="gen-bg" value="#FFFFFF">
      </div>

      <div class="presets" id="gen-presets">
        <button type="button" data-preset="#10111A,#0B5CFF,#FFFFFF" title="Cobalt"></button>
        <button type="button" data-preset="#10111A,#10111A,#FFFFFF" title="Mono"></button>
        <button type="button" data-preset="#0B5CFF,#0B5CFF,#FFFFFF" title="All blue"></button>
        <button type="button" data-preset="#12996B,#0F7A55,#FFFFFF" title="Green"></button>
        <button type="button" data-preset="#D6274A,#A81C39,#FFFFFF" title="Red"></button>
        <button type="button" data-preset="#FFFFFF,#7FB0FF,#10111A" title="Inverted"></button>
      </div>

      <div class="logo-row">
        <input type="file" id="gen-logo" accept="image/*">
        <label for="gen-logo">Add a centre logo</label>
        <button type="button" id="gen-logo-clear">Remove</button>
      </div>

      <button class="btn btn-primary" id="dl-png" type="button">Download PNG</button>
      <button class="btn btn-ghost" id="dl-svg" type="button">Download SVG</button>
    </aside>
  </div>
</section>

<section class="section section-alt">
  <div class="wrap prose">
{body_html}
{faq_html}
    <h2>Check it before you print it</h2>
    <p>Scan your own code with your own phone before you commit it to print. And if
      you scan codes out in the world — parking meters, delivery notes, table cards —
      use a scanner that reads the address out and checks it first.
      <a href="qr-code-safety.html">See the 21 safety checks</a>.</p>

    <h2>More QR code generators</h2>
    <ul>
{related}
    </ul>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="cta-band">
      <h2>Scan with something that checks first</h2>
      <p>TrustScan reads every code, runs 21 checks on the address, and tells you
        what it found before the page opens. Free forever.</p>
      <div class="stores">
        <a class="store store-play" href="https://play.google.com/store/apps/details?id=com.trustscan.scanner" rel="noopener noreferrer">
          <svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#00D3FF" d="M3.61 2.30a1.5 1.5 0 0 0-.35.99v17.42c0 .38.13.72.35.99l.06.06L13.4 12v-.23L3.67 2.24z"/><path fill="#FFCE00" d="M16.66 15.29L13.4 12.03v-.23l3.26-3.26.07.04 3.86 2.19c1.1.63 1.1 1.65 0 2.28l-3.86 2.19z"/><path fill="#FF3A44" d="M16.73 15.25L13.4 11.92 3.61 21.70c.36.39.96.43 1.64.05z"/><path fill="#00F076" d="M16.73 8.59L5.25 2.09c-.68-.39-1.28-.34-1.64.05l9.79 9.78z"/></svg>
          <span><small>Get it on</small><b>Google Play</b></span>
        </a>
        <a class="store" href="{IOS_URL}" rel="noopener noreferrer">
          <span><small>Get it on</small><b>App Store</b></span>
        </a>
      </div>
    </div>
  </div>
</section>
</main>
{footer()}
{schema_html}
<script src="assets/js/qr.js"></script>
<script src="assets/js/types.js"></script>
<script src="assets/js/generator.js"></script>
<script src="assets/js/site.js"></script>
</body>
</html>
"""



def slugify(text):
    out = "".join(c.lower() if c.isalnum() else "-" for c in text)
    while "--" in out:
        out = out.replace("--", "-")
    return out.strip("-")


def render_guide_page(g):
    """An informational page targeting a question query.

    The 40-55 word direct answer sits immediately after the H1, before any
    prose. That is the shape Google lifts for a featured snippet; an answer
    buried under three paragraphs of preamble forfeits the position.
    """
    body = "\n".join(
        f'    <h2 id="{slugify(h)}">{html.escape(h)}</h2>\n{t}'
        for h, t in g["sections"])

    toc = "\n".join(
        f'        <li><a href="#{slugify(h)}">{html.escape(h)}</a></li>'
        for h, _ in g["sections"])

    others = [x for x in GUIDES if x["slug"] != g["slug"]]
    related = "\n".join(
        f'        <li><a href="{o["slug"]}.html">{o["h1"]}</a></li>' for o in others)

    schemas = [{
        "@context": "https://schema.org", "@type": "Article",
        "headline": g["h1"], "description": g["desc"],
        "author": {"@type": "Organization", "name": "TrustScan",
                   "url": SITE + "/about.html"},
        "publisher": {"@type": "Organization", "name": "TrustScan",
                      "logo": {"@type": "ImageObject",
                               "url": SITE + "/assets/img/logo96.png"}},
        "mainEntityOfPage": f"{SITE}/{g['slug']}.html",
        "datePublished": LASTMOD, "dateModified": LASTMOD,
    }, {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Guides",
             "item": SITE + "/qr-code-safety.html"},
            {"@type": "ListItem", "position": 3, "name": g["h1"],
             "item": f"{SITE}/{g['slug']}.html"},
        ],
    }]
    schema_html = "\n".join(
        '<script type="application/ld+json">' + json.dumps(x) + "</script>"
        for x in schemas)

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{g["title"]}</title>
<meta name="description" content="{html.escape(g["desc"], quote=True)}">
<meta name="keywords" content="{g["kw"]}">
<link rel="canonical" href="{SITE}/{g["slug"]}.html">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta property="og:type" content="article">
<meta property="og:site_name" content="TrustScan">
<meta property="og:title" content="{html.escape(g["h1"], quote=True)}">
<meta property="og:description" content="{html.escape(g["desc"], quote=True)}">
<meta property="og:url" content="{SITE}/{g["slug"]}.html">
<meta property="og:image" content="{SITE}/assets/img/logo96.png">
<meta property="og:image:width" content="1024">
<meta property="og:image:height" content="1024">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="assets/img/logo96.png" type="image/png">
<meta name="referrer" content="strict-origin-when-cross-origin">
<meta http-equiv="Content-Security-Policy" content="default-src \'none\'; script-src \'self\'; style-src \'self\' \'unsafe-inline\'; img-src \'self\' data: blob:; font-src \'self\'; connect-src \'none\'; base-uri \'self\'; form-action \'none\'">
<link rel="preload" href="assets/fonts/Manrope-ExtraBold.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/Manrope-Regular.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/css/style.css">
{schema_html}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{HEADER}
<main id="main" tabindex="-1">
<article class="section">
  <div class="wrap prose">
    <nav class="crumbs" aria-label="Breadcrumb">
      <a href="index.html">Home</a> <span aria-hidden="true">›</span> {g["h1"]}
    </nav>
    <h1>{g["h1"]}</h1>
    <p class="answer">{g["answer"]}</p>

    <nav class="toc" aria-label="On this page">
      <h2>On this page</h2>
      <ol>
{toc}
      </ol>
    </nav>

{body}

    <h2>Check a link before you trust it</h2>
    <p>Anyone can print a QR code and stick it over yours. TrustScan reads the
      address and runs 21 checks on it before the page opens — free, offline, and
      on every scan. <a href="qr-code-safety.html">Try the checker</a> or
      <a href="index.html#get">get the app</a>.</p>

    <p style="margin-top:2rem">
      <a class="btn btn-primary btn-lg" href="{g["cta"][0]}">{g["cta"][1]}</a>
    </p>

    <h2>Related guides</h2>
    <ul>
{related}
    </ul>
  </div>
</article>
</main>
{footer()}
<script src="assets/js/site.js"></script>
</body>
</html>
'''

def render_types_js():
    entries = []
    for t in TYPES:
        fields = json.dumps(t["fields"])
        entries.append(
            "  %s: { fields: %s, build: function (v) { %s } }"
            % (json.dumps(t["id"]), fields, t["build"]))
    return ("/* Generated by build.py — do not edit by hand. */\n"
            "window.QR_TYPES = {\n" + ",\n".join(entries) + "\n};\n")


def render_sitemap():
    urls = [("", "1.0", "weekly"),
            ("qr-code-safety.html", "0.9", "monthly"),
            ("about.html", "0.6", "yearly"),
            ("support.html", "0.4", "yearly"),
            ("privacy.html", "0.4", "yearly")]
    urls += [(g["slug"] + ".html", "0.9", "monthly") for g in GUIDES]
    urls += [(t["slug"] + ".html", "0.7", "monthly") for t in TYPES]
    body = "\n".join(
        f"  <url>\n    <loc>{SITE}/{u}</loc>\n"
        f"    <changefreq>{cf}</changefreq>\n    <priority>{p}</priority>\n  </url>"
        for u, p, cf in urls)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + body + "\n</urlset>\n")


if __name__ == "__main__":
    for t in TYPES:
        (OUT / f"{t['slug']}.html").write_text(render_type_page(t))
    for g in GUIDES:
        (OUT / f"{g['slug']}.html").write_text(render_guide_page(g))
    (OUT / "assets/js/types.js").write_text(render_types_js())
    (OUT / "sitemap.xml").write_text(render_sitemap())
    print(f"built {len(TYPES)} tool pages, {len(GUIDES)} guides, types.js, sitemap.xml")
