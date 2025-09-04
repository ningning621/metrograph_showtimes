# The DataFace's Style Guide

## Introduction

This document is a style guide for the DataFace project. It is intended to be a living document, and will be updated as the project evolves. The purpose of this document is to ensure that the codebase is consistent and easy to read. It is not intended to be a comprehensive guide to Svelte or TypeScript but rather a guide to the specific conventions used in this project.

## Table of Contents

- [Introduction](#introduction)
- [Table of Contents](#table-of-contents)
- [File Structure](#file-structure)
- [Naming Conventions](#naming-conventions)
- [Formatting](#formatting)
- [Comments](#comments)
- [Imports](#imports)
- [TypeScript](#typescript)
- [Svelte](#svelte)
- [CSS](#css)

## File Structure

The file structure of the average project is as follows:

```
static/ --static files to be served directly. Not to be imported into app. Font files, etc.
src/
	lib/ --development files
		actions/ --svelte actions for DOM interactions
		assets/ --assets to be imported into app. Use with @sveltejs/enhanced-img or Vite's .svg?raw query to mutate or inline assets.
		components/ --svelte components
			atoms/ --basic UI building blocks (Icon, etc.)
			charts/ --data visualization components (Map, Treemap, etc.)
			furniture/ --layout and page structure components (Head, Masthead, Colophon)
			interactivity/ --interactive UI components (Button, Dialog, Toggle, etc.)
			layout/ --layout and container components (Grid, Carousel, etc.)
			media/ --media-related components (ai2html integration)
			search/ --search functionality components and utilities (deprecated and needs updating)
		data/ --data files that can be imported
		styles/ --css files + design system (app.css, tokens.css, fonts.css, animations.css)
		utils/ --helper js/ts scripts
		stores.ts --global stores
		site.yaml --site metadata
	params/ --sveltekit route params
	routes/ --sveltekit page routes
		(app)/ --protected routes group
			[article]/ --dynamic article routes
		playground/ --component showcase and testing
		preview/ --preview route for password protection
		PageName/ --sveltekit page route. would be /PageName
			+page.svelte --sveltekit page. equal to index.html
			+page.js --sveltekit page script
			+page.yaml --page metadata + copy
	routes-templates/ --templates for common routes
		yamarkdown/ --template for yamarkdown pages, markdown-driven pages
	app.html --the html shell file
	app.d.ts --typescript declarations
scripts/ --build and data fetching scripts
	airtable/ --airtable integration scripts
	fetch/ --google docs/sheets fetching scripts
	img/ --image processing scripts
	publish/ --deployment scripts
```

## Naming Conventions

- **Directory & file names** _should_ be `kebab-case` (e.g. `my-file-name.ts`).
- **Route names** _should_ be `kebab-case` (e.g. `my-file-name/`).
- **Variable and prop names** _should_ be `camelCase` (e.g. `myVariable`). A prefixed `_` is permitted for private variables (e.g. `_myVariable`).
- **Boolean variable names** _should_ be prefixed with `is` (e.g. `isMyVariable`).
- **JavaScript Class names** _should_ be `PascalCase` (e.g. `MyClass`).
- **Component names** _should_ be `PascalCase` (e.g. `MyComponent`) and _should_ be imported using the same name.

## Formatting

The `.editorconfig` and `.eslintrc.cjs` files in the root should automatically handle formatting. Here are the main rules:

- **Indentation** _must_ be tabs.
- **Line length** _should_ be 80 characters.
- **Line breaks** _should_ be LF.
- **Quotes** _should_ be single quotes.
- **Semicolons** _should_ be included.

## Comments

JSDoc comments with TypeScript should be applied to all functions, classes and component props, allowing intellisense code completion in editors. It is recommended to use JSdoc comments for variables to improve readability, but it is not required. JSDoc comments should omit typings in favor of inline typings but should include at a minimum descriptions. Add examples and other JSDoc features as needed.

**Correct examples**

```ts
/** This is a parameter. */
type MyParam = string;

/**
 * This is a function that does something.
 * @param {MyParam} myParam
 * @returns {string} This is a return value.
 */
function myFunction(myParam: string): string {
	return myParam;
}

/** This is a comment explaining the below. */
const myVariable = 'myVariable';

/** This is a comment explaining the below, with types inline and comments using JSDoc. */
const myVariable: string | undefined = 'myVariable';

// only use $$Props if you need to type $$restProps. In this case, you should type props here and reference them during initialization.
interface $$Props extends svelteHTML.HTMLAttributes<HTMLElementTagNameMap['div']> {
	/** This is a comment explaining the myProp prop. */
	myProp?: string;
}
export let myProp: $$Props['myProp'] = undefined;

// Otherwise, type props inline with JSDoc comments above for descriptions only.

/** This is a comment explaining the prop */
export let myProp: string | undefined = undefined;
```

**Incorrect examples**

```ts
// This typing should be done inline. See `myVariable` above.

/** This describes the MyVariable type */
type MyVariable = string | undefined;
const myVariable: MyVariable = undefined;

// This should be typed inline instead of via JSDoc. Typescript will recognize the type and display it in intellisense.
/**  @type {?Href} Toggle between an `<a>` and a `<button>` element based on the `href` prop */
let href: Href | undefined = undefined;

// This typing should include props within the $$Props typing so that intellisense captures them.
interface $$Props {}
export let myProp: string | undefined = undefined;
```

## Imports

Imports should be grouped by type, with a line break between each group. Where possible, imports should be destructured to only import the required variables. Where unspecific, import external libraries prior to internal libraries. Types should be imported alongside existing imports from that library, with isolated types imported last. Local imports should be done via the `$lib/` path opposed to relative paths.

Imports should follow the given hierarchy:

1. Environment variables (e.g. `dev` from `'$app/env'`)
2. Core Svelte variables (e.g. `onMount` from `'svelte'`)
3. Nested Svelte variables (e.g. `writable` from `'svelte/store'`)
4. External libraries (e.g. `d3` from `'d3'`)
5. Internal libraries (e.g. `myFunction` from `'$lib/utils/myFunction'`)
6. Data files (e.g. `myData` from `'$lib/data/myData.csv'`)
7. Actions (e.g. `myAction` from `'$lib/actions/myAction'`)
8. Stores (e.g. `myStore` from `'$lib/stores'`)
9. External components (e.g. `MyComponent` from `'my-component'`)
10. Internal components (e.g. `MyComponent` from `'$lib/components/MyComponent'`)
11. Types (e.g. `type { MyType }` from `'$lib/file'`)

## TypeScript

All JavaScript and Svelte files should be written in TypeScript using the `.ts` extension. Svelte files should default to the rules below should conflicts arise. Global types should be written in `src/app.d.ts` if the type is general in nature. Generated types should be written to their own file (e.g. `cms.d.ts`) alongside `app.d.ts` and should be added to `tsconfig.json`'s `include` array. Otherwise, write types alongside components and documentation.

## Svelte

All Svelte files should be written in TypeScript using the `lang='ts'` attribute on the `<script>` tag. This project uses Svelte 5 with runes syntax. The following rules should be followed:

- **Component props** _should_ be typed using the `Props` interface pattern: `interface Props { myProp: MyType }` and `let { myProp }: Props = $props()`. If a component requires the use of `$$restProps`, include them in the Props interface: `interface Props extends HTMLAttributes<HTMLDivElement> { myProp: MyType }`.
- **State variables** _should_ use the `$state()` rune: `let myVariable = $state(false)`.
- **Derived values** _should_ use the `$derived()` rune: `let computedValue = $derived(someCalculation)`.
- **Effects** _should_ use the `$effect()` rune: `$effect(() => { /* side effects */ })`. Please use this only when necessary.
- **Explicitly true props** _should_ omit the value (e.g. `<Component myProp/> ` instead of `<Component myProp={true}/>`).
- **Snippets** _should_ be used instead of slots for content projection: `{@render children?.()}`.

Code should be ordered according to the following:

1. Imports (e.g. `import { myImport } from 'my-import'`)
2. Interface definitions (e.g. `interface Props { myProp: MyType }`)
3. Props destructuring (e.g. `let { myProp }: Props = $props()`)
4. State variables (e.g. `let myVariable = $state(false)`)
5. Derived values (e.g. `let computed = $derived(calculation)`)
6. Functions and event handlers (e.g. `const handleClick = () => {}`)
7. Effects (e.g. `$effect(() => {})`)
8. Context setters (e.g. `setContext('my-context', myVariable)`)

## CSS

CSS is to be primarily written using [TailwindCSS v4](https://tailwindcss.com/). This project uses the new `@theme` syntax for design tokens and CSS-first configuration. If custom CSS is required, use PostCSS syntax in the chosen component with nesting and Tailwind where applicable. Global styles are to be written in `src/lib/styles/app.css`.

Design tokens are defined in `src/lib/styles/tokens.css` using the `@theme` directive:

```css
@theme {
	--color-blue-500: #3b82f6;
	--color-text-primary: var(--is-light-theme, var(--color-gray-900))
		var(--is-dark-theme, var(--color-gray-100));
}
```

Custom utilities can be defined using the `@utility` directive:

```css
@utility headline-1 {
	line-height: 1.2;
	font-size: 2.125rem;

	@variant md {
		font-size: 2.75rem;
	}
}
```

Component-specific styles should use PostCSS nesting:

```css
.my-class {
	&:hover {
		@apply text-red;
	}
}
```

The project includes a comprehensive design system with semantic color tokens that adapt to light/dark themes automatically.
