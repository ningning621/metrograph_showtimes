import { json } from '@sveltejs/kit';

import type { Block } from '$lib/components/search/types';
import articles from '../[article]/articles';

export const GET = async () => {
	const blocks: Block[] = [
		// iterate over groups to create entries
		...Object.entries(articles).map(([pathname, article]) => ({
			breadcrumbs: [article.title],
			href: `/${pathname}`,
			content: article.description,
			type: article.group,
			rank: article?.rank || 4
		}))
	];

	return json({
		blocks
	});
};
