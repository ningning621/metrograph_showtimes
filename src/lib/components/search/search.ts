import flexsearch from 'flexsearch';

import type { Block, Tree, Type } from './types';
import searchGroups from './groups.ts';

const Index = flexsearch.Index ?? flexsearch;

/** If the search is already initialized */
export let inited = false;

let indexes: flexsearch.Index[] = [];

// these are served by default
const stashes = new Map<string, Block['href'][]>(Object.keys(searchGroups).map((key) => [key, []]));

const map = new Map<string, Block>();

const hrefs = new Map<string, string>();

const showAllOnEmptyTypes = new Set<Type>(
	Object.values(searchGroups)
		.filter((d) => d.showAllOnEmpty)
		.map((d) => d.value)
);

/**
 * Initialize the search index
 */
export function init(blocks: Block[]) {
	if (inited) return;

	// we have multiple indexes, so we can rank sections (migration guide comes last)
	const maxRank = Math.max(...blocks.map((block) => block.rank ?? 0));

	indexes = Array.from({ length: maxRank + 1 }, () => new Index({ tokenize: 'forward' }));

	for (const block of blocks) {
		const title = block.breadcrumbs?.at(-1);
		if (!title) continue;
		map.set(block.href, block);
		// NOTE: we're not using a number as the ID here, but it is recommended:
		// https://github.com/nextapps-de/flexsearch#use-numeric-ids
		// If we were to switch to a number we would need a second map from ID to block
		// We need to keep the existing one to allow looking up recent searches by URL even if docs change
		// It's unclear how much browsers do string interning and how this might affect memory
		// We'd probably want to test both implementations across browsers if memory usage becomes an issue
		// TODO: fix the type by updating flexsearch after
		// https://github.com/nextapps-de/flexsearch/pull/364 is merged and released
		indexes[block.rank ?? 0].add(block.href, `${title} ${block.content}`);

		hrefs.set(block.breadcrumbs.join('::'), block.href);

		if (block?.type && block?.href) {
			// include in all stash by default
			stashes.get('All')?.push(block.href);

			if (stashes.has(block.type)) {
				stashes.get(block.type)?.push(block.href);
			}
		}
	}

	inited = true;
}

/**
 * Search for a given query in the existing index
 */
export function search(query: string, type: Type): Tree[] {
	// if there's no query and we're showing all on empty types
	// return early with the designated stash
	if (!query && type && showAllOnEmptyTypes.has(type) && stashes.has(type)) {
		const hrefs = stashes.get(type);
		if (hrefs) {
			const blocks = hrefs?.map(lookup);
			return tree([], blocks).children;
		}
	}

	const escaped = query.replace(/[-[\]{}()*+?.,\\^$|#\s]/g, '\\$&');
	const regex = new RegExp(`(^|\\b)${escaped}`, 'i');

	const blocks = indexes
		.flatMap((index) => index.search(query))
		.map((href: string) => lookup(href))
		.filter((block: Block) => block && (type === 'All' || block.type === type))
		.map((block, rank) => ({ block, rank }) as { block: Block; rank: number })
		.sort((a, b) => {
			const aTitleMatches = regex.test(a.block.breadcrumbs.at(-1) as string);
			const bTitleMatches = regex.test(b.block.breadcrumbs.at(-1) as string);

			// massage the order a bit, so that title matches
			// are given higher priority
			if (aTitleMatches !== bTitleMatches) {
				return aTitleMatches ? -1 : 1;
			}

			return a.block.breadcrumbs.length - b.block.breadcrumbs.length || a.rank - b.rank;
		})
		.map(({ block }) => block);

	const results = tree([], blocks).children;

	return results;
}

/**
 * Get a block with details by its href
 */
export function lookup(href: string): Block | undefined {
	return map.get(href);
}

function tree(breadcrumbs: string[], blocks: Block[]): Tree {
	const depth = breadcrumbs.length;

	const node = blocks.find((block) => {
		if (block.breadcrumbs.length !== depth) return false;
		return breadcrumbs.every((part, i) => block.breadcrumbs[i] === part);
	});

	const descendants = blocks.filter((block) => {
		if (block.breadcrumbs.length <= depth) return false;
		return breadcrumbs.every((part, i) => block.breadcrumbs[i] === part);
	});

	const childParts = Array.from(new Set(descendants.map((block) => block.breadcrumbs[depth])));

	return {
		breadcrumbs,
		href: hrefs.get(breadcrumbs.join('::')) as string,
		node: node as Block,
		children: childParts.map((part) => tree([...breadcrumbs, part], descendants))
	};
}
