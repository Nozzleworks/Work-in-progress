# Washdown pages: Wix Editor build guide

Source: *Washdown Gun Range – Product line-up by series* (2-page PDF).

## What's already done in Wix (via API)

| Item | Where in Wix | Contents |
|---|---|---|
| 24 product photos | Media Manager (`classic.jpg`, `blue-king.jpg` …) | Cut from the PDF and padded onto 600×600 white squares so the product never touches the card edge. The CMS uses these padded versions; the originals are in `images/`. |
| **Washdown - Series** collection (`WashdownSeries`) | CMS | 5 items: Classic, Premium, Specialty Guns, Twistflow, Shower Head. Fields: Series Name, Slug, Tagline, Intro, Image, Sort Order |
| **Washdown - Guns** collection (`WashdownGuns`) | CMS | 24 products. Fields: Product Name, Slug, **Series** (reference to Washdown - Series), Image, Short Description, Long Description (loaded, from `long_descriptions.json`), Material, Max Pressure, Max Temperature, Flow Rate, Other Specs, Brochure (PDF, empty), Sort Order |

Product → series mapping:

- **Classic Series (10):** Classic, Classic Plus, Classic High-Flow, Classic Protection Plus, Classic Lite, Classic Hot Wash, Classic 1/2" or QC Outlet, Classic SS Food Grade, Classic SS Sterilisable, Classic ATEX
- **Premium Series (4):** Blue King, Blue Princess, Baby Series, Baby 1/2" or QC Outlet
- **Specialty Guns (2):** Air-Boosted Water Gun, Spray Gun XS Lite
- **Twistflow Series (5):** Twistflow WD Nozzle, Twistflow Lite WD Nozzle, Twistflow-L Lite, Twistflow M / L / XL, Twistflow Handles
- **Shower Head Series (3):** Shower Wash Head, The Squeezer, Squeezer Shower Head

The Wix API can't add pages to a site built in the classic Wix Editor, so the pages below have to be added in the Editor. Because the content lives in the CMS, you only build **2 pages** (one main, one dynamic). The dynamic page produces all 5 sub-pages automatically.

---

## Page 1: Washdown (main page, static)

**Editor → Pages & Menu → + Add Page → Blank.** Name it `Washdown Guns`, URL slug `washdown`.

1. **Header strip**
   - Heading: **Washdown Gun Range**
   - Sub-heading: *Washdown & cleaning guns by series*
   - Paragraph:
     > From everyday brass guns to food-grade stainless, ATEX-rated and water-saving models, our washdown range covers hose-down cleaning across food processing, agriculture and industry. Every gun has its own detailed brochure, so ask us for the one you need.
2. **Series grid**
   - Add a **Repeater** (or reuse the card layout from your other product-group pages).
   - **Add → CMS → Dataset**, connect it to **Washdown - Series**, sort by **Sort Order ascending**, and set items per load to 5.
   - Connect the card image to **Image**, the title to **Series Name**, and the text to **Tagline**.
   - Connect the card button (or the whole card) link to the **Washdown - Series (Item)** dynamic page. Do this after Page 2 exists.
3. **"Did you know? Why a trigger gun beats an open hose"** (5 tiles, copy from the PDF):
   - **Kinking kills hoses.** Folding a hose to stop the flow cracks the wall until it bursts. A trigger gun keeps it straight.
   - **You pay for water twice.** You pay once to bring it in and again to send it down the drain. A washdown gun's focused, high-impact spray cleans faster with less water, which cuts both bills.
   - **Less water, less heating.** Every litre you don't use is a litre you don't have to heat. A trigger gun with a focused spray cleans with less water, so your energy bill falls with it.
   - **Control where it counts.** Adjust the spray from a gentle rinse to a powerful jet, and stop the flow instantly with the trigger. The right force goes exactly where it's needed.
   - **Uncontrolled hoses injure people.** Burst hot-water hoses scald, dropped hoses whip, and pooled water causes slips. Release the trigger and the flow stops.
4. **Call to action:** *Discuss the options with our team*: 022 132 9900 · info@nozzleworks.co.nz

## Page 2: Series sub-pages (one dynamic page that produces all 5)

**CMS → Washdown - Series → More actions → Add dynamic page → Item page.**

1. Set the URL to `/washdown/{slug}`. Use the **Slug** field so you get clean URLs like `/washdown/classic-series` and `/washdown/premium-series`.
2. Bind the page heading to **Series Name**, the sub-heading to **Tagline**, and a paragraph to **Intro**.
3. **Product grid**
   - Add a second dataset connected to **Washdown - Guns**.
   - **Filter:** *Series* **is** *Washdown - Series dataset (current item)*.
   - **Sort:** Sort Order ascending. Set items per load to 12.
   - Add a Repeater connected to it. Card fields:
     - Image → **Image** (set to *Fit* so the guns aren't cropped)
     - Title → **Product Name**
     - Text → **Short Description**
     - Spec rows: **Material**, **Max Pressure**, **Max Temperature**, **Flow Rate** (and **Other Specs** for Twistflow Handles)
   - Optional "Request brochure" button linked to your contact page or `mailto:info@nozzleworks.co.nz`.
4. Add the "Discuss the options with our team" CTA strip.
5. **SEO (Pages → dynamic page → SEO basics):** title `{Series Name} | Washdown Guns | Nozzleworks`, description `{Tagline}`.

## Optional Page 3: individual product pages

If you want a page per gun (as you have for air blow guns at `/air-blow-gun/{model}`):
**CMS → Washdown - Guns → Add dynamic page → Item page**, with URL `/washdown-gun/{slug}`. Then link each card on Page 2 to it. Bind the **Long Description** field to a rich-text box. The **Brochure (PDF)** field is still empty, ready for each gun's brochure.

## Menu and product listing

- **Menu:** add *Washdown Guns* → `/washdown`, with 5 sub-items: `/washdown/classic-series`, `/washdown/premium-series`, `/washdown/specialty-guns`, `/washdown/twistflow-series`, `/washdown/shower-head-series`.
- **00 Products collection:** add a *Washdown* group item with Product Page = `https://www.nozzleworks.co.nz/washdown` once the page is published, so it appears with your other product groups. This wasn't done yet because the entry would go live straight away and link to a page that doesn't exist.

## Data source

`washdown_data.json` in this folder is the master copy of all series and product text, specs and Wix image references. `images/` holds the original photos.
