# Site Testing Checklist

This is a brief tick list intended to act as a reminder of the secondary and tertiary steps required to ship a site.

## SEO

Ensuring the site is findable and shareable.

### General site

- [ ] The site _must_ be classified as a PWA when running [Lighthouse](https://developer.chrome.com/docs/lighthouse/seo/). This includes a web manifest.
- [ ] The site and all pages _must_ have `<meta name="robots" content="index,follow" />`.
- [ ] The site _must_ have a working favicon following the SVG [method](https://evilmartians.com/chronicles/how-to-favicon-in-2021-six-files-that-fit-most-needs).
- [ ] The site _should_ have a thorough `sitemap.xml` route that can be submitted to search engines. If the site has a nested or dynamic route (e.g. `/org/[org]`), it is highly recommended to include a sitemap.
- [ ] The site's home page _should_ have a [`WebSite` JSON-LD](https://schema.org/WebSite) schema.

### Per-page

- [ ] Each page _must_ have a 100% SEO score on [Lighthouse](https://developer.chrome.com/docs/lighthouse/seo/).
- [ ] Each page _must_ have unique `<title>`, `<meta name='description' content=''>` and `<link  rel="canonical" href={url}` tags. See other recommended [meta tags](https://web.dev/learn/html/metadata/).
- [ ] Each page _must_ have a 1200x630 and a 1012x506 share image that is properly linked.
- [ ] Each page _should_ have an associated [JSON-LD](https://schema.org/docs/schemas.html) schema, strengthening the page's knowledge graph entry.

## Accessibility (a11y)

Ensuring the site is friendly to all users

- [ ] Each page _must_ have 0 issues when running [Deque's Axe extension](https://chrome.google.com/webstore/detail/axe-devtools-web-accessib/lhdoppojpmngadmnindnejefpokejbdd).
- [ ] Each page _must_ have 90% or greater (100% preferred) a11y score on [Lighthouse](https://developer.chrome.com/docs/lighthouse/accessibility/scoring/).
- [ ] `<img>` and `<picture>` elements _must_ have an `alt` attribute.
- [ ] `<svg>` elements _must_ have an `aria-label` attribute.
- [ ] `<video>` and `<audio>` elements _must_ have a `<track>` element.
- [ ] `<figure>` elements _must_ have a `<figcaption>` element.
- [ ] Each input, button or other interactive element _must_ be properly labelled using `aria-label` or visually hidden text.
- [ ] Focusable elements _must_ have a visual indicator on focus. (See [more](<[url](https://dequeuniversity.com/class/semantic-structure/links/visual-focus-indicator)>)). These elements _should_ have enhanced focus indication styles.
- [ ] Text links _must_ be visually distinct from surrounding text.
- [ ] Landmark elements or otherwise bespoke components _must_ utilize proper [WAI-ARIA roles](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Roles). If in doubt, no ARIA is better than bad ARIA.
- [ ] Noninteractive elements (`<rect>`, `<div>`, .etc) _must_ utilize `keydown` events in tandem with `focus` or `click` events.
- [ ] All elements using `mouseover` or `mouseout` events _must_ also utilize `focus` and `blur` events with identical functions.
- [ ] Animations _must_ be easily disabled if a user's motion preference is set to `prefers-reduced-motion`.
- [ ] Charts _must_ have an associated `<figcaption>` or likewise description, preferably with a `<table>`. This can be visually hidden.
- [ ] Each page _should_ be tested utilizing a screenreader such as [MacOS's Voiceover](https://www.apple.com/voiceover/info/guide/_1124.html).
- [ ] Each input, button or other interactive element _should_ be properly described using `aria-describedby` via visually hidden text.
- [ ] A group of links _should_ utilize the `aria-current="page"` attribute to signify the currently active page.
- [ ] External links _should_ indicate they are external using `aria-label="Opens in a new window"` or a `<span id='opens-new-window' aria-hidden="true" class="sr-only">(opens in new window)<span>`.
- [ ] Elements with appropriate tooltips _should_ utilize the [`tooltip` role](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Roles/tooltip_role) with associated attributes.
- [ ] `<canvas>` elements _should_ have a background fill enforcing the typical background color to avoid issues with high contrast.

## Performance

Ensuring the site is friendly to a user's GPU & CPU

- [ ] Each page _must_ have a `Good` (green) rating on CLS (Content Layout Shift).
- [ ] Each page _must_ [preload](https://web.dev/preload-critical-assets/) assets that appear within the first viewport or "above the fold".
- [ ] `svelte.config.js`'s [`kit.prerender.origin`](https://kit.svelte.dev/docs/configuration) _must_ be filled out with the appropriate URL origin.
- [ ] The site _should_ be [statically](https://www.npmjs.com/package/@sveltejs/adapter-static) rendered, if possible. Otherwise, it should be server-side rendered on [Vercel](https://www.npmjs.com/package/@sveltejs/adapter-vercel) using the platform adapter.
- [ ] Each page _should_ have a 90% or greater Core Web Vitals score on [Lighthouse](https://developer.chrome.com/docs/lighthouse/performance/) or [PageSpeed Insights](https://pagespeed.web.dev/).
- [ ] All fetches and data manipulations _should_ be [memoized](https://www.freecodecamp.org/news/memoization-in-javascript-and-react/) where applicable.
- [ ] Images _should_ be optimized using `@sveltejs/enhanced-img` and served as `<enhanced:img>` elements with automatic responsive sizing and format optimization.
- [ ] SVG _should_ be inlined to reduce network requests.

## Cross-compability

Ensuring the site is friendly to all browsers & devices. Utilize [BrowserStack](https://www.browserstack.com/users/sign_in) (Jack holds the keys) or test on owned devices. It is recommended to test on each combination of browser/device, emulating key interactions such as tooltips, searchbars, inputs and other reactive elements.

- [ ] Chrome/MacOS
- [ ] Safari/MacOS
- [ ] Firefox/MacOS
- [ ] Chrome/iPhone
- [ ] Safari/iPhone
- [ ] Firefox/iPhone
- [ ] Chrome/Windows
- [ ] Safari/Windows
- [ ] Firefox/Windows
- [ ] Chrome/Android
- [ ] Safari/Android
- [ ] Firefox/Android

## Developer Experience

Ensuring that we are all in sync and are documenting our work.

- [ ] Environment variables _must_ be added to Netlify, if applicable.
- [ ] The `.env.default` file _must_ be updated to include the keys (NO VALUES) for every environment variable.
- [ ] The `README.md`` _should_ be updated with site-specific information as applicable
