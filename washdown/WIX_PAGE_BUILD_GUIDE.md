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

The Wix API can't add pages to a site built in the classic Wix Editor, so the pages below have to be added in the Editor. Because the content lives in the CMS, you build **3 pages**: one main page, one dynamic series page (creates all 5 series pages) and one dynamic product page (creates all 24 product pages).

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

## Build order

Page 1 is done. Build **Page 3 before Page 2**, because the "View details" buttons on Page 2 can only link to Page 3 once it exists.

## Page 3: Product page (one dynamic page that creates all 24)

Go to **CMS → Washdown - Guns → More actions → Add dynamic page → Item page**.

1. **URL:** set it to `/washdown-gun/{slug}`, using the **Slug** field. You'll get addresses like `/washdown-gun/blue-king`.
2. **Layout**, from top to bottom. Connect each element by clicking it, then **Connect to CMS**, and choose the page's *Washdown - Guns* dataset:
   - **Image** → **Image**. Set the display to *Fit*.
   - **Heading** → **Product Name**.
   - **Sub-heading** → **Short Description**.
   - **Text box** → **Long Description**. The text already includes paragraph formatting.
   - **Specs:** 5 rows, each with a fixed label on the left and a text box connected to the field on the right:
     - Material → **Material**
     - Max pressure → **Max Pressure**
     - Max temperature → **Max Temperature**
     - Flow rate → **Flow Rate**
     - Other → **Other Specs**. Only Twistflow Handles uses this field. In the dataset's connection settings, turn on *Hide when empty* (or collapse it).
3. **"Back to series" button:** connect its link to the **Series** field. Wix should offer the *Washdown - Series (Item)* page there because Page 2 uses that collection. If it doesn't appear yet, finish Page 2 and come back to this step.
4. **"Request a brochure" button:** link it to your contact page or `mailto:info@nozzleworks.co.nz`.
5. **Contact banner:** *Discuss the options with our team*: 022 132 9900 · info@nozzleworks.co.nz
6. **SEO:** go to **Pages → this page → SEO basics**. Set the title to `{Product Name} | Washdown Guns | Nozzleworks` and the description to `{Short Description}`.

## Page 2: Series page with its product list (one dynamic page that creates all 5)

Go to **CMS → Washdown - Series → More actions → Add dynamic page → Item page**. Wix adds a dataset for the current series automatically.

1. **URL:** set it to `/washdown/{slug}`, using the **Slug** field. You'll get addresses like `/washdown/premium-series`.
2. **Header:** connect the heading to **Series Name**, the sub-heading to **Tagline** and a paragraph to **Intro**.
3. **Product list:**
   1. Go to **Add → CMS → Dataset** and connect it to **Washdown - Guns**. Rename it `gunsDataset` so it's easy to spot.
   2. **Filter:** click *Add filter*, choose the field **Series**, the condition **is**, and the value *Dataset → Washdown - Series* (the page's own dataset). This makes each series page show only its own products.
   3. **Sort:** Sort Order, ascending.
   4. **Items to load:** 12. That covers the largest series, Classic, with 10 products.
   5. Add a **Repeater** and connect it to `gunsDataset`. Lay out each card like this:
      - Image → **Image**, set to *Fit*
      - Title → **Product Name**
      - Text → **Short Description**
      - Optional quick-spec line → **Max Pressure** and **Max Temperature**, for example "24 bar · 95°C"
      - **"View details" button:** connect its link to the *Washdown - Guns (Item)* page (Page 3).
4. **Contact banner:** same as Page 3.
5. **SEO:** set the title to `{Series Name} | Washdown Guns | Nozzleworks` and the description to `{Tagline}`.

## Check the links between pages

- **Page 1 → Page 2:** each series card goes to `/washdown/...` and shows only that series' products.
- **Page 2 → Page 3:** each "View details" button opens the right product.
- **Page 3 → Page 2:** "Back to series" returns to the right series.
- Preview a few pages: Classic Series (10 products), Specialty Guns (2), and Twistflow Handles (the only product that shows Other Specs).

## Menu and product listing

- **Menu:** add *Washdown Guns* → `/washdown`, with 5 sub-items: `/washdown/classic-series`, `/washdown/premium-series`, `/washdown/specialty-guns`, `/washdown/twistflow-series`, `/washdown/shower-head-series`.
- **00 Products collection:** add a *Washdown* group item with Product Page = `https://www.nozzleworks.co.nz/washdown` once the page is published, so it appears with your other product groups. This wasn't done yet because the entry would go live straight away and link to a page that doesn't exist.

## Data source

`washdown_data.json` in this folder is the master copy of all series and product text, specs and Wix image references. `images/` holds the original photos.
