// See https://kit.svelte.dev/docs/types#app
// for information about these interfaces
declare global {
	namespace App {
		// interface Error {}
		// interface Locals {}
		// interface PageData {}
		// interface Platform {}
	}

	// METADATA
	interface ShareImage {
		src: string;
		width: number;
		height: number;
	}
	interface SocialItem {
		title: string;
		icon: string;
		url?: string;
		onClick?: () => void;
	}
	interface Fontdata {
		typekit?: string;
		googleFonts?: { family: string; weights: string[]; italics: string[] }[];
		fontAwesome?: string;
	}
	interface Metadata {
		siteName: string;
		group?: string | undefined;
		tag?: string;
		title: string;
		description: string;
		date_created?: Date;
		date_modified?: Date;
		url?: string;
		route?: string;
		publisher?: {
			name: string;
			url: string;
		};
		author: {
			name: string;
			url: string;
			twitter: {
				url: string;
				handle: string;
			};
		};
		image: {
			alt: string;
			large: ShareImage;
			small: ShareImage;
		};
		email?: string;
		social?: SocialItem[];
		share?: SocialItem[];
		colors: {
			background: string;
			theme: string;
		};
	}

	// For classes sent as props so they can be strings or arrays of strings
	type ClassValue =
		| ClassArray
		| ClassDictionary
		| string
		| number
		| bigint
		| null
		| boolean
		| undefined;
	type ClassDictionary = Record<string, any>;
	type ClassArray = ClassValue[];
	type Classes = ClassArray | ClassValue;

	// YAML + Markdown pages. Can have metadata + anything else!
	interface Yamarkdown extends Metadata {
		[key: string]: unknown;
	}

	// prose pages have metadata + body, nothing else!
	interface YamarkdownProse extends Metadata {
		body: string;
	}
}

// prevent typescript errors on vite-imagetools imports by suffixing with '&imagetools'
declare module '*&imagetools' {
	/**
	 * actual types
	 * - code
	 * https://github.com/JonasKruckenberg/imagetools/blob/main/packages/core/src/output-formats.ts
	 * - docs
	 * https://github.com/JonasKruckenberg/imagetools/blob/main/docs/guide/getting-started.md#metadata
	 */
	const out;
	export default out;
}

// prevent typescript errors on yaml imports
declare module '*.yaml' {
	// eslint-disable-next-line @typescript-eslint/no-explicit-any
	const value: Record<string, any>;
	export default value;
}

declare module '*.yml' {
	// eslint-disable-next-line @typescript-eslint/no-explicit-any
	const value: Record<string, any>;
	export default value;
}

export {};
