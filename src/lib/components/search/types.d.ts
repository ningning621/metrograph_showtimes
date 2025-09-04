import type { IconifyIconAttributes } from 'iconify-icon/dist/iconify-icon.js';

/** specific subsections */
export type StashType = 'Site Information';

/** all page groupings */
export type Type = 'All' | StashType;

export interface Block {
	icon?: IconifyIconAttributes['icon'];
	type?: Type;
	breadcrumbs: string[];
	href: string;
	content?: string;
	rank: number;
}

export interface Tree {
	breadcrumbs: string[];
	href: string;
	node: Block;
	children: Tree[];
}

export interface SearchGroup {
	value: Type;
	inline: string;
	placeholder: string;
	showAllOnEmpty: boolean;
}
