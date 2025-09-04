import { error } from '@sveltejs/kit';
import articles from './articles.js';

export const prerender = true;

export const entries = () => Object.keys(articles).map((article) => ({ article }));

export const load = async ({ params }) => {
	const article = articles?.[params.article];
	if (!article) error(404, 'Not found');

	return article;
};
