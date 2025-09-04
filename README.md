# The DataFace x SvelteKit

## Requirements

- [Node v20](https://github.com/nvm-sh/nvm)
- [pnpm](https://pnpm.io/)

## Getting started

1. Use Figma Handoff to facilitate design-to-dev token and font styling handoff

## Out-of-the-box features

- [SvelteKit](https://kit.svelte.dev/docs) as an app framework
- [Svelte](https://svelte.dev/docs) as a component framework
- [Vite](https://vitejs.dev/guide/) (with [Rollup](https://rollupjs.org/guide/en/)) as SvelteKit's default frontend tooling
- [@sveltejs/adapter-vercel](https://github.com/sveltejs/kit/tree/master/packages/adapter-vercel) for seamless Vercel deployments
- [@sveltejs/enhanced-img](https://kit.svelte.dev/docs/images) for optimized responsive images
- [Iconify](https://iconify.design/) + [Google Fonts](https://fonts.google.com/) for icons + fonts
- [TailwindCSS v4](https://tailwindcss.com/) + [PostCSS](https://postcss.org/) for styling with design tokens
- [bits-ui](https://bits-ui.com/) for accessible component primitives
- [ArchieML](http://archieml.org/) as a micro-CMS powered by Google Docs
- [Airtable](https://airtable.com/) integration for data management
- [ai2html](http://ai2html.org/) for responsive static images and charts
- [D3](https://github.com/d3/d3) + [LayerCake](https://layercake.graphics/) for charting

## Extensible features

Additionally, this template contains branches that integrate with third party services frequently used for client projects. To use any of these features, merge the corresponding branches into the main branch of the cloned project.

1. [Storyblok](https://www.storyblok.com/) Integration: [branch](https://github.com/the-dataface/df-sveltekit/tree/feature/storyblok)
2. [Supabase](https://supabase.com/) Integration: [branch](https://github.com/the-dataface/df-sveltekit/tree/feature/supabase)
3. [PDF Generation](https://pdf-lib.js.org/): [branch](https://github.com/the-dataface/df-sveltekit/tree/feature/pdfs)

## Scripts

#### `pnpm run fetch:sheet`

This template has out-of-the-box features to help with consuming data from google sheets. Tag the Google Sheet for your graphic in `google.config.json` and make sure you have the ID and sheet ID (gid) filled out correctly. Make sure the share permissions on the sheet are set up so that it is viewable by anyone with the share link. **Note: Don't make it available to edit by anybody!**

Directly import csv's into your .svelte file via [@rollup/plugin-dsv](https://www.npmjs.com/package/@rollup/plugin-dsv)

```js
import data from '$lib/data/data.csv';
```

#### `pnpm run fetch:doc`

Like a lot of newsrooms, we use a Google Doc and ArchieMl approach to make copy content management easier. The setup is similar to using Sheets data. Make sure the share permissions on the doc are set up so that it is viewable by anyone with the share link. The just grab the document ID from the address bar — ...com/document/d/**1IiA5a5iCjbjOYvZVgPcjGzMy5PyfCzpPF-LnQdCdFI0**/edit — and paste it into the respective property in `google.config.json`.

[htmlparser2](https://www.npmjs.com/package/htmlparser2) and [html-entities](https://www.npmjs.com/package/html-entities) act as a middle man to catch various tags like `<a>`, `<h*>`, `<ul>` and more.

Import copy into your package like any JSON file

```js
import copy from '$lib/data/copy.json';
```

#### `pnpm run fetch:airtable`

This template integrates with Airtable for structured data management. Configure your Airtable base and table information in the environment variables and use the fetch script to pull data into your project. This is automatically run during the build process.

## Development

```shell
nvm use
pnpm install
pnpm run dev
```

Modify content in `src`. Pages live in `src/routes` and contents live in `src/lib`.

### Asset management

For image optimization, use [@sveltejs/enhanced-img](https://kit.svelte.dev/docs/images) which provides automatic optimization and responsive images.

[Vite's Static Asset Handling](https://vitejs.dev/guide/assets.html) lets us import image and SVG files with several options.

#### As files

Imports the hashed file name for the asset. For example, `imgUrl` will be `/img.png` during development, and become `/assets/img.2d8efhg.png` in the production build.

```js
import imgUrl from '$lib/assets/img.png';
```

#### As strings

Import raw strings by appending ?raw at the end. This is useful for SVG files.

```js
import imgUrl from '$lib/assets/img.svg?raw';
```

### Useful libs

- [body-scroll-lock](https://www.npmjs.com/package/body-scroll-lock) - Enables body scroll locking (for iOS Mobile and Tablet, Android, desktop Safari/Chrome/Firefox) without breaking scrolling of a target element (eg. modal/lightbox/flyouts/nav-menus).
- [focus-trap](https://www.npmjs.com/package/focus-trap) - Trap focus within a DOM node.
- [fullpage.js](https://www.npmjs.com/package/fullpage.js) - Create fullscreen scrolling websites.
- [gsap](https://www.npmjs.com/package/gsap) - Professional-grade animation for the modern web.
- [journalize](https://www.npmjs.com/package/journalize) - A collection of functions useful for making prose reader friendly.
- [lodash](https://www.npmjs.com/package/lodash) - Various helper functions.
- [slugify](https://www.npmjs.com/package/slugify) - Easily slug a string.
- [@sveltejs/svelte-scroller](https://www.npmjs.com/package/@sveltejs/svelte-scroller) - Svelte-y scrollytelling
- [svelte-select](https://www.npmjs.com/package/svelte-select) - A select/autocomplete component for Svelte apps. With support for grouping, filtering, async and more.
- [swiper](https://www.npmjs.com/package/swiper) - Modern mobile touch slider with hardware accelerated transitions and amazing native behavior.
- [svelte-french-toast](https://svelte-french-toast.com/) - Suave, extensible and accessible toasters

## Deployment

This is setup to use Vercel with the adapter configuration in `svelte.config.js`. The site can also be deployed to Netlify using the included `netlify.toml` file.

You can preview the built app with `pnpm run preview`.
